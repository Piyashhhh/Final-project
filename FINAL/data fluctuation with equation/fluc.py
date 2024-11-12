import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

# Load the Trained Model
with open(r"C:\Users\Admin\Desktop\FINAL\data fluctuation with equation\stress_level_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Load the Cow Data
cow_data = pd.read_excel(r"C:\Users\Admin\Desktop\FINAL\data fluctuation with equation\cow data accurate.xlsx")

# Define initial empty lists to store metric data for plotting
time_steps = []
heart_rate_data = []
body_temp_data = []
activity_level_data = []
eating_behavior_data = []
vocalizations_data = []
feeding_time_data = []
lying_time_data = []
standing_time_data = []
predicted_stress_data = []

# Fluctuate data function with random changes in standing and lying time
def fluctuate_data(row):
    # Fluctuate Heart Rate and Body Temperature
    row['Heart Rate'] += np.random.uniform(-2, 2)
    row['Body Temp'] += np.random.uniform(-0.1, 0.1)
    
    # Fluctuate Activity Level based on standing/lying status
    if row['Standing Time'] == 1:
        row['Activity Level'] += np.random.uniform(0, 2)
    elif row['Lying Time'] == 1:
        row['Activity Level'] -= np.random.uniform(0, 1)
    
    # Fluctuate Eating Behavior
    row['Eating Behavior'] = 1 if np.random.rand() > 0.7 else 0
    row['Feeding Time'] += row['Eating Behavior']
    
    # Fluctuate Vocalizations based on stress level
    row['Vocalizations'] = np.random.randint(0, 3) if row['Stress Level'] == 1 else np.random.randint(0, 2)
    
    # Introduce random changes in Standing Time and Lying Time to simulate fluctuation
    if np.random.rand() > 0.5:  # 50% chance of switching states
        row['Standing Time'] = 1 if np.random.rand() > 0.5 else 0
        row['Lying Time'] = 1 if row['Standing Time'] == 0 else 0  # Ensure only one of them is 1 at a time

    return row

# Function to calculate weighted stress
def calculate_weighted_stress(row):
    # Define weights for each metric
    weights = {
        'Heart Rate': 0.3,
        'Body Temp': 0.2,
        'Activity Level': 0.1,
        'Eating Behavior': 0.1,
        'Vocalizations': 0.2,
        'Feeding Time': 0.1
    }
    
    # Normalize the metrics to a range of 0 to 1 for proper weighting
    heart_rate_norm = (row['Heart Rate'] - 50) / 60  # Example normalization
    body_temp_norm = (row['Body Temp'] - 36) / 4
    activity_level_norm = row['Activity Level']  # Assuming Activity Level is already 0-1
    eating_behavior_norm = row['Eating Behavior']
    vocalizations_norm = row['Vocalizations'] / 2
    feeding_time_norm = row['Feeding Time'] / 24  # Normalize feeding time in hours
    
    # Weighted sum calculation
    weighted_sum = (
        weights['Heart Rate'] * heart_rate_norm + 
        weights['Body Temp'] * body_temp_norm + 
        weights['Activity Level'] * activity_level_norm + 
        weights['Eating Behavior'] * eating_behavior_norm + 
        weights['Vocalizations'] * vocalizations_norm + 
        weights['Feeding Time'] * feeding_time_norm
    )
    
    # Calculate stress level (binary: 1 for stressed, 0 for not stressed)
    stress_level = 1 if weighted_sum > 0.5 else 0
    return stress_level

# Initialize the plot
plt.ion()  # Turn on interactive mode
fig, axs = plt.subplots(3, 3, figsize=(15, 10))  # 3x3 grid for separate plots

while True:
    # Apply fluctuations and predict stress level
    cow_data = cow_data.apply(fluctuate_data, axis=1)
    
    # Apply the weighted stress calculation function
    cow_data['Predicted Stress Level'] = cow_data.apply(calculate_weighted_stress, axis=1)
    
    # Collect metrics from one row (you can adjust to track multiple cows if needed)
    heart_rate_data.append(cow_data['Heart Rate'].mean())
    body_temp_data.append(cow_data['Body Temp'].mean())
    activity_level_data.append(cow_data['Activity Level'].mean())
    eating_behavior_data.append(cow_data['Eating Behavior'].mean())
    vocalizations_data.append(cow_data['Vocalizations'].mean())
    feeding_time_data.append(cow_data['Feeding Time'].mean())
    lying_time_data.append(cow_data['Lying Time'].mean())
    standing_time_data.append(cow_data['Standing Time'].mean())
    predicted_stress_data.append(cow_data['Predicted Stress Level'].mean())
    time_steps.append(len(time_steps))  # Keeps counting up, starting from 0


    # Clear and redraw each subplot with more information
    axs[0, 0].clear()
    axs[0, 0].plot(time_steps, heart_rate_data, label='Heart Rate', color='tab:blue')
    axs[0, 0].set_title("Heart Rate Over Time")
    axs[0, 0].set_xlabel("Time (Minutes)")
    axs[0, 0].set_ylabel("Heart Rate (bpm)")
    axs[0, 0].grid(True)
    axs[0, 0].legend(loc='upper right')

    axs[0, 1].clear()
    axs[0, 1].plot(time_steps, body_temp_data, label='Body Temperature', color='tab:orange')
    axs[0, 1].set_title("Body Temperature Over Time")
    axs[0, 1].set_xlabel("Time (Minutes)")
    axs[0, 1].set_ylabel("Temperature (°C)")
    axs[0, 1].grid(True)
    axs[0, 1].legend(loc='upper right')

    axs[0, 2].clear()
    axs[0, 2].plot(time_steps, activity_level_data, label='Activity Level', color='tab:green')
    axs[0, 2].set_title("Activity Level Over Time")
    axs[0, 2].set_xlabel("Time (Minutes)")
    axs[0, 2].set_ylabel("Activity Level")
    axs[0, 2].grid(True)
    axs[0, 2].legend(loc='upper right')

    axs[1, 0].clear()
    axs[1, 0].plot(time_steps, vocalizations_data, label='Vocalizations', color='tab:red')
    axs[1, 0].set_title("Vocalizations Over Time")
    axs[1, 0].set_xlabel("Time (Minutes)")
    axs[1, 0].set_ylabel("Vocalizations")
    axs[1, 0].grid(True)
    axs[1, 0].legend(loc='upper right')

    axs[1, 1].clear()
    axs[1, 1].plot(time_steps, feeding_time_data, label='Feeding Time', color='tab:purple')
    axs[1, 1].set_title("Feeding Time Over Time")
    axs[1, 1].set_xlabel("Time (Minutes)")
    axs[1, 1].set_ylabel("Feeding Time (Hours)")
    axs[1, 1].grid(True)
    axs[1, 1].legend(loc='upper right')

    axs[1, 2].clear()
    axs[1, 2].plot(time_steps, lying_time_data, label='Lying Time', color='tab:cyan')
    axs[1, 2].set_title("Lying Time Over Time")
    axs[1, 2].set_xlabel("Time (Minutes)")
    axs[1, 2].set_ylabel("Lying Time")
    axs[1, 2].grid(True)
    axs[1, 2].legend(loc='upper right')

    axs[2, 0].clear()
    axs[2, 0].plot(time_steps, standing_time_data, label='Standing Time', color='yellow')  # Correct color

    axs[2, 0].set_title("Standing Time Over Time")
    axs[2, 0].set_xlabel("Time (Minutes)")
    axs[2, 0].set_ylabel("Standing Time")
    axs[2, 0].grid(True)
    axs[2, 0].legend(loc='upper right')

    axs[2, 2].clear()
    axs[2, 2].plot(time_steps, predicted_stress_data, label='Predicted Stress Level', color='magenta')  # Corrected color

    axs[2, 2].set_title("Predicted Stress Level Over Time")
    axs[2, 2].set_xlabel("Time (Minutes)")
    axs[2, 2].set_ylabel("Stress Level")
    axs[2, 2].grid(True)
    axs[2, 2].legend(loc='upper right')

    # Refresh the plot every 60 seconds (or adjust as needed)
    plt.pause(1)
