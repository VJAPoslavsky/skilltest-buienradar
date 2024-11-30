from utils.buienradar_api import BuienradarAPI

if __name__ == "__main__":
    api = BuienradarAPI()

    print("Collect and store data...")

    api.store_data()