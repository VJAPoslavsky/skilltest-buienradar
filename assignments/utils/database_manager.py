import os
import sqlite3

class DatabaseManager:
    def __init__(self, db_path="data/weather_data.sqlite"):
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            self._setup_database()

    def _setup_database(self):
        """Set up the SQLite database and create tables with indexes."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.executescript('''
                CREATE TABLE Stations (
                    stationid INTEGER PRIMARY KEY,
                    stationname TEXT NOT NULL,
                    lat REAL NOT NULL,
                    lon REAL NOT NULL,
                    regio TEXT NOT NULL
                );

                CREATE TABLE Measurements (
                    measurementid TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    temperature REAL NOT NULL,
                    groundtemperature REAL NOT NULL,
                    feeltemperature REAL NOT NULL,
                    windgusts REAL NOT NULL,
                    windspeedBft INTEGER NOT NULL,
                    humidity REAL NOT NULL,
                    precipitation REAL NOT NULL,
                    sunpower REAL NOT NULL,
                    stationid INTEGER NOT NULL,
                    FOREIGN KEY (stationid) REFERENCES Stations(stationid)
                );

                CREATE INDEX idx_measurements_stationid 
                ON Measurements(stationid);
            ''')
            print("Database setup complete.")

    def _execute_batch(self, query, data):
        """Helper to execute batch operations."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executemany(query, data)

    def insert_station_data(self, station_data):
        """Insert station data into the Stations table."""
        query = '''
            INSERT OR IGNORE INTO Stations (stationid, stationname, lat, lon, regio)
            VALUES (?, ?, ?, ?, ?)
        '''
        self._execute_batch(query, [
            (station['stationid'], station['stationname'], station['lat'], station['lon'], station['regio'])
            for station in station_data
        ])

    def insert_weather_data(self, weather_data):
        """Insert weather data into the Measurements table."""
        query = '''
            INSERT OR IGNORE INTO Measurements 
            (measurementid, timestamp, temperature, groundtemperature, feeltemperature, 
            windgusts, windspeedBft, humidity, precipitation, sunpower, stationid)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self._execute_batch(query, [
            (
                measurement['measurementid'], measurement['timestamp'], measurement['temperature'],
                measurement['groundtemperature'], measurement['feeltemperature'], measurement['windgusts'],
                measurement['windspeedBft'], measurement['humidity'], measurement['precipitation'],
                measurement['sunpower'], measurement['stationid']
            ) for measurement in weather_data
        ])

    def execute_query(self, query):
        """Execute a custom query and return the results."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()