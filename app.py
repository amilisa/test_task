import cli_argument_parser

parser = cli_argument_parser.CliArgumentParser()
parser.configure_parser()
args = parser.parse()
