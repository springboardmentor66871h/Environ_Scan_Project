import os
import pandas as pd


def merge_and_clean():

    # Get project root directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Define file paths
    pollution_path = os.path.join(base_dir, "data", "raw", "pollution_data.csv")
    weather_path = os.path.join(base_dir, "data", "raw", "weather_data.csv")
    output_path = os.path.join(base_dir, "data", "processed", "cleaned_data.csv")

    # Load data
    pollution = pd.read_csv(pollution_path)
    weather = pd.read_csv(weather_path)

    # Merge (change 'datetime' if your column name is different)
    df = pd.merge(pollution, weather, on="datetime", how="inner")

    # Basic cleaning
    df = df.drop_duplicates()

    # Convert timestamp
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["hour"] = df["datetime"].dt.hour
    df["day"] = df["datetime"].dt.day
    df["month"] = df["datetime"].dt.month

    # Make sure processed folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save cleaned file
    df.to_csv(output_path, index=False)

    print("✅ Merge & Cleaning Completed Successfully!")


if __name__ == "__main__":
    merge_and_clean()