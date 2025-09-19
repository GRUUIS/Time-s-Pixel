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
    """Clean CSV data by preserving NaN values for missing astronomical events.
    
    NOTE: We preserve NaN values for missing moonrise/moonset times.
    These represent genuine astronomical events - some days the moon 
    simply doesn't rise or set, which is natural and should not be interpolated.
    """
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
    
    # Create clean copy - preserve original structure
    df_clean = df.copy()
    
    # Only clean invalid time formats, preserve genuine NaN/missing values
    for col in time_cols:
        # Track originally missing values (these should stay missing)
        originally_missing = df[col].isna() | (df[col] == '') | (df[col].astype(str) == 'nan')
        
        # For non-missing values, validate time format
        for idx in df.index:
            if not originally_missing.iloc[idx]:
                time_val = df.at[idx, col]
                try:
                    # Validate time format
                    if pd.notna(time_val) and time_val != '':
                        parts = str(time_val).split(':')
                        if len(parts) == 2:
                            hours, minutes = int(parts[0]), int(parts[1])
                            if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                                # Invalid time, mark as missing
                                df_clean.at[idx, col] = None
                        else:
                            # Invalid format, mark as missing
                            df_clean.at[idx, col] = None
                except (ValueError, AttributeError):
                    # Conversion error, mark as missing
                    df_clean.at[idx, col] = None
        
        # Ensure originally missing values remain missing
        df_clean.loc[originally_missing, col] = None
    
    if output_path:
        df_clean.to_csv(output_path, index=False)
        print(f"Cleaned {label} saved to {output_path}")
        
        # Count preserved missing values
        missing_count = df_clean[time_cols].isna().sum().sum()
        print(f"Preserved {missing_count} missing astronomical events (as they should be)")
    
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
