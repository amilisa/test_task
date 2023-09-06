import pandas as pd


def load_data(personal_data_path, financial_data_path):
    """
    Load personal and financial data from CSV files.
    :param personal_data_path: Path to a personal data file
    :param financial_data_path: Path to a financial data file
    :return: DataFrame objects
    """
    personal_data = pd.read_csv(personal_data_path)
    financial_data = pd.read_csv(financial_data_path)
    return personal_data, financial_data


def filter_data(personal_data, countries):
    """
    Filter data based on countries.
    :param personal_data: Personal data DataFrame
    :param countries: List of countries to filter data
    :return: Filtered DataFrame
    """
    return personal_data.loc[personal_data["country"].isin(countries), :]


def create_client_data(personal_data, financial_data, columns_renamer):
    """
    Merge datasets and rename columns.
    :param personal_data: Personal data DataFrame
    :param financial_data: Financial data DataFrame
    :param columns_renamer: Dictionary mapping current column names with new names
    :return: Merged DataFrame with renamed columns
    """
    return personal_data\
        .merge(financial_data, how="left", on="id")\
        .rename(columns=columns_renamer)


def save_data(dataset, output_path):
    """
    Save merged data to a CSV file.
    :param dataset: DataFrame to save
    :param output_path: Path to the output file
    :return:
    """
    dataset.to_csv(output_path, index=False)
