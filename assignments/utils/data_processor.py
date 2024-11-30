import hashlib
import json

class DataProcessor:
    """
    A class to process and filter data from API responses.

    Attributes:
        REQUIRED_WEATHER_COLUMNS (list): A list of required column names for weather data.
        REQUIRED_STATION_COLUMNS (list): A list of required column names for station data.
    """

    REQUIRED_WEATHER_COLUMNS = [
        'timestamp', 'temperature', 'groundtemperature', 'feeltemperature',
        'windgusts', 'windspeedBft', 'humidity', 'precipitation', 'sunpower', 'stationid'
    ]
    REQUIRED_STATION_COLUMNS = ['stationid', 'stationname', 'lat', 'lon', 'regio']

    def _generate_hash(self, data_dict):
        """
        Generate a SHA-256 hash from a dictionary.

        Args:
            data_dict (dict): A dictionary containing data to be hashed.

        Returns:
            str: A SHA-256 hash of the dictionary.
        """
        unique_data = {
            'stationid': data_dict.get('stationid'),
            'timestamp': data_dict.get('timestamp')
        }
        json_str = json.dumps(unique_data, sort_keys=True)
        return hashlib.sha256(json_str.encode('utf-8')).hexdigest()

    def _process_data(self, data, required_columns, generate_id=False):
        """
        Generic method to process and filter data.

        Args:
            data (list of dict): A list of dictionaries containing raw data.
            required_columns (list): A list of required column names.
            generate_id (bool, optional): Whether to generate a unique ID for each item. Defaults to False.

        Returns:
            list of dict: A list of dictionaries containing processed data.
        """
        processed_data = []
        for item in data:
            processed_item = {col: item.get(col) for col in required_columns}
            if generate_id:
                processed_item['measurementid'] = self._generate_hash(item)
            processed_data.append(processed_item)
        return processed_data

    def process_weather_data(self, data):
        """
        Process weather data from the API response.

        Args:
            data (list of dict): A list of dictionaries containing raw weather data.

        Returns:
            list of dict: A list of dictionaries containing processed weather data with generated IDs.
        """
        return self._process_data(
            data,
            self.REQUIRED_WEATHER_COLUMNS,
            generate_id=True
        )

    def process_station_data(self, data):
        """
        Process station data from the API response.

        Args:
            data (list of dict): A list of dictionaries containing raw station data.

        Returns:
            list of dict: A list of dictionaries containing processed station data.
        """
        return self._process_data(
            data,
            self.REQUIRED_STATION_COLUMNS
        )