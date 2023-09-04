import cli_argument_parser
import pandas as pd


parser = cli_argument_parser.CliArgumentParser()
parser.configure_parser()
args = parser.parse()
personal_data_path = args.pdata
financial_data_path = args.fdata
countries = args.countries

personal_data = pd.read_csv(personal_data_path)
financial_data = pd.read_csv(financial_data_path)

personal_data_filtered = personal_data[personal_data.country.isin(countries)]
