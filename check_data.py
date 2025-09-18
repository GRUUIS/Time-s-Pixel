import pandas as pd
import os

def time_to_minutes(t):
    if pd.isna(t) or t == '':
        return None
    try:
        h, m = map(int, t.split(':'))
        return h * 60 + m
    except:
        return None

def minutes_to_time(m):
    if pd.isna(m):
        return ''
    h = int(m // 60)
    m = int(m % 60)
    return f"{h:02d}:{m:02d}"

def clean_and_save(file_path, label, output_path=None):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None
    # Identify time columns
    time_cols = [col for col in df.columns if col.upper() in ['RISE', 'SET', 'TRAN.']]
    # Convert time columns to minutes
    for col in time_cols:
        df[col] = df[col].apply(time_to_minutes)
    # Interpolate missing values
    df_clean = df.interpolate(method="linear", limit_direction="both")
    # Convert back to time strings
    for col in time_cols:
        df_clean[col] = df_clean[col].apply(minutes_to_time)
    if output_path:
        df_clean.to_csv(output_path, index=False)
        print(f"Cleaned {label} saved to {output_path}")
    print(f"\n=== {label} (Cleaned) ===")
    print(f"Rows: {len(df_clean)} | Columns: {df_clean.columns.tolist()}")
    print(df_clean.head(10).to_string(index=False))
    return df_clean

def main():
    clean_and_save("hongkong_sunrise_sunset_2024.csv", "Sunrise/Sunset Data", "hongkong_sunrise_sunset_2024_clean.csv")
    clean_and_save("moonrise_moonset_2024.csv", "Moonrise/Moonset Data", "moonrise_moonset_2024_clean.csv")

if __name__ == "__main__":
    main()


# import pandas as pd

# # Load the downloaded CSV file
# data_file = "hongkong_sun_moon_2024.csv"

# # Read the CSV and display basic info
# def check_data_cleanliness(filename):
#     df = pd.read_csv(filename)
#     print("Columns:", df.columns.tolist())
#     print("Entire data:")
#     print(df)
#     print("Null values per column:")
#     print(df.isnull().sum())

# if __name__ == "__main__":
#     check_data_cleanliness(data_file)
