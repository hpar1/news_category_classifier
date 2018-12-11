
# LSTM for sequence classification in the IMDB dataset

import os
import operator
import numpy as np
import math
import csv
import sys
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

file = open('Dictionary.txt', mode = 'r')
lines = file.readlines()
output = (x.replace("\n",'').split(",") for x in lines)
encoding = {}
x = next(output)
while not (x) == ['']:
	encoding[x[0]] = x[1]
	x = next(output)
file.close()



article_path = sys.argv[1]
file = open(article_path, mode='r', encoding='utf8')
reading = file.readlines()
lines = ''
for line in reading:
	lines += line

words = lines.replace('\n',' ').replace('"', '').replace("'",'').replace(",",'').replace(".",'').replace("?",'').replace("!",'').lower().strip(" ").replace("—",'').replace("-",'').split(" ")
words = words[:article_length]

for i in range(len(words)):
	try:
		words[i] = str(encoding[words[i]])
	except KeyError as e:
		words[i] = "2"
while len(words) < article_length:
			words.append('2')
article = np.expand_dims(np.reshape(np.asarray(words),(input_dimension, input_dimension)), axis = 0)
num_categories = 3



np.random.seed()
top_words = 10000
embedding_vector_length = 400


inputs = Input((input_dimension,input_dimension))
m = Lambda(lambda x : x)(inputs)
m = Reshape((article_length,))(m)
m = Embedding(top_words, embedding_vector_length, input_length=article_length)(m)
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
model.load_weights('weights/56-0.21.h5')

prediction = model.predict(article)
print(prediction)
prediction = prediction[0]
category = max(prediction)

if category == prediction[0]:
	message = "health"
elif category == prediction[1]:
	message = "politics"
elif category == prediction[2]:
	message = "tech"

print("article is about " + message)

