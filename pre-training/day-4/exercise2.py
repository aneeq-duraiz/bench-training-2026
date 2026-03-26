import requests


def get_coordinates_by_name(city_name: str):
    geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1
    }

    try:
        response = requests.get(geocode_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "results" not in data or not data["results"]:
            print(f"Error: Could not find coordinates for city '{city_name}'.")
            return None

        result = data["results"][0]
        return {
            "name": result.get("name", city_name),
            "country": result.get("country", ""),
            "latitude": result.get("latitude"),
            "longitude": result.get("longitude")
        }

    except requests.RequestException as exc:
        print(f"Error: Failed to fetch coordinates. Details: {exc}")
        return None


def weather_code_to_description(code: int) -> str:
    weather_map = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return weather_map.get(code, "Unknown weather condition")


def get_current_weather(latitude: float, longitude: float):
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m,weather_code"
    }

    try:
        response = requests.get(weather_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data.get("current")
        if not current:
            print("Error: Current weather data is unavailable.")
            return None

        temp_c = current.get("temperature_2m")
        wind_speed = current.get("wind_speed_10m")
        weather_code = current.get("weather_code")

        if temp_c is None or wind_speed is None or weather_code is None:
            print("Error: Incomplete weather data received.")
            return None

        temp_f = (temp_c * 9 / 5) + 32
        description = weather_code_to_description(weather_code)

        return {
            "temp_c": temp_c,
            "temp_f": temp_f,
            "wind_speed": wind_speed,
            "description": description
        }

    except requests.RequestException as exc:
        print(f"Error: Failed to fetch weather data. Details: {exc}")
        return None


if __name__ == "__main__":
    city_input = input("Enter city name: ").strip()

    if not city_input:
        print("Error: City name cannot be empty.")
    else:
        location = get_coordinates_by_name(city_input)
        if location:
            weather = get_current_weather(location["latitude"], location["longitude"])
            if weather:
                city_display = location["name"]
                if location["country"]:
                    city_display = f"{city_display}, {location['country']}"

                print("\n=== Current Weather ===")
                print(f"City: {city_display}")
                print(f"Temperature: {weather['temp_c']:.1f} C / {weather['temp_f']:.1f} F")
                print(f"Wind Speed: {weather['wind_speed']} km/h")
                print(f"Weather: {weather['description']}")

