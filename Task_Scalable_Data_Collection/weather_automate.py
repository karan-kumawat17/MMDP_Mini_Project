import requests
import pandas as pd
import time
from datetime import datetime, timedelta

API_KEY = "9ed68a12162c982ffc3bfe6822afad80"
BASE_URL = "https://api.openweathermap.org/data/2.5/"


def get_real_time_weather(city, lat, lon):
    url = f"{BASE_URL}weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if "main" in data and "weather" in data:
        return {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Time": datetime.now().strftime("%H:%M:%S"),
            "City": city,
            "Temperature": data["main"]["temp"],
            "Humidity": data["main"]["humidity"],
            "Wind Speed": data["wind"]["speed"],
            "Weather": data["weather"][0]["description"]
        }
    return None


def main():
    CITIES = {
        "Delhi": (28.6139, 77.2090), "Mumbai": (19.0760, 72.8777), "Kolkata": (22.5726, 88.3639),
        "Chennai": (13.0827, 80.2707), "Bengaluru": (12.9716, 77.5946), "Hyderabad": (17.3850, 78.4867),
        "Pune": (18.5204, 73.8567), "Ahmedabad": (23.0225, 72.5714), "Jaipur": (26.9124, 75.7873),
        "Lucknow": (26.8467, 80.9462), "Kanpur": (26.4499, 80.3319), "Guwahati": (26.1151, 91.7032),
        "Indore": (22.7196, 75.8577), "Patna": (25.5941, 85.1376), "Bhopal": (23.2599, 77.4126),
        "Ludhiana": (30.9010, 75.8573), "Agra": (27.1767, 78.0081), "Varanasi": (25.3176, 82.9739),
        "Surat": (21.1702, 72.8311), "Visakhapatnam": (17.6868, 83.2185)
    }

    df = pd.DataFrame()
    filename = "BharatWeather_Trends.csv"
    print("Press Ctrl+C to stop the data collection process.")

    try:
        while True:
            weather_data = []

            for city, (lat, lon) in CITIES.items():
                print(f"Fetching real-time weather data for {city}")
                real_time_weather = get_real_time_weather(city, lat, lon)
                if real_time_weather:
                    weather_data.append(real_time_weather)
                time.sleep(2)

            if weather_data:
                df = pd.DataFrame(weather_data)
                df.to_csv(filename, index=False, mode='a', header=not pd.io.common.file_exists(filename))
                print(f"Data appended to {filename}")
            else:
                print("No data available. Retrying in 30 seconds...")
            time.sleep(30)
    except KeyboardInterrupt:
        print("\nData collection stopped. Final data saved to BharatWeather_Trends.csv")

if __name__ == "__main__":
    main()
