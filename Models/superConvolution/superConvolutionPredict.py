
# LSTM for sequence classification in the IMDB dataset

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


article_length = 400
batch_size = 64
epochs = 100
input_dimension = int(math.sqrt(article_length))
train_data_path = "../../data/firstWords/encoded/train/"
test_data_path = "../../data/firstWords/encoded/NYtest/"
train_data = []
train_label = []
test_data = []
test_label = []
categories = next(os.walk(train_data_path))[1]
num_categories = len(categories)
i = 0 
for folder in categories:
	print(folder)
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

i = 0
for folder in categories:
	print(folder)
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



np.random.seed()
top_words = 10000
max_review_length = article_length
train_data = np.asarray(train_data)
train_label = np.asarray(train_label)
test_data = np.asarray(test_data)
test_label = np.asarray(test_label)

# train_data = sequence.pad_sequences(train_data, maxlen = max_review_length)
#print(np.asarray(train_data))
# print(X_train)
# print("\n\n myData \n\n")
# print(np.asarray(train_data))

embedding_vector_length = 400


inputs = Input((input_dimension,input_dimension))
m = Lambda(lambda x : x)(inputs)
m = Reshape((max_review_length,))(m)
m = Embedding(top_words, embedding_vector_length, input_length=max_review_length)(m)
m = Reshape((input_dimension,input_dimension,embedding_vector_length,))(m)

m = Conv2D(filters = embedding_vector_length, kernel_size = (3,3),padding='same',  activation='relu')(m)
m = Conv2D(filters = embedding_vector_length, kernel_size = (3,3),padding='same',  activation='relu')(m)
m = MaxPooling2D((2, 2))(m)
m = Conv2D(filters = embedding_vector_length, kernel_size = (3,3),padding='same',  activation='relu')(m)
m = Conv2D(filters = embedding_vector_length, kernel_size = (3,3),padding='same',  activation='relu')(m)
m = MaxPooling2D((2, 2))(m)
m = Reshape((int((input_dimension / 4)**2),embedding_vector_length,))(m)
m = (Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'))(m)
m = (BatchNormalization())(m)
m = (MaxPooling1D(pool_size=2))(m)
m = (SpatialDropout1D(0.1))(m)
m = (Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'))(m)
m = (BatchNormalization())(m)
m = (MaxPooling1D(pool_size=2))(m)
m = (Dropout(0.1))(m)
m = (CuDNNLSTM(100))(m)
outputs = (Dense(num_categories, activation='softmax'))(m)
model = Model(inputs = [inputs], outputs = [outputs]) 
model.compile(loss='binary_crossentropy', optimizer=optimizers.SGD(lr=1e-3, momentum=0.9), metrics=['accuracy'])
print(model.output_shape)
output_path = "weights/"
if not os.path.exists(output_path):
	os.makedirs(output_path)
	os.makedirs(output_path + "history")
# checkpointer = ModelCheckpoint(output_path + '{epoch:02d}-{val_loss:.2f}.h5', verbose=1, save_best_only=False)
# model.fit(train_data, train_label, epochs = epochs, batch_size = batch_size, validation_split = 0.2, callbacks = [checkpointer])

for weight in next(os.walk(output_path))[2]:
	print(weight)
	model.load_weights(output_path + weight)
	score = model.evaluate(x=test_data, y=test_label, batch_size = batch_size, verbose=1)
	print(score)




