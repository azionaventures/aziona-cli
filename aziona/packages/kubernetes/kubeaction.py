# -*- coding: utf-8 -*-
import os
import sys
import tempfile

from aziona.core import argparser, commands, files, io, text
from aziona.core.conf import settings
from aziona.packages.kubernetes import functions


def argsinstance():
    parser = argparser.argparse.ArgumentParser()
    parser.add_argument(
        "--manifest-path", required=True, type=str, help="Path of kube manifest"
    )
    parser.add_argument(
        "--manifest-yaml", default=[], nargs="+", help="Path of kube manifest"
    )
    parser.add_argument(
        "--kustomize-image",
        action=argparser.StoreDictParser,
        default={},
        help="Path of kube manifest",
    )
    parser.add_argument(
        "--wait-readiness",
        default=False,
        type=bool,
        help="Wait cluster readiness",
    )
    parser.add_argument(
        "--blue-green",
        default=False,
        type=bool,
        help="Blue green deploy",
    )
    parser.add_argument(
        "--check-container-sha256",
        default=False,
        type=bool,
        help="Check image hash",
    )
    parser.add_argument(
        "--action",
        choices=["apply", "delete"],
        required=True,
        type=str,
        help="Comando k8s da eseguire, scelta tra apply e delete.",
    )

    argparser.standard_args(parser)

    return parser


def kubeaction_exec(action: str, filename: str):
    manifests = tempfile.NamedTemporaryFile(mode="w")
    single = tempfile.NamedTemporaryFile(mode="w")
    try:
        # interpolazione delle variabili d'ambiente all'interno del file
        manifests.write(text.interpolation_file(filename))
        manifests.seek(0)
        data = files.yaml.load_all(open(manifests.name, "r"))
        for yml in data:
            if (
                yml.get("spec", {})
                .get("template", {})
                .get("spec", {})
                .get("containers", None)
                is not None
            ):
                for container in yml["spec"]["template"]["spec"]["containers"]:
                    for item in container.get("env", {}):
                        if "valueFrom" in item.keys():
                            continue
                        if isinstance(item["value"], bool):
                            item["value"] = "true" if item["value"] else "false"
                            continue
                        if isinstance(item["value"], (int, float)):
                            item["value"] = str(item["value"])
                            continue
                        if item["value"] is None or item["value"] == "":
                            item["value"] = None
                            continue
                        if isinstance(item["value"], str):
                            continue
                        io.critical(
                            "Il valore della '%s' non è valido (deve essere un: int, float, str o null)"
                            % item["name"]
                        )
            files.yaml_dump(single.name, yml)
            io.debug(yml)
            commands.exec("kubectl -f %s %s" % (single.name, action))
    finally:
        manifests.close()
        single.close()


def load(args) -> None:
    """Esegue la logica del modulo.

    Args:
        args(dict,argparse.Namespace,optional): argomenti richiesti dal modulo

    Returns:
        None:
    """
    if isinstance(args, dict):
        args = argparser.namespace_from_dict(argsinstance()._actions, args)

    if not isinstance(args, argparser.argparse.Namespace):
        io.critical("Argomenti non validi")

    try:
        pwd = os.getcwd()
        os.chdir(args.manifest_path)

        if args.blue_green is True:
            current_prod = functions.set_blue_green_target(
                domain=settings.getenv("APPLICATION_DOMAIN")
            )

        if (
            args.check_container_sha256 is True
            and functions.check_container_sha(
                current_prod,
                settings.getenv("DOCKER_IMAGE"),
            )
            is False
        ):
            commands.exec(
                'echo "::set-output name=result::This release image is alread running in the current production"'
            )
            io.critical(
                "This release image is alread running in the current production"
            )

        for (key, value) in args.kustomize_image.items():
            functions.kustomize(name=key, image=value)

        if args.manifest_yaml:
            for manifest in args.manifest_yaml:
                kubeaction_exec(action=args.action, filename=manifest)
        else:
            # L'output del kustomize vengono salvati in un file temporaneo
            temp = tempfile.NamedTemporaryFile(mode="w")
            try:
                commands.exec("kustomize build . > %s" % temp.name)
                kubeaction_exec(action=args.action, filename=temp.name)
            finally:
                temp.close()

        if args.wait_readiness is True:
            functions.check_readiness(
                settings.getenv("APPLICATION_NAME"),
                settings.getenv("ENVIRONMENT"),
            )
    except Exception as e:
        io.exception(e)
    finally:
        os.chdir(pwd)


def main() -> bool:
    try:
        load(args=argsinstance().parse_args())
    except KeyboardInterrupt as e:
        io.exception(e)
    except Exception as e:
        io.exception(e)
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
