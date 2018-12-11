#Bag of words encoding

import os
import operator
word_limit = 10000


raw_path = "data/firstWords/unencoded/train/"
encoded_path = "data/firstWords/encoded/train/"
allWords = {}

for folder_path in next(os.walk(raw_path))[1]:
	files = next(os.walk(raw_path + folder_path))[2]
	
	for path in files:
		file = open(raw_path + folder_path + "/" + path,"r")
		line = file.readline()
		while not line == "" :	
			line = line.split(" ")
			for word in line:
				word = word.replace(",","").replace(".","").replace("?","").replace("!","")
				if word in allWords and not word == "":
					allWords[word] += 1
				elif not word == "":
					allWords[word] = 1
			line = file.readline()
		file.close()
ordered = sorted(allWords.items(), key=operator.itemgetter(1), reverse = True)


outFile = open("Count.txt", "w")

for word in ordered:
	outFile.write(str(word) + "\n")
outFile.close()
i = 3
outFile = open("Dictionary.txt", "w")
for word in ordered:
	outFile.write(word[0] + "," + str(i) + "\n")
	i += 1
	if(i > word_limit):
		break
outFile.write("\n\n" + str(len(ordered) - word_limit) + " words ignored")
outFile.close()


i = 3
encoding = {}
for word in ordered:
	encoding[word[0]] = i
	i += 1	
	if(i > word_limit):
		break



for folder_path in next(os.walk(raw_path))[1]:
	if not os.path.exists(encoded_path + folder_path + '/'):
		os.makedirs(encoded_path +  folder_path + '/')
	files = next(os.walk(raw_path + folder_path))[2]
	for path in files:
		file = open(raw_path + folder_path + "/" + path,"r")
		newFile = open(encoded_path + folder_path + "/" + path + "_encoded", "w")
		line = file.readline()
		while not line == "" :	
			line = line.split(" ")
			for word in line:
				word = word.replace(",","").replace(".","").replace("?","").replace("!","")
				if not word == "":
					if word in encoding:
						newFile.write(str(encoding[word]) + " ")
					else:
						newFile.write(str(2) + " ")

			line = file.readline()
		file.close()
		newFile.close()




