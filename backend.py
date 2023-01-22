import requests
import requests_cache

API_KEY = "e1f4f8e145f873c282bb767284038d00"

# Set up cache for requests
requests_cache.install_cache('weather_cache', expire_after=3600)


def get_data(place, forecast_days=None, units='metric', lang='en'):
    try:
        # validate API key
        if not API_KEY:
            raise ValueError("API key is not set.")

        # API url
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}&units={units}&lang={lang}"

        # Make GET request to API
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        filtered_data = data["list"]

        # Filter data by number of forecast days
        if forecast_days:
            nr_values = 8 * forecast_days
            filtered_data = filtered_data[:nr_values]

        return filtered_data
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)
