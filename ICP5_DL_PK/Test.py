# Import libraries
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from keras.wrappers.scikit_learn import KerasClassifier
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
import re
from sklearn.preprocessing import LabelEncoder

# Read the input data from csv file
data = pd.read_csv('spam.csv')

# Keeping only the necessary columns - cleaning the data set to identify features that are important
data = data[['text','sentiment']]
data['text'] = data['text'].apply(lambda x: x.lower())
data['text'] = data['text'].apply((lambda x: re.sub('[^a-zA-z0-9\s]', '', x)))

for idx, row in data.iterrows():
    row[0] = row[0].replace('rt', ' ')

max_features = 2000
tokenizer = Tokenizer(num_words=max_features, split=' ')
tokenizer.fit_on_texts(data['text'].values)
X = tokenizer.texts_to_sequences(data['text'].values)

X = pad_sequences(X)

# Creating the model to be fit
embed_dim = 128
lstm_out = 196
# Define model used along with the appropriate layers
def createmodel():
    model = Sequential()
    model.add(Embedding(max_features, embed_dim,input_length = X.shape[1]))
    model.add(LSTM(lstm_out, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(3, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])
    return model
# print(model.summary())

# Identify the data into training and test sets
labelencoder = LabelEncoder()
integer_encoded = labelencoder.fit_transform(data['sentiment'])
y = to_categorical(integer_encoded)
X_train, X_test, Y_train, Y_test = train_test_split(X,y, test_size = 0.33, random_state = 42)

# Fitting the training data on the model defined
batch_size = 32
model = createmodel()
history = model.fit(X_train, Y_train, epochs = 1, batch_size=batch_size, verbose = 2, validation_data=(X_test, Y_test))

# Evaluation of the performance of the model fit
score, acc = model.evaluate(X_test, Y_test, verbose=2, batch_size=batch_size)
print('The score obtained from the model fit is ', score)
print('The accuracy of the model fit is ', acc)
print(model.metrics_names)

# Saving the model to be applied on varying test data
modelFit = model.save('modelFit.h5')

# Performing grid search analysis
model = KerasClassifier(build_fn=createmodel, verbose=0)
batch_size = [10, 20, 40]
epochs = [1, 2, 3]
param_grid = dict(batch_size=batch_size, epochs=epochs)
# Import library used to do grid search
from sklearn.model_selection import GridSearchCV
grid = GridSearchCV(estimator=model, param_grid=param_grid)
grid_result = grid.fit(X_train, Y_train)

# Summarize results obtained from the grid search
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))