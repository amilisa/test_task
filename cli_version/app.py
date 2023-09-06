import pandas as pd
import yaml

import logging.config
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from common import data_processing as dp
from cli_version import cli_argument_parser


CLI_VERSION = "cli_version"

with open(os.path.join(CLI_VERSION, "logging_config.yaml"), "r") as config:
    log_config = yaml.safe_load(config.read())

logging.config.dictConfig(log_config) 
logger = logging.getLogger("cli_app")

parser = cli_argument_parser.CliArgumentParser()
parser.configure_parser()
args = parser.parse()
personal_data_path = args.pdata
financial_data_path = args.fdata
countries = args.countries

try:
    personal_data, financial_data = dp.load_data(personal_data_path, financial_data_path)
    logger.info(f"Loaded personal data with schema {personal_data.columns}.")
    logger.info(f"Loaded financial data with schema {financial_data.columns}.")

    if countries:
        personal_data = dp.filter_data(personal_data, countries)
        
    personal_data_filtered = personal_data.drop(columns=["first_name", "last_name", "country"])
    financial_data_filtered = financial_data.drop(columns=["cc_n"])
    
    datasets_merged = dp.create_client_data(
        personal_data_filtered,
        financial_data_filtered,
        {"id": "client_identifier", "btc_a": "bitcoin_address", "cc_t": "credit_card_type"}
    )
    logger.info(f"Merged two datasets. Final schema: {datasets_merged.columns}.")
    
    output_path = os.path.join(CLI_VERSION, "client_data")
    os.makedirs(output_path, exist_ok=True)
        
    dp.save_data(datasets_merged, os.path.join(output_path, "client_data.csv"))
except Exception as exception:
    logger.error(exception)
