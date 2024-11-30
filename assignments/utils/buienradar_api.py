import requests
from utils.database_manager import DatabaseManager
from utils.data_processor import DataProcessor

class BuienradarAPI:
    """
    A class to interact with the Buienradar API, process the data, and store it in a database.

    Attributes:
        api_url (str): The URL of the Buienradar API.
        database_manager (DatabaseManager): An instance of the DatabaseManager to manage database operations.
        data_processor (DataProcessor): An instance of the DataProcessor to process the API data.
    """

    def __init__(self, api_url="https://data.buienradar.nl/2.0/feed/json", db_path="data/weather_data.sqlite"):
        """
        Initialize the BuienradarAPI instance.

        Args:
            api_url (str, optional): The URL of the Buienradar API. Defaults to "https://data.buienradar.nl/2.0/feed/json".
            db_path (str, optional): The path to the SQLite database file. Defaults to "data/weather_data.sqlite".
        """
        self.api_url = api_url
        self.database_manager = DatabaseManager(db_path)
        self.data_processor = DataProcessor()

    def _fetch_api_response(self):
        """
        Fetch the API response from Buienradar.

        Returns:
            dict: The JSON response from the API.
        """
        response = requests.get(self.api_url)
        response.raise_for_status()
        return response.json()

    def store_data(self):
        """
        Fetch, process, and store the data in the SQLite database.
        """
        response = self._fetch_api_response()
        weather_data = self.data_processor.process_weather_data(
            response['actual']['stationmeasurements']
        )
        station_data = self.data_processor.process_station_data(
            response['actual']['stationmeasurements']
        )
        self.database_manager.insert_station_data(station_data)
        self.database_manager.insert_weather_data(weather_data)

    def get_database_manager(self):
        """
        Return the DatabaseManager instance.

        Returns:
            DatabaseManager: The instance of the DatabaseManager.
        """
        return self.database_manager