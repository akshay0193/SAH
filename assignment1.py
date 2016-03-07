import pandas as pd
import copy
import numpy as np
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from collections import Counter
from nltk import FreqDist
import csv
import nltk
import operator
from nltk.tokenize import RegexpTokenizer

#f = open("/Users/akshayagarwal/myDesktop/Programming/SAH/Assignment_I-2/gatech_Subreddit_Posts.txt")
#print f.read()
#print type(f.read())
class assignment1_Part1:
	def __init__(self,filename):
		self.data = pd.read_csv(filename,names=['post_id','timestamp','username','post_title','post_body'],sep="	",header=None,parse_dates=[1])


	def part1(self):
		
		#print data
		#data.columns("post_id","timestamp","username","post_title","post_body")
		data_new = copy.deepcopy(self.data)
		for x in range(0,len(data_new)):
			data_new[:]['timestamp'][x] = (data_new[:]['timestamp'][x]).date()

		#print data_new[:]['timestamp']


		print data_new.groupby('timestamp').count()
		print "&&&&&&&&"

		data_new.sort('timestamp')

		data_uniqueUsersDay = data_new.groupby('timestamp').agg({"username":pd.Series.nunique})
		#print data_uniqueUsersDay

		ax = data_uniqueUsersDay.plot(title="Unique Users per Day", fontsize=12, legend=False)
		ax.set_xlabel("Date")
		ax.set_ylabel("Unique Users")
		#ax.label.set_visible(False)
		#plt.show()
		#print type(data[:][1])
		#list_A = data[:][1].tolist()
		#print type(list_A[0])
		#print len(data_uniqueUsersDay)

		data_postCount = (data_new.groupby('timestamp').count())
		data_postCount1 = data_postCount[:]['post_id']
		ay = data_postCount1.plot(title="No.of posts per day", fontsize=12)
		ay.set_ylabel("No.of posts")
		ay.set_xlabel("Date")
		#plt.show()

		

	def mean_stdDeviation(self):
		list_count_postTitles = []
		list_postTitles = self.data[:]['post_body'].tolist()
		#tokenizer = RegexpTokenizer(r'\w+')

		for x in list_postTitles:
			list_count_postTitles.append(len(x.split()))
		#print list_count_postTitles
		npArray = np.asarray(list_count_postTitles)
		#print npArray.mean()
		#print npArray.std()
		return [npArray.mean(),npArray.std(),list_postTitles,list_count_postTitles]

	def nGramCalculation(self):
		mean, std, list_postBody, list_count_postBody = self.mean_stdDeviation()
		#stop word removal
		list_words_GreaterMean = []
		list_words_LesserMean = []
		for index in range(0,len(list_count_postBody)):
			if list_count_postBody[index]>mean:
				list_words_GreaterMean.append(list_postBody[index])
			elif list_count_postBody[index]<mean:
				list_words_LesserMean.append(list_postBody[index])

		#self.uniGramCalculation(list_words_GreaterMean)	#calculate for lesser mean
		self.nGramsBi(list_words_GreaterMean,True)


	def uniGramCalculation(self,listAB):
		list_words = copy.deepcopy(listAB)
		tokenizer = RegexpTokenizer(r'\w+')
		for sentence in listAB:		#splitting every post in individual words
			list_words += tokenizer.tokenize(sentence)

		for index in range(0,len(list_words)):
			list_words[index] = list_words[index].upper()

		#print list_words[0:20]

		list_words_stopRemoved=[]
		stopwords_mine = []
		#a.encode('ascii','ignore')
		stopwords_mine+= (word.encode('ascii','ignore') for word in stopwords.words('english'))
		#print type(stopwords_mine[0])
		#print type(list_words[0])
		list_words_stopRemoved += (word for word in list_words if word.lower() not in stopwords_mine)

		#print len(list_words_stopRemoved)

		fDist = FreqDist(list_words_stopRemoved)
		print type(fDist)
		#raw_input()
		#stringA = (" ").join(list_words_stopRemoved)

		#print stringA
		#fDist = FreqDist(stringA)
		list_mostFreq = fDist.most_common(27)		#top 25 unigrams
		new_list_term_rawFreq_normalizedFreq = []
		for index,item in enumerate(list_mostFreq):
			new_list_term_rawFreq_normalizedFreq.append([item[0],item[1],item[1]/float(list_mostFreq[0][1])])

		with open('csv2.csv','a') as testfile:
			csv_writer = csv.writer(testfile)
			for index in range(len(new_list_term_rawFreq_normalizedFreq[0])):
				csv_writer.writerow([x[index] for x in new_list_term_rawFreq_normalizedFreq])



		#print new_list_term_rawFreq_normalizedFreq

		#new_list_term_rawFreq_normalizedFreq_DataFrame = pd.Series(new_list_term_rawFreq_normalizedFreq)
		#print new_list_term_rawFreq_normalizedFreq_DataFrame

		#new_list_term_rawFreq_normalizedFreq_DataFrame.to_csv(path="csv1.csv")


		#dictionary_unigram = {}
		
		#for word in list_words_stopRemoved:
		#	if word not in dictionary_unigram.keys():
		#		dictionary_unigram[word] = 1
		#	else:
		#		dictionary_unigram[word] += 1


		#print dictionary_unigram.most_common(25)
	def nGramsBi(self,listAB,stopWordInstruction):

		stopwords_mine = []
		#a.encode('ascii','ignore')
		stopwords_mine+= (word.encode('ascii','ignore') for word in stopwords.words('english'))
		tokenizer = RegexpTokenizer(r'\w+')
		tokenized_list = []
		for item in listAB:
			tokenized_list.append(tokenizer.tokenize(item))

		#print tokenized_list[0]
		#print listAB[0]	

		new_list_tokenized = []

		if stopWordInstruction==True:
			for item in tokenized_list:
				temp = []
				temp += (word for word in item if word.lower() not in stopwords_mine)
				#print temp
				#raw_input()
				new_list_tokenized.append(temp)
		else:
			new_list_tokenized=copy.deepcopy(tokenized_list)

		print new_list_tokenized[0]

		gram_dict = {}

		#for item in new_list_tokenized
		new_list_biGrams = []
		for item in new_list_tokenized:
			#print item
			new_list_biGrams += nltk.bigrams(item)
			#print list(temp)
			#raw_input("Press")
			# for value in temp:
			# 	print value
			# 	#raw_input("Press Enter")
			# 	if value not in gram_dict.keys():
			# 		gram_dict[value] = 1
			# 	else:
			# 		gram_dict[value] += 1
		print len(new_list_biGrams)
		print type(new_list_biGrams)
		print new_list_biGrams[0]

		for value in new_list_biGrams:
			#print value
			#raw_input("Press Enter")
			if value not in gram_dict.keys():
				gram_dict[value] = 1
			else:
				gram_dict[value] += 1

		# list_mostFreq = new.most_common(27)


		final_list_sorted =sorted(gram_dict.items(), key=operator.itemgetter(1), reverse = True)  
		counter = 0

		new_list_term_rawFreq_normalizedFreq = []
		for index,item in enumerate(final_list_sorted):
			new_list_term_rawFreq_normalizedFreq.append([item[0],item[1],item[1]/float(final_list_sorted[0][1])])

		with open('csv2.csv','a') as testfile:
			csv_writer = csv.writer(testfile)
			for index in range(len(new_list_term_rawFreq_normalizedFreq[0])):
				if counter<25:
					csv_writer.writerow([x[index] for x in new_list_term_rawFreq_normalizedFreq])
				counter+=1
		#raw_input()
		#for x in sorted_output.keys():
			#while counter<25:
				#counter+=1
				#print sorted_output[x]
		# for x in range(0,len(sorted_output)):
		# 	while x<25:
		# 		print sorted_output[x]

	def nGramsTri(self,listAB,stopWordInstruction):

		stopwords_mine = []
		#a.encode('ascii','ignore')
		stopwords_mine+= (word.encode('ascii','ignore') for word in stopwords.words('english'))
		tokenizer = RegexpTokenizer(r'\w+')
		tokenized_list = []
		for item in listAB:
			tokenized_list.append(tokenizer.tokenize(item))

		#print tokenized_list[0]
		#print listAB[0]	

		new_list_tokenized = []

		if stopWordInstruction==True:
			for item in tokenized_list:
				temp = []
				temp += (word for word in item if word.lower() not in stopwords_mine)
				#print temp
				#raw_input()
				new_list_tokenized.append(temp)
		else:
			new_list_tokenized=copy.deepcopy(tokenized_list)

		print new_list_tokenized[0]

		gram_dict = {}

		#for item in new_list_tokenized
		new_list_biGrams = []
		for item in new_list_tokenized:
			#print item
			new_list_biGrams += nltk.trigrams(item)
			#print list(temp)
			#raw_input("Press")
			# for value in temp:
			# 	print value
			# 	#raw_input("Press Enter")
			# 	if value not in gram_dict.keys():
			# 		gram_dict[value] = 1
			# 	else:
			# 		gram_dict[value] += 1
		print len(new_list_biGrams)
		print type(new_list_biGrams)
		print new_list_biGrams[0]

		for value in new_list_biGrams:
			#print value
			#raw_input("Press Enter")
			if value not in gram_dict.keys():
				gram_dict[value] = 1
			else:
				gram_dict[value] += 1

		# list_mostFreq = new.most_common(27)


		final_list_sorted =sorted(gram_dict.items(), key=operator.itemgetter(1), reverse = True)  
		counter = 0

		new_list_term_rawFreq_normalizedFreq = []
		for index,item in enumerate(final_list_sorted):
			new_list_term_rawFreq_normalizedFreq.append([item[0],item[1],item[1]/float(final_list_sorted[0][1])])

		with open('csv2.csv','a') as testfile:
			csv_writer = csv.writer(testfile)
			for index in range(len(new_list_term_rawFreq_normalizedFreq[0])):
				if counter<25:
					csv_writer.writerow([x[index] for x in new_list_term_rawFreq_normalizedFreq])
				counter+=1
		#raw_input()
		#for x in sorted_output.keys():
			#while counter<25:
				#counter+=1
				#print sorted_output[x]
		# for x in range(0,len(sorted_output)):
		# 	while x<25:
		# 		print sorted_output[x]
  






		

if __name__=="__main__":
	filename = '/Users/akshayagarwal/myDesktop/Programming/SAH/Assignment_I-2/gatech_Subreddit_Posts.txt'
	object1 = assignment1_Part1(filename)
	object1.nGramCalculation()

