
import yaml
from flask import Flask, request, send_file, make_response

import pandas as pd
import logging.config
import json
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from common import data_processing as dp


API_VERSION = "api_version"

app = Flask(__name__)

with open(os.path.join(API_VERSION, "logging_config.yaml"), "r") as config:
    log_config = yaml.safe_load(config.read())

logging.config.dictConfig(log_config)
logger = logging.getLogger("api")


def upload_files(request):
    """
    Upload and save personal and financial data files.
    :param request: Flask request object.
    :return: Paths for personal and financial data files.
    """
    personal_data_file = request.files['personal_data']
    financial_data_file = request.files['financial_data']

    personal_data_path = os.path.join(API_VERSION, "uploads/personal_data.csv")
    financial_data_path = os.path.join(API_VERSION, "uploads/financial_data.csv")
    personal_data_file.save(personal_data_path)
    financial_data_file.save(financial_data_path)
    return personal_data_path, financial_data_path


@app.route('/process_data', methods=['POST'])
def process_data():
    """
    Process uploaded data, merge datasets, and save the result.
    :return: Flask response with processed data or error message.
    """
    try:
        data = request.form.get('data')
        data_dict = json.loads(data)
        countries = data_dict.get('countries', [])
        
        personal_data_path, financial_data_path = upload_files(request)
        
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

        output_dir = "client_data"
        output_path = os.path.join(API_VERSION, output_dir)
        os.makedirs(output_path, exist_ok=True)
        
        output_filename = "client_data.csv"
        dp.save_data(datasets_merged, os.path.join(output_path, output_filename))
        
        return send_file(os.path.join(output_dir, output_filename), as_attachment=True)
    except json.JSONDecodeError as exception:
        logger.error(exception)
        return make_response(json.dumps({"error": "Invalid data in the request"}), 400)
    except FileNotFoundError as exception:
        logger.error(exception)
        return make_response(json.dumps({"error": "File not found"}), 404)
    except Exception as exception:
        logger.error(exception)
        return make_response(json.dumps({"error": "Error processing data"}), 500)

if __name__ == '__main__':
    app.run(debug=True)
