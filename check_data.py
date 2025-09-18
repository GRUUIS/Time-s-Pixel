import pandas as pd

# Load the downloaded CSV file
data_file = "hongkong_sun_moon_2024.csv"

# Read the CSV and display basic info
def check_data_cleanliness(filename):
    df = pd.read_csv(filename)
    print("Columns:", df.columns.tolist())
    print("Entire data:")
    print(df)
    print("Null values per column:")
    print(df.isnull().sum())

if __name__ == "__main__":
    check_data_cleanliness(data_file)
