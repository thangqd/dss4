from datetime import datetime
import math
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from keras import backend as K
import matplotlib
matplotlib.use('TkAgg')
import streamlit as st

# Calculate DSS1
def dss4_preprocessing (input, selected_column):
    ######### remove NULL value   
    df = pd.read_csv(input,encoding = "UTF-8") # depend on exisitng dss4.csv file
    df["Datetime"] =  pd.to_datetime(df["Datetime"],dayfirst=True)
    df.set_index('Datetime', inplace=True)

    print('Before processing: ', len(df)) 
    # print('Before remove NULL values', len(df)) 
    df = df.dropna(subset=[selected_column]) 
    print('After remove NULL values', len(df)) 
   
    ######### Detect and delete outliers of S1
    Q1 = df[selected_column].quantile(0.25)
    Q3 = df[selected_column].quantile(0.75)
    IQR = Q3 - Q1
    # identify outliers
    threshold = 1.5
    outliers = df[(df[selected_column] < Q1 - threshold * IQR) | (df[selected_column] > Q3 + threshold * IQR)]
    # print ('outliers: ', outliers)
    df = df.drop(outliers.index)
    # print('After remove NULL values', len(df))

    print('After remove outliers: ', len(df))
    print('Statistics of processed data:')  
    print(df[selected_column].describe())  
    # df['S1'] = np.log(df['S1'])
    return df

# def create_sequences(data, sequence_length):
    # X, y = [], []
    # for i in range(len(data) - sequence_length):
    #     X.append(data[i:(i + sequence_length)])
    #     y.append(data[i + sequence_length])
    # return np.array(X), np.array(y)
def split_sequence(sequence, n_steps):
    X, y = list(), list()
    for i in range(len(sequence)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the sequence
        if end_ix > len(sequence)-1:
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)



def dss4_lstm_old(df):
    selected_columns = ['S1']  # Replace with your actual column names

    # Filter the DataFrame to include only the selected columns
    df = df[selected_columns]

    # Data preprocessing
    # scaler = MinMaxScaler(feature_range=(0, 1))
    scaler = MinMaxScaler(feature_range=(0, 1))
    df = scaler.fit_transform(df)
    
    # Data preprocessing
    # scaler = MinMaxScaler(feature_range=(0, 1))
    # scaled_data = scaler.fit_transform(df)

    # Hyperparameters
    n_steps = 12
    epochs = 50
    batch_size = 32

    # Create sequences
    X, y = split_sequence(df, n_steps)
    for i in range(len(X)):
        print(X[i], y[i])
      
    # Split the data into training and testing sets
    train_size = int(len(X) * 0.8)
    x_train, x_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(LSTM(units=50))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)

    # Make predictions on the test set
    predictions = model.predict(x_test)

    # Inverse transform the predictions and actual values to the original scale
    # predictions = scaler.inverse_transform(predictions)
    # y_test = scaler.inverse_transform(y_test.reshape(-1, 1))

    # Calculate and print the Mean Squared Error
    # mse = mean_squared_error(y_test, predictions)
    # print(f'Mean Squared Error: {mse}')

    # Plot the actual vs. predicted values
    # fig, ax = plt.subplots(figsize=(12, 6))
    # ax.plot(df.index[-len(y_test):], y_test, label='Actual')
    # ax.plot(df.index[-len(predictions):], predictions, label='Predicted')
    # ax.legend()
    # ax.set_title('Time Series Forecasting with LSTM')
    # # Display the plot in Streamlit
    # st.pyplot(fig)
    return predictions

def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)

def dss4_lstm(df):
    # Reference: https://github.com/huevosabio/ts-predict/blob/master/TS%20Forecasting%20Single-Step%20LSTM%20RNN.ipynb
    selected_columns = ['S1']  # Replace with your actual column names
    # Filter the DataFrame to include only the selected columns
    df = df[selected_columns]
    # Data preprocessing
    # scaler = MinMaxScaler(feature_range=(0, 1))
    scaler = MinMaxScaler(feature_range=(0, 1))
    df = scaler.fit_transform(df)

    # split into train and test sets
    train_size = int(len(df) * 0.67)
    test_size = len(df) - train_size
    train, test = df[0:train_size,:], df[train_size:len(df),:]
    # convert an array of values into a dataset matrix
    # reshapes the data into input and output matrices (X and Y respectively)
    look_back = 3
    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)
    # reshape input to be [samples, time steps, features]
    trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
    model = Sequential()
    model.add(LSTM(4, input_shape=(1, look_back)))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    # model.fit(trainX, trainY, epochs=5, batch_size=1, verbose=2)
    for i in range(10):
        model.fit(trainX, trainY, epochs=1, batch_size=1, verbose=2)
    ## make predictions
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)
    # invert predictions
    trainPredict = scaler.inverse_transform(trainPredict)
    trainY = scaler.inverse_transform([trainY])
    testPredict = scaler.inverse_transform(testPredict)
    testY = scaler.inverse_transform([testY])
    # calculate root mean squared error
    trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
    print('Train Score: %.2f RMSE' % (trainScore))
    testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
    print('Test Score: %.2f RMSE' % (testScore))

    # shift train predictions for plotting
    trainPredictPlot = np.empty_like(df)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict
    # shift test predictions for plotting
    testPredictPlot = np.empty_like(df)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(trainPredict)+(look_back*2)+1:len(df)-1, :] = testPredict
    K.clear_session()
    return trainScore, testScore, scaler.inverse_transform(df[train_size+1:]), trainPredict, testPredict



def dss4_final (input, status_callback):
    i = 0
    steps =2   
    df = dss4_preprocessing (input,'S1')
    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Preprocessing Data'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label) 

    trainScore, testScore, Train,trainPredict, testPredict = dss4_lstm(df)
    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Running LSTM forecast'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label) 

    return trainScore, testScore, Train, trainPredict, testPredict