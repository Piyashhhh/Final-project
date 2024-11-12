import psycopg2
import pandas as pd
import random
import time

# Database connection details
db_params = {
    'dbname': 'CattleMetrics',
    'user': 'postgres',
    'password': 'admin',
    'host': 'localhost',
    'port': 5432
}

# Insert data into PostgreSQL with timestamp
def insert_data_into_postgres(data, db_params):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Ensure the 'Updated_At' column is added to track updates
        query = '''
        ALTER TABLE "CowMetrics"
        ADD COLUMN IF NOT EXISTS "Updated_At" TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        '''
        cursor.execute(query)
        conn.commit()

        # Insert fluctuated data
        for index, row in data.iterrows():
            query = '''
            INSERT INTO "CowMetrics" ("Cow ID", "HeartRate", "BodyTemp", "ActivityLevel", 
                                      "EatingBehavior", "Vocalizations", "EnvironmentalTemp", 
                                      "FeedingTime", "LyingTime", "StandingTime", "StressLevel", "Updated_At")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP);
            '''
            cursor.execute(query, (
                row['Cow ID'], row['Heart Rate'], row['Body Temp'], row['Activity Level'], 
                row['Eating Behavior'], row['Vocalizations'], row['Environmental Temp'], 
                row['Feeding Time'], row['Lying Time'], row['Standing Time'], row['Stress Level']
            ))
        
        conn.commit()  # Commit transaction
        print(f"Data updated in PostgreSQL at {time.ctime()}")

    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
        conn.close()

# Simulate data fluctuations (example)
def simulate_fluctuations():
    # Example data with random fluctuations
    cows_data = pd.DataFrame({
        'Cow ID': ['C1', 'C2', 'C3'],
        'Heart Rate': [80, 75, 78],
        'Body Temp': [38.5, 38.7, 38.6],
        'Activity Level': [5, 6, 4],
        'Eating Behavior': [2, 3, 1],
        'Vocalizations': [3, 4, 2],
        'Environmental Temp': [22, 23, 21],
        'Feeding Time': [15, 12, 20],
        'Lying Time': [1, 0, 1],
        'Standing Time': [0, 1, 0],
        'Stress Level': [0, 1, 0]
    })

    # Simulate small fluctuations
    cows_data['Heart Rate'] = cows_data['Heart Rate'] + random.randint(-2, 2)
    cows_data['Body Temp'] = cows_data['Body Temp'] + random.uniform(-0.1, 0.1)
    cows_data['Activity Level'] = cows_data['Activity Level'] + random.randint(-1, 1)
    cows_data['Eating Behavior'] = cows_data['Eating Behavior'] + random.randint(-1, 1)
    cows_data['Vocalizations'] = cows_data['Vocalizations'] + random.randint(-1, 1)
    cows_data['Environmental Temp'] = cows_data['Environmental Temp'] + random.randint(-1, 1)
    cows_data['Feeding Time'] = cows_data['Feeding Time'] + random.randint(-2, 2)
    cows_data['Lying Time'] = random.choice([0, 1])
    cows_data['Standing Time'] = random.choice([0, 1])
    cows_data['Stress Level'] = random.choice([0, 1])

    return cows_data

# Main loop to insert data every minute
while True:
    fluctuated_data = simulate_fluctuations()
    insert_data_into_postgres(fluctuated_data, db_params)
    time.sleep(0.1)  # Wait for 1 minute before the next update
