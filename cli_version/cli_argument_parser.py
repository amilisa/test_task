import argparse
from cli_version import arguments

class CliArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def configure_parser(self):
        self.parser.add_argument("--pdata", help="path to personal data", type=str, required=True)
        self.parser.add_argument("--fdata", help="path to financial data", type=str, required=True)
        self.parser.add_argument("--countries", help="countires to filter", nargs="*", type=str, default=[])

    def parse(self):
        args = self.parser.parse_args()
        return arguments.Arguments(args.pdata, args.fdata, args.countries)