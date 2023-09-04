import pandas as pd
import yaml

import logging.config

import cli_argument_parser


with open("logging_config.yaml", "r") as config:
    log_config = yaml.safe_load(config.read())

logging.config.dictConfig(log_config) 
logger = logging.getLogger("app")

parser = cli_argument_parser.CliArgumentParser()
parser.configure_parser()
args = parser.parse()
personal_data_path = args.pdata
financial_data_path = args.fdata
countries = args.countries

try:
    personal_data = pd.read_csv(personal_data_path)
    logger.info(f"Loaded personal data with schema {personal_data.columns}.")

    financial_data = pd.read_csv(financial_data_path)
    logger.info(f"Loaded financial data with schema {financial_data.columns}.")

    personal_data_filtered = personal_data[personal_data["country"].isin(countries)].drop(columns=["first_name", "last_name", "country"])
    financial_data_filtered = financial_data.drop(columns=["cc_n"])    
except Exception as exception:
    logger.error(exception)
