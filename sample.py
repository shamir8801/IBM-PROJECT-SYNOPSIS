import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense
from tensorflow.keras.optimizers import Adam
from datetime import datetime
# Example lists (replace these with your actual lists)
months_list = ['2022-01', '2022-02', '2022-03', '2022-04', '2022-05', '2022-06', '2022-07', '2022-08', '2022-09', '2022-10', '2022-11', '2022-12']
target_list = [15, 18, 16, 20, 22, 19, 23, 21, 24, 25, 22, 27]  # Replace with your actual target values (discrete)
def forecast_inventory(months_list,target_list):
    # Convert month strings to datetime
    months = pd.to_datetime(months_list, format='%Y-%m')

    # Create a DataFrame from the lists
    df = pd.DataFrame({'Month': months, 'Target': target_list})

    # Feature engineering: Extract month and year from the 'Month' column
    df['Month_num'] = df['Month'].dt.month  # Month number (1-12)
    df['Year'] = df['Month'].dt.year  # Year

    # Normalize the target values
    scaler = MinMaxScaler(feature_range=(0, 1))
    df['Target_scaled'] = scaler.fit_transform(df['Target'].values.reshape(-1, 1))

    # Prepare data for GRU: We will create sequences of 1 step
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

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Build the GRU model
    model = Sequential()
    model.add(GRU(units=50, return_sequences=False, input_shape=(X_train.shape[1], 1)))
    model.add(Dense(units=1))

    # Compile the model
    model.compile(optimizer=Adam(), loss='mean_squared_error')

    # Train the model
    model.fit(X, y, epochs=50, batch_size=1, verbose=2)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Rescale the predictions and actual values back to the original scale
    y_pred_rescaled = scaler.inverse_transform(y_pred)
    y_test_rescaled = scaler.inverse_transform(y_test.reshape(-1, 1))

    # Evaluate the performance (mean squared error for continuous targets)
    mse = np.mean((y_pred_rescaled - y_test_rescaled) ** 2)
    print(f'Mean Squared Error on test set: {mse:.2f}')

    # Forecasting the next 12 months (based on the last known value)
    # We'll use the last value from the training set to start forecasting
    last_sequence = df['Target_scaled'].values[-time_step:].reshape(1, time_step, 1)

    future_predictions = []
    for _ in range(12):  # Forecast 12 months ahead
        next_pred = model.predict(last_sequence)
        future_predictions.append(next_pred[0, 0])
        last_sequence = np.append(last_sequence[:, 1:, :], next_pred.reshape(1, 1, 1), axis=1)

    # Rescale the forecasted values back to the original scale
    future_predictions_rescaled = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

    # Prepare a DataFrame for the forecasted future months
    future_months = pd.date_range(start=str(int(datetime.now().strftime("%Y"))+1)+'-01-01', periods=12, freq='M')
    future_df = pd.DataFrame({'Month': future_months, 'Predicted_Target': future_predictions_rescaled.flatten()})

    # Print the forecasted data
    print(future_df[['Month', 'Predicted_Target']])
    print(type(future_df))

    list_of_lists = future_df.values.tolist()
    oplist=[]
    for i in list_of_lists:
        oplist.append(float(str(i[1]).split("e")[0]))
    print(oplist)
    print(months_list,target_list)
    return oplist