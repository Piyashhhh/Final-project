import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle

df = pd.read_excel(r'C:\Users\Admin\Desktop\Model Training\cow data accurate.xlsx')


X = df[['Heart Rate', 'Body Temp', 'Activity Level', 'Eating Behavior', 'Vocalizations', 
        'Environmental Temp', 'Feeding Time', 'Lying Time', 'Standing Time']]
y = df['Stress Level']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


model = LinearRegression()
model.fit(X_train, y_train)


y_pred = model.predict(X_test)


y_pred_binary = [1 if pred >= 0.5 else 0 for pred in y_pred]


accuracy = (y_pred_binary == y_test).mean()
print(f"Accuracy: {accuracy * 100:.2f}%")


mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Mean Squared Error: {mse:.4f}')
print(f'R² (Coefficient of Determination): {r2:.4f}')


with open('stress_level_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

print("Model has been saved as 'stress_level_model.pkl'")


with open('stress_level_model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)


new_data = [[75, 38, 50, 3, 2, 22, 45, 30, 25]]  


predicted_stress_level = loaded_model.predict(new_data)
predicted_stress_level_binary = 1 if predicted_stress_level[0] >= 0.5 else 0

print(f"Predicted Stress Level: {predicted_stress_level[0]}")
print(f"Predicted Stress Level (Binary): {predicted_stress_level_binary}")
