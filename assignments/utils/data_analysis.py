import json

def get_highest_temperature(database_manager):
    query_highest_temp = '''
        SELECT Stations.stationname, MAX(Measurements.temperature) AS max_temperature
        FROM Measurements
        JOIN Stations ON Measurements.stationid = Stations.stationid
        GROUP BY Stations.stationname
        ORDER BY max_temperature DESC
        LIMIT 1;
    '''
    highest_temp = database_manager.execute_query(query_highest_temp)[0]
    return {
        "station": highest_temp[0],
        "temperature": highest_temp[1]
    }

def get_average_temperature(database_manager):
    query_avg_temp = 'SELECT AVG(temperature) FROM Measurements;'
    avg_temp = database_manager.execute_query(query_avg_temp)[0][0]
    return avg_temp

def get_biggest_temperature_difference(database_manager):
    query_biggest_diff = '''
        SELECT Stations.stationname, MAX(ABS(Measurements.feeltemperature - Measurements.temperature)) AS max_difference
        FROM Measurements
        JOIN Stations ON Measurements.stationid = Stations.stationid
        GROUP BY Stations.stationname
        ORDER BY max_difference DESC
        LIMIT 1;
    '''
    biggest_diff = database_manager.execute_query(query_biggest_diff)[0]
    return {
        "station": biggest_diff[0],
        "difference": biggest_diff[1]
    }

def get_north_sea_stations(database_manager):
    query_north_sea = 'SELECT stationname FROM Stations WHERE regio="Noordzee";'
    north_sea_stations = database_manager.execute_query(query_north_sea)
    return [row[0] for row in north_sea_stations]

def analyze_weather_data(
        database_manager,
        output_file="Results/results_part_2.json",
        print_output=True
):
    print("Analyzing weather data...\n")

    highest_temp = get_highest_temperature(database_manager)
    avg_temp = get_average_temperature(database_manager)
    biggest_diff = get_biggest_temperature_difference(database_manager)
    north_sea_stations = get_north_sea_stations(database_manager)

    results = {
        "Question 5": {
            "description": "Which weather station recorded the highest temperature?",
            "result": highest_temp
        },
        "Question 6": {
            "description": "What is the average temperature?",
            "result": avg_temp
        },
        "Question 7": {
            "description": "What is the station with the biggest difference between feel temperature and the actual temperature?",
            "result": biggest_diff
        },
        "Question 8": {
            "description": "Which weather station is located in the North Sea?",
            "result": north_sea_stations
        }
    }

    if print_output:
        print("Analysis results of part 2:")
        print(results)

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"Analysis results saved to {output_file}\n")