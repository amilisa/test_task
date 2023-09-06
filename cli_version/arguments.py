class Arguments:
    """
    Container for command-line arguments used in data processing.

    :param personal_data_path: Path to personal data file.
    :param financial_data_path: Path to financial data file.
    :param countries: List of countries to filter data for.
    """
    
    def __init__(self, personal_data_path, financial_data_path, countries):
        self.pdata = personal_data_path
        self.fdata = financial_data_path
        self.countries = countries
