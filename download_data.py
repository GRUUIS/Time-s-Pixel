import requests
import os

# URL for Hong Kong sunrise, sunset, and moon time data (2024)
DATA_URL = "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=SRS&year=2024&rformat=csv"
DATA_FILE = "hongkong_sun_moon_2024.csv"

# Download the CSV file
def download_data(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Data downloaded and saved as {filename}")

if __name__ == "__main__":
    download_data(DATA_URL, DATA_FILE)
    # Print the first few lines to verify
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for i in range(10):
            line = f.readline()
            if not line:
                break
            print(line.strip())
