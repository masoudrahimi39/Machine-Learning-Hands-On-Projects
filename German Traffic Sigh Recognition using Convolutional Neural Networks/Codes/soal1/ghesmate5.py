import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
import time
#from keras.layers import 
from keras.layers import Activation, SimpleRNN, LSTM, Dropout, GRU
#from keras.optimizers import SGD,adam

def load_data():
    all_data = np.load('polution_dataSet.npy')
    all_data = all_data[:15000, :]
    X = np.copy(all_data[:11, :])
    for i in list(range(12,15000,12)) :
        X = np.concatenate((X, all_data[i:i+11, :].reshape(11, 8)), axis=0)
    Y = np.copy(all_data[11, :]).reshape(1,8)
    for i in list(range(23,15000,12)):
        Y = np.concatenate((Y, all_data[i, :].reshape(1,8)), axis=0)
    Y = np.copy(Y[:, 0]).reshape(1250, 1)
    X_train = np.copy(X[:11000, :])
    Y_train = np.copy(Y[:1000, :])
    X_test = np.copy(X[11000: , :])
    Y_test = np.copy(Y[1000: , :])
    return X_train, Y_train, X_test, Y_test

def load_data_vector():   ###data vector e 88 dar 1 e###data vector e 88 dar 1 e
    all_data = np.load('polution_dataSet.npy')
    all_data = all_data[:15000, :]
    X = np.copy(all_data[:11, :]).reshape(1, 88)
    for i in list(range(12,15000,12)) :
        X = np.concatenate((X, all_data[i:i+11, :].reshape(1, 88)), axis=0)
    Y = np.copy(all_data[11, :]).reshape(1,8)
    for i in list(range(23,15000,12)):
        Y = np.concatenate((Y, all_data[i, :].reshape(1,8)), axis=0)
    Y = np.copy(Y[:, 0]).reshape(1250, 1)
    X_train = np.copy(X[:1000, :])
    Y_train = np.copy(Y[:1000, :])
    X_test = np.copy(X[1000: , :])
    Y_test = np.copy(Y[1000: , :])
    return X_train, Y_train, X_test, Y_test


X_train, Y_train, X_test, Y_test = load_data()
def gru(epoch): 
    X_train, Y_train, X_test, Y_test = load_data()
    X_train = np.reshape(X_train, (int(X_train.shape[0]/11), 11, X_train.shape[1]))
    X_test  = np.reshape(X_test , (int(X_test.shape[0]/11), 11, X_test.shape[1]))
    los = ['mean_squared_error', 'mean_absolute_error']
    opt = ['Adam', 'RMSprop', 'ADAgrad']
    cnt = 0
    for i in range(1):
        for j in range(1):
            cnt+=1
            model = Sequential()
            model.add(GRU(units = 50, input_shape=(11, 8)))
            model.add(Dropout(0.2))
            model.add((Dense(1)))
            model.compile(loss=los[i], optimizer=opt[j])
            begin = time.time()
            history = model.fit(X_train,Y_train,epochs = epoch
                                ,batch_size=12,verbose=2,shuffle=False,
                                validation_data=(X_test, Y_test))
            end = time.time()
            print('GRU learning time(',los[i],'and', opt[j],') is:%0.2f'%(end - begin))
            y_predicted = model.predict(X_test)
            model.summary()
            from math import sqrt
            from sklearn.metrics import mean_squared_error
            error = sqrt(mean_squared_error(Y_test, y_predicted))
            print('RMSE for test data is : %.3f' % error)
            plt.figure('loss')
            plt.subplot(2,3,cnt)
            plt.title('loss:'+los[i]+'/optimizer:'+opt[j])
            plt.plot(history.history['loss'], label='train_loss')
            plt.plot(history.history['val_loss'], label='test_loss')
            plt.legend()
            model.summary()
           # y_predicted = model.predict(X_test)
            plt.figure()
            plt.title('loss:'+los[i]+'/optimizer:'+opt[j])
            plt.plot(y_predicted)
            plt.plot(Y_test)
            plt.legend(['predicted', 'actual'])
            plt.figure()
            plt.plot(history.history['loss'], label='train_loss')
            plt.plot(history.history['val_loss'], label='test_loss')
            plt.title('loss:'+los[i]+'/optimizer:'+opt[j])
            plt.legend()

B=gru(100)
#lstm(2)