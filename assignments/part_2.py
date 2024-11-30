from utils.buienradar_api import BuienradarAPI
from utils.data_analysis import analyze_weather_data

if __name__ == "__main__":
    api = BuienradarAPI()

    print("Collect data and perform data analysis...")
    
    api.store_data()
    analyze_weather_data(api.get_database_manager())