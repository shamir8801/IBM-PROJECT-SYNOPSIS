import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense
from tensorflow.keras.optimizers import Adam

# Example time series data (replace with your actual lists)
months_list = ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06', '2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12']
target_list = [15, 18, 16, 20, 22, 19, 23, 21, 24, 25, 22, 27]  # Replace with your actual target values (discrete)

# Step 1: Data Preprocessing
# Convert month strings to datetime
months = pd.to_datetime(months_list, format='%Y-%m')

# Create a DataFrame from the lists
df = pd.DataFrame({'Month': months, 'Target': target_list})

# Feature engineering: Extract month and year from the 'Month' column
df['Month_num'] = df['Month'].dt.month  # Month number (1-12)
df['Year'] = df['Month'].dt.year  # Year

# Normalize the target values (scaling between 0 and 1)
scaler = MinMaxScaler(feature_range=(0, 1))
df['Target_scaled'] = scaler.fit_transform(df['Target'].values.reshape(-1, 1))

# Prepare data for GRU: Create sequences
def create_sequences(data, time_step=1):
    X, y = [], []
    for i in range(len(data) - time_step):
        X.append(data[i:(i + time_step), 0])  # Select the input sequence
        y.append(data[i + time_step, 0])  # Target value after the time step
    return np.array(X), np.array(y)

# Prepare the data with a time step of 1 (predict next value based on previous one)
time_step = 1
X, y = create_sequences(df['Target_scaled'].values.reshape(-1, 1), time_step)

# Reshape X to be suitable for GRU [samples, time_steps, features]
X = X.reshape(X.shape[0], X.shape[1], 1)

# Step 2: Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Step 3: Build the GRU model
model = Sequential()
model.add(GRU(units=50, return_sequences=False, input_shape=(X_train.shape[1], 1)))  # 50 units
model.add(Dense(units=1))  # Output layer

# Compile the model
model.compile(optimizer=Adam(), loss='mean_squared_error')

# Step 4: Train the GRU model
model.fit(X, y, epochs=50, batch_size=1, verbose=2)

# Step 5: Forecast on the test set
y_pred = model.predict(X_test)

# Rescale the predictions and actual values back to the original scale
y_pred_rescaled = scaler.inverse_transform(y_pred)
y_test_rescaled = scaler.inverse_transform(y_test.reshape(-1, 1))

# Evaluate the performance (Mean Squared Error for continuous targets)
mse = np.mean((y_pred_rescaled - y_test_rescaled) ** 2)
print(f'Mean Squared Error on test set: {mse:.2f}')


# Step 6: Forecasting the next 12 months (based on the last known value)
last_sequence = df['Target_scaled'].values[-time_step:].reshape(1, time_step, 1)

future_predictions = []
for _ in range(12):  # Forecast 12 months ahead
    next_pred = model.predict(last_sequence)
    future_predictions.append(next_pred[0, 0])
    last_sequence = np.append(last_sequence[:, 1:, :], next_pred.reshape(1, 1, 1), axis=1)

# Rescale the forecasted values back to the original scale
future_predictions_rescaled = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

# Prepare a DataFrame for the forecasted future months
future_months = pd.date_range(start='2025-01-01', periods=12, freq='M')
future_df = pd.DataFrame({'Month': future_months, 'Predicted_Target': future_predictions_rescaled.flatten()})

# Print the forecasted data
print(future_df[['Month', 'Predicted_Target']])

# Step 7: Plot the results
plt.figure(figsize=(10, 6))

# Plot historical data
plt.plot(df['Month'], df['Target'], label='Historical Data', color='blue')

# Plot forecasted data
plt.plot(future_df['Month'], future_df['Predicted_Target'], label='Predicted Data', linestyle='--', color='red')

# Labels and title
plt.xlabel('Month')
plt.ylabel('Target')
plt.title('GRU Time Series Forecast')
plt.legend()

# Show plot
plt.grid(True)
plt.show()
