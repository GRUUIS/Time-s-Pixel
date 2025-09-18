import requests
import os

SUN_URL = "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=SRS&year=2024&rformat=csv"
SUN_FILE = "hongkong_sunrise_sunset_2024.csv"
    
# URL and filename for Hong Kong moonrise/moonset data (2024)
MOON_URL = "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=MRS&year=2024&rformat=csv"
MOON_FILE = "moonrise_moonset_2024.csv"

# Download the CSV file
def download_data(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Data downloaded and saved as {filename}")
    
# Download moonrise/moonset CSV file
def download_moon_data():
    response = requests.get(MOON_URL)
    response.raise_for_status()
    with open(MOON_FILE, "wb") as f:
        f.write(response.content)
    print(f"Moonrise/moonset data downloaded and saved as {MOON_FILE}")

if __name__ == "__main__":
    download_data(SUN_URL, SUN_FILE)
    # Print the first few lines to verify
    with open(SUN_FILE, "r", encoding="utf-8") as f:
        for i in range(10):
            line = f.readline()
            if not line:
                break
            print(line.strip())

    download_moon_data()
    # Print the first few lines to verify moon data
    with open(MOON_FILE, "r", encoding="utf-8") as f:
        for i in range(10):
            line = f.readline()
            if not line:
                break
            print(line.strip())
