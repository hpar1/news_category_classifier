
# Import necessary libraries

import os
import operator
import numpy as np
import math
import csv
from keras.models import Sequential, Model
from keras.layers import LSTM, BatchNormalization, Dense, SpatialDropout1D, CuDNNLSTM, Reshape
from keras.engine.input_layer import Input
from keras.layers.embeddings import Embedding
from keras.layers.convolutional import Conv1D, Conv2D, Conv3D
from keras.layers.convolutional import MaxPooling1D, MaxPooling2D, MaxPooling3D
from keras.layers.core import Dropout, Lambda
from keras.preprocessing import sequence 
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import optimizers

#Designate hyperparamaters 
article_length = 400
batch_size = 64
epochs = 100
dictionary_size = 10000
embedding_vector_length = 400
input_dimension = int(math.sqrt(article_length))
train_data_path = "data/firstWords/encoded/train/"
test_data_path = "data/firstWords/encoded/test/"
train_data = []
train_label = []
test_data = []
test_label = []
categories = next(os.walk(train_data_path))[1]
num_categories = len(categories)

#Read in pre encoded training articles and assign labels based on parent folder
i = 0 
for folder in categories:
	file_paths = next(os.walk(train_data_path + folder))[2]
	for path in file_paths:
		file = open(train_data_path + folder+ "/" + path, "r")
		words = file.readlines()[0].strip(" ").split(" ")
		if(len(words) < 100):
			continue
		while len(words) < article_length:
			words.append("2")
		words = words[:article_length]
		train_data.append(np.reshape(words,(input_dimension, input_dimension) ))
		new_label = np.zeros(num_categories)
		new_label[i % num_categories] = 1
		train_label.append(new_label)
	i += 1

#Read in pre encoded test articles and assign labels based on parent folder
i = 0
for folder in categories:
	file_paths = next(os.walk(test_data_path + folder))[2]
	for path in file_paths:
		test_file = open(test_data_path + folder+ "/" + path, "r")
		test_words = test_file.readlines()[0].strip(" ").split(" ")
		while len(test_words) < article_length:
			test_words.append("2")
		test_words = test_words[:article_length]
		test_data.append(np.reshape(test_words,(input_dimension, input_dimension) ))
		new_test_label = np.zeros(num_categories)
		new_test_label[i % num_categories] = 1
		test_label.append(new_test_label)
	i += 1


#Convert data into arrays for training and establish random seed
np.random.seed()

max_review_length = article_length
train_data = np.asarray(train_data)
train_label = np.asarray(train_label)
test_data = np.asarray(test_data)
test_label = np.asarray(test_label)





#Create model
inputs = Input((input_dimension,input_dimension))
m = Lambda(lambda x : x)(inputs)
m = Reshape((max_review_length,))(m)
#Embed vectors into vector space
m = Embedding(dictionary_size, embedding_vector_length, input_length=max_review_length)(m)
#1d convolution
m = (Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'))(m)
m = (BatchNormalization())(m)
m = (MaxPooling1D(pool_size=2))(m)
m = (SpatialDropout1D(0.1))(m)
m = (Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'))(m)
m = (BatchNormalization())(m)
m = (MaxPooling1D(pool_size=2))(m)
m = (Dropout(0.1))(m)
#LSTM
m = (CuDNNLSTM(100))(m)
#Softmax(prediction)
outputs = (Dense(num_categories, activation='softmax'))(m)
#Put together model parts
model = Model(inputs = [inputs], outputs = [outputs]) 
#Compile model
model.compile(loss='binary_crossentropy', optimizer=optimizers.SGD(lr=1e-3, momentum=0.9), metrics=['accuracy'])

#Designate output path for model weights
output_path = os.path.basename(__file__).replace('.py', '/')
if not os.path.exists(output_path):
	os.makedirs(output_path)
	os.makedirs(output_path + "history")
#Delete any previous weights left in output directory
for item in next(os.walk(output_path))[2]:
	os.remove(output_path + item)
#Establish checkpointer to save weights by epoch
checkpointer = ModelCheckpoint(output_path + '{epoch:02d}-{val_loss:.2f}.h5', verbose=1, save_best_only=False)
#Train model
model.fit(train_data, train_label, epochs = epochs, batch_size = batch_size, validation_split = 0.2, callbacks = [checkpointer])


#Evaluate model with all recorded weights using test data and record results
scores = {}
history = open(output_path + "history/history.csv", mode = 'w', newline='')
history_writer = csv.writer(history)
history_writer.writerow(["Epoch", "Loss", "Accuracy"])
for weights in next(os.walk(output_path))[2]:
	model.load_weights(output_path + weights)
	score = model.evaluate(x=test_data, y=test_label, batch_size = batch_size, verbose=1)
	scores[weights] = score
	history_writer.writerow([weights[:weights.find('-')], score[0], score[1]])
history.close()
#sort scores
scores = sorted(scores.items(), key=((operator.itemgetter(1))), reverse = False)

#Save top five weights to text file for further use
i = 0
top_five = open(output_path + "history/top5.txt", mode = 'w', newline='')
for score in scores:
	print(score)
	top_five.write(str(score) + '\n')
	if i == 5:
		break;
	i += 1



