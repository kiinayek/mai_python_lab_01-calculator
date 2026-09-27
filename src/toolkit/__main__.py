import argparse
import sys

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import ToolkitError


def main(argv=None):
    
    parser = argparse.ArgumentParser(prog="toolkit")
    sub = parser.add_subparsers(dest="command")

    calc_p = sub.add_parser("calc")
    calc_p.add_argument("expression")

    conv_p = sub.add_parser("convert")
    conv_p.add_argument("value", type=float)
    conv_p.add_argument("--from", dest="from_unit", required=True)
    conv_p.add_argument("--to", dest="to_unit", required=True)

    args = parser.parse_args(argv)

    try:
        if args.command == "calc":
            print(calculate(args.expression))
        elif args.command == "convert":
            print(convert(args.value, args.from_unit, args.to_unit))
        else:
            parser.print_help()
        return 0
    except ToolkitError as e:
        print(e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())