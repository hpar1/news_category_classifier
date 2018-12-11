#Even out dataset
import os
import operator

data_path = "data/firstWords/encoded5000/train/"
overflow_path = "data/firstWords/encoded5000/overflow/"

categories = next(os.walk(data_path))[1]
counts = {}
minCount = 9999999999
for catgory in categories:
	file_count = len(next(os.walk(data_path + catgory))[2])
	counts[catgory] = file_count
	if file_count < minCount:
		minCount = file_count



for catgory in categories:
	files = next(os.walk(data_path + catgory))[2]
	i = 0
	for file in files:
		if i < minCount:
			i += 1
		else:
			if not os.path.exists(overflow_path + catgory):
				os.makedirs(overflow_path + catgory)
			os.rename(data_path + catgory + '/' + file, overflow_path + catgory + '/' + file )