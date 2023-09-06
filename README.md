## Description
This application takes two files, representing personal and financal data of customers, and a list of countries as input. Personal data is filtered out leaving only customers from the chosen countries.
The application provides a merged dataset in a required format with emails and customer financial data.

The application can be used as command line interface (CLI) or as an API.
## Usage
### CLI
Run ```python3.11 cli_version/app.py --pdata "/path/to/personal_data/file.csv" --fdata "/path/to/personal_data/file.csv" --countries "<country1>" "<country2>"``` with required paths and countries.<br />
The output file is saved to ```cli_version/client_data```.
### API
Run ```api_version/app.py```.<br />
Example of request: ```
curl -X POST -H "Content-Type: multipart/form-data" 
    -F "personal_data=@/path/to/personal_data/file.csv" 
    -F "financial_data=@/path/to/personal_data/file.csv" 
    -F "data={\"countries\": [\"<country1>\", \"<country2>\"]}" 
    http://localhost:5000/process_data 
     -o "/path/to/your/directory/client_data.csv"```.<br />
API will send the output file to ```"/path/to/your/directory/client_data.csv"``` you provide with request.
## Requirements
Python 3.11
