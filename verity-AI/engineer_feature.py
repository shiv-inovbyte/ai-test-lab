import generate_data as gd

# creating a feature engineering function to add useful features to the dataset.
# This will create new columns to the data set
def engineer_features(df):
    df["temp_vibration_interaction"] = df["temperature"] * df["vibration"]
    df["vibration_rate_of_change"] = df.groupby("machine_id")["vibration"].diff().fillna(0) 
    df["temp_rolling_avg"] = df.groupby("machine_id")["temperature"].rolling(window=24, min_periods=1).mean().reset_index(0, drop=True)

    # Drop NaN
    return df.dropna().reset_index(drop=True)

# apply feature engineering to the generated data
df = gd.generate_synthetic_data(num_machines=10, duration_days=180)
df_engineered = engineer_features(df)
print("--- Engineered Features ---")
print(df_engineered.head())