import argparse
from cli_version import arguments

class CliArgumentParser:
    """
    Command-line argument parser.
    """
    
    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def configure_parser(self):
        """
        Configure the command-line argument parser with supported arguments.
        """
        self.parser.add_argument("--pdata", help="path to personal data", type=str, required=True)
        self.parser.add_argument("--fdata", help="path to financial data", type=str, required=True)
        self.parser.add_argument("--countries", help="countires to filter", nargs="*", type=str, default=[])

    def parse(self):
        """
        Parse command-line arguments.
        :return: Arguments object
        """
        args = self.parser.parse_args()
        return arguments.Arguments(args.pdata, args.fdata, args.countries)