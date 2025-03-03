# Importing libraries
import pandas as pd
from keras.callbacks import TensorBoard
from keras.optimizers import Adam, SGD
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from matplotlib import pyplot as plt

# Reading data
deathData = pd.read_csv('DeathRate.csv')

# Identifying features and predictor variables associated with the heart data set
x = deathData.iloc[:, 0:13]
y = deathData.iloc[:, 13]

# Split the data set into training and test sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=45)
print(x_train.size)
print(x_train.shape)

# Hyper parameters set 1
# activation_function='relu'
# learning_rate=0.1
# epochs=50
# b_size=256
# decay_rate= learning_rate / epochs
# optimizer = Adam(lr=learning_rate, decay=decay_rate)

# Hyper parameters set 2
activation_function="tanh"
learning_rate=0.3
epochs=100
b_size=32
decay_rate= learning_rate / epochs
optimizer = SGD(lr=learning_rate, decay=decay_rate)

# Creating neural network to perform linear regression
# Model identified to be built
model = Sequential()
# Providing inputs to the first hidden layer
model.add(Dense(25, input_dim=13, activation=activation_function))
# Adding multiple hidden layers
model.add(Dense(15, activation='relu'))
model.add(Dense(255, activation='tanh'))
# Defining the output layer
model.add(Dense(1, activation='softmax'))
# Compiling the model defined
model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

# Fitting the defined model using the training data set
history = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=100, batch_size=b_size, verbose=0, initial_epoch=0)

# Evaluation of the loss and accuracy associated to the test data set
[test_loss, test_acc] = model.evaluate(x_test, y_test)
print("Evaluation result on Test Data : Loss = {}, accuracy = {}".format(test_loss, test_acc))

# Listing all the components of data present in history
print('The data components present in history are', history.history.keys())

# Graphical evaluation of accuracy associated with training and validation data
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Evaluation of Data Accuracy')
plt.xlabel('epoch')
plt.ylabel('Accuracy of Data')
plt.legend(['TrainData', 'ValidationData'], loc='upper right')
plt.show()

# Graphical evaluation of loss associated with training and validation data
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.xlabel('epoch')
plt.ylabel('Loss of Data')
plt.title('Evaluation of Data Loss')
plt.legend(['TrainData', 'ValidationData'], loc='upper right')
plt.show()

# Visualization of the model using tensor board
tbCallBack = TensorBoard(log_dir='./lab2_1', histogram_freq=0, write_graph=True, write_images=True)

# Fitting the model defined using the training data along with validation using test data
history = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=10, verbose=0, initial_epoch=0, callbacks=[tbCallBack])

# Evaluation of the loss and accuracy associated to the test data set
[test_loss, test_acc] = model.evaluate(x_test, y_test)
print("Evaluation result on Test Data using Tensorflow : Loss = {}, accuracy = {}".format(test_loss, test_acc))

# Listing all the components of data present in history
print('The data components present in history using Tensorflow are', history.history.keys())

# Graphical evaluation of accuracy associated with training and validation data
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Evaluation of Data Accuracy using Tensorflow')
plt.xlabel('epoch')
plt.ylabel('Accuracy of Data')
plt.legend(['TrainData', 'ValidationData'], loc='upper right')
plt.show()

# Graphical evaluation of loss associated with training and validation data
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.xlabel('epoch')
plt.ylabel('Loss of Data')
plt.title('Evaluation of Data Loss using Tensorflow')
plt.legend(['TrainData', 'ValidationData'], loc='upper right')
plt.show()