import random
import pandas as pd

# Function to generate per-minute synthetic data for each cow with consistent environmental temperature
def generate_per_minute_data(cow_id, num_minutes=250, stress_prob=0.2, base_env_temp=25):
    data = []
    
    # Weights for each factor in the stress equation
    w_heart_rate = 0.3
    w_body_temp = 0.2
    w_eating_behavior = 0.2
    w_vocalizations = 0.2
    w_env_temp = 0.1
    
    # Stress distribution: 80% not stressed, 20% stressed
    stress_level = 1 if random.random() < stress_prob else 0
    
    for minute in range(1, num_minutes + 1):
        # Randomized values based on cow's behavior (ensure no decimals)
        heart_rate = random.randint(60, 80) if random.random() > 0.3 else random.randint(80, 100)
        body_temp = random.randint(38, 40)  # Round to nearest integer (no decimal)
        activity_level = random.randint(10, 50) if random.random() > 0.2 else random.randint(5, 10)
        vocalizations = random.randint(1, 5) if random.random() > 0.2 else random.randint(6, 10)
        
        # Environmental temperature with slight variations (rounded to nearest integer)
        environmental_temp = base_env_temp + random.randint(-2, 2)  # No decimals
        
        eating_behavior = random.randint(15, 30) if random.random() > 0.5 else random.randint(0, 10)
        
        # Generate standing and lying time based on activity level
        standing_time = 1 if activity_level > 30 else 0
        lying_time = 1 if activity_level <= 30 else 0
        
        # Stress level calculation using the formula (modified for 80% not stressed, 20% stressed)
        if stress_level == 1:
            stress_value = (w_heart_rate * (heart_rate - 50) / 10) + (w_body_temp * (body_temp - 38) / 1) - \
                           (w_eating_behavior * (eating_behavior / 30)) + (w_vocalizations * (vocalizations / 2)) + \
                           (w_env_temp * (environmental_temp - 20) / 2)
            stress_level = 1 if stress_value > 0 else 1  # Force stress level to 1 for this cow
        else:
            stress_value = (w_heart_rate * (heart_rate - 50) / 10) + (w_body_temp * (body_temp - 38) / 1) - \
                           (w_eating_behavior * (eating_behavior / 30)) + (w_vocalizations * (vocalizations / 2)) + \
                           (w_env_temp * (environmental_temp - 20) / 2)
            stress_level = 0 if stress_value <= 0 else 0  # Force stress level to 0 for this cow
            
        # Append data for each minute (make sure all values are integers)
        data.append({
            "Cow ID": cow_id,
            "Time (Minute)": minute,
            "Heart Rate": heart_rate,
            "Body Temp": body_temp,
            "Activity Level": activity_level,
            "Eating Behavior": eating_behavior,
            "Vocalizations": vocalizations,
            "Environmental Temp": environmental_temp,
            "Feeding Time": eating_behavior,
            "Lying Time": lying_time,
            "Standing Time": standing_time,
            "Stress Level": stress_level
        })
        
    return data

# Generate data for 250 cows with 80% non-stressed and 20% stressed cows
all_data = []
for cow_num in range(1, 251):
    # Set the probability of stress (20% chance to be stressed)
    cow_data = generate_per_minute_data(f"C{cow_num}", num_minutes=1, stress_prob=0.2)
    all_data.extend(cow_data)

# Convert the generated data to a DataFrame
df = pd.DataFrame(all_data)

# Save the generated data to an Excel file
file_path = r'C:\Users\Admin\Documents\cow_stress_data_80_20_no_decimals.xlsx'
df.to_excel(file_path, index=False)  # Use openpyxl engine for saving

print(f"Data saved successfully to {file_path}")
