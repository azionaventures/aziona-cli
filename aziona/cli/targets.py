import argparse
from aziona import settings
from aziona.ingress import route


def argsinstance(parser=None):
    if parser is None:
        parser = argparse.ArgumentParser()

    parser.add_argument(
        '-f',
        '--filename',
        default=settings.TEMPLATE_FILE_NAME,
        type=str,
        help='Nome del template o del path(compreso del nome).',
    )
    parser.add_argument(
        'targets',
        metavar='targets',
        type=str,
        nargs='+',
        help='Target che verrano eseguiti a partire dal template indicato. Verrano eseguiti in sequenza.',
    )


def main(args=None):
    try:
        if args is None:
            args = argsinstance().parse_args()

        if not isinstance(args, argparse.Namespace):
            raise Exception('aa')

        r = route.get(
            index=args._type,
            data={
                'filename': args.filename,
                'targets': args.targets,
            }
        )

        r.run()
    except KeyboardInterrupt:
        return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
