# -*- coding: utf-8 -*-
import os

from aziona.core import commands, io
from aziona.core.conf import settings


def kustomize(name: str, image: str) -> None:
    commands.exec("kustomize edit set image %s=%s" % (name, image))


def set_blue_green_target(domain: str) -> str:
    # who is production
    cmd = (
        "kubectl get ingress -o json | jq -r '.items[] | select(.spec.rules[0].host == \"%s\") | .metadata.labels.app'"
        % domain
    )
    current_prod = commands.exec_output(cmd)

    if current_prod == settings.getenv("APPLICATION_GREEN"):
        os.environ["ENVIRONMENT"] = settings.getenv("ENVIRONMENT") + "-blue"
    else:
        os.environ["ENVIRONMENT"] = settings.getenv("ENVIRONMENT") + "-green"

    settings.setenv(
        "APPLICATION_DOMAIN",
        "origin-%s-%s.%s"
        % (
            settings.getenv("APPLICATION_NAME"),
            settings.getenv("ENVIRONMENT"),
            settings.getenv("APPLICATION_ROOT_DOMAIN", "ROOT_DOMAIN"),
        ),
    )

    return current_prod


def check_container_sha(current_prod: str, docker_image: str) -> bool:
    current_sha = (
        "kubectl get pod -l app=%s -o json | jq -r '.items | .[0] | .status.containerStatuses | .[] | select(.name == \"%s\") | .imageID')"
        % (current_prod, current_prod)
    )
    next_sha = (
        "docker image inspect %s | jq -r '.[] | .RepoDigests | .[]'" % docker_image
    )

    io.debug("CURRENT SHA %s" % current_sha)
    io.debug("NEXT SHA %s" % next_sha)

    return False if current_sha == next_sha else True


def alb_domain() -> str:
    stdout = commands.exec_output(
        "kubectl get ingress alb-ingress-connect-nginx -n kube-system -o json"
        + " | "
        + "jq -r '.status.loadBalancer.ingress[0].hostname'"
    )
    io.debug("ALB_INGRESS_DOMAIN=%s" % stdout)
    settings.setenv("ALB_INGRESS_DOMAIN", stdout)
    return stdout


def check_readiness(name: str, env: str) -> None:
    from time import sleep

    cmd = (
        "kubectl get pod -o json | jq -r '.items[] | select(.metadata.labels.app == \"%s-%s\") | .status.phase' | head -n 1"
        % (name, env)
    )
    for t in range(400):
        sleep(15.0)
        status = commands.exec_output(cmd)

        if status == "Running":
            break
        if status in ["ImagePullBackOff", "CrashLoopBackOff"]:
            io.critical("Failed Pod creation - status: %s" % status)

    io.info("Environment ready: %s" % name)
