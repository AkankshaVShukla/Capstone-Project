####################################################################
#This file was created by Mihir Mirajkar
#Unity ID:mmmirajk
####################################################################

import csv
import sys
import pickle

pwords = []
nwords = []
review_dict = {}
stopwords =[]
listing_score = {}


####################################################################
#This method was created by Mihir Mirajkar
#Unity ID:mmmirajk
#Description: This method loads positive, negative and stop words
#from text files
####################################################################

def load_words():
	f = open('positive.txt')
	for line in f:
		pwords.append(line[:-1])
	f.close()
	f = open('negative.txt')
	for line in f:
		nwords.append(line[:-1])
	f.close()
	f = open('stopwords.txt')
	i=0
	for line in f:
		if i%2 ==0:
			stopwords.append(line[:-1])
		i+=1
	f.close()
	

####################################################################
#This method was created by Mihir Mirajkar
#Unity ID:mmmirajk
#Description: This method loads the reviews of existing houses.
####################################################################

def load_reviews():
	f = open('../Data/reviews.csv')
	f.next()
	f_csv = csv.reader(f)
	for line in f_csv:
		id = int(line[0])
		review = line[5]
		if id not in review_dict:
			review_dict[id] = [review]
		else:
			review_dict[id].append(review)
	#print review_dict[12147973]

####################################################################
#This method was created by Mihir Mirajkar
#Unity ID:mmmirajk
#Description: This method removes stop words from the review passed
####################################################################

def remove_stop_words(s):
	for word in s:
		if word.lower() in stopwords:
			s.remove(word)
	return s

####################################################################
#This method was created by Mihir Mirajkar
#Unity ID:mmmirajk
#Description: This method calculates positive score of the review passed
####################################################################

def pos_score(s):
	if len(s)==0:
		return 0
	count = 0
	for word in s:
		if word.lower() in pwords:
			count += 1
	return float(count)/len(s)

####################################################################
#This method was created by Mihir Mirajkar
#Unity ID:mmmirajk
#Description: This method calculates negative score of the review passed
####################################################################

def neg_score(s):
	if len(s)==0:
		return 0
	count = 0
	for word in s:
		if word.lower() in nwords:
			count += 1

	return float(count)/len(s)

####################################################################
#This method was created by Mihir Mirajkar
#Unity ID:mmmirajk
#Description: This method calculates the score of of each review and
# stores in a pickle file.
####################################################################

review_score = []
def calc_score():
	neg_count =0
	pos_count =0
	total = 68276
	count = 0
	pos_count =0
	neg_count =0
	for id in review_dict.keys():

		pos_count =0
		neg_count =0
		for review in review_dict[id]:
			review = review.split()
			count += 1
			if count%682 == 0:
				print count/682
			#print review
			review = remove_stop_words(review)
			#print review
			pos = pos_score(review)
			neg = neg_score(review)
			score =pos-neg
			if	score>0:
				pos_count += 1
			else:
				neg_count += 1

		listing_score[id] = (float(pos_count-neg_count)/float(pos_count+neg_count))+1
		review_score.append([pos_count-neg_count, id])

	#print listing_score
	output = open('review_dict.pkl', 'ab+')
	pickle.dump(listing_score, output)
	output.close()
	return listing_score

def main():
	load_words()
	load_reviews()
	calc_score()

main()
