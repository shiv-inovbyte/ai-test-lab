import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_synthetic_data(num_machines, duration_days):
    """Geneate time seried data for multiple machines"""
    
    data = []

    for machine_id in range(1, num_machines + 1):
        start_date = datetime(2025,1,1)
        end_date = start_date + timedelta(days=duration_days)
        time_series = pd.date_range(start=start_date, end=end_date, freq='h')

        # Simulate sensor readings
        baseline_vibrations = np.random.normal(loc=50, scale=5, size=len(time_series))
        baseline_temp = np.random.normal(loc=70, scale=3, size=len(time_series))

        # Simulate normal degradtion over time
        vibration_trend = np.linspace(0, 5, len(time_series))
        temp_trend = np.linspace(0, 2, len(time_series))

        # Simulate failure for ssmall subset of machines
        if(np.random.rand() < 0.2):  # 20% chance of failure
            failure_day= np.random.randint(low=duration_days*0.7, high=duration_days)
            failure_index = failure_day * 24  # Convert days to hours

            # Create a spike in sesonsor readings leading up to failure
            spike_indices = range(failure_index-48, failure_index)
            vibration_trend[spike_indices] += np.linspace(3, 10, len(spike_indices))

            #label data as failing in the days before failure
            fail_label_indices = range(failure_index-72, failure_index)
            failure_labels = np.zeros(len(time_series), dtype=int)
            failure_labels[fail_label_indices] = 1
        else:
            failure_labels = np.zeros(len(time_series), dtype=int)

        # Combine trends and noises
        vibration_data = baseline_vibrations + vibration_trend 
        temp_data = baseline_temp + temp_trend

        #Assemble into a data frame
        machine_df = pd.DataFrame({
            'machine_id': machine_id,
            'timestamp': time_series,
            'vibration': vibration_data,
            'temperature': temp_data,
            'failure': failure_labels,
            'operating_hours': np.arange(len(time_series)),
            'failure_imminent': failure_labels
        })
        data.append(machine_df)
        
    return pd.concat(data, ignore_index=True)


#Generate data for 10 machines over 180 days
df = generate_synthetic_data(num_machines=10, duration_days=180)
print("--- Generated Synthetic Data Sample ---")
print(df.head())
print("\n--- Failure Distribution ---")
print(df['failure_imminent'].value_counts())        

        