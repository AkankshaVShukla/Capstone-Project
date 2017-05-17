####################################################################
#This file was created by Mihir Mirajkar
#Unity ID:mmmirajk
####################################################################

from sklearn.ensemble import RandomForestClassifier
import pickle
import numpy as np
import csv
import locale
from sklearn.metrics import accuracy_score
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import sys

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

amenities = []

base_price = []

####################################################################
#This method was created by Mihir Mirajkar
#Unity ID:mmmirajk
#Description: This method loads the amenities of existing houses in 
#a set to check which are the unique amenities
####################################################################

def load_amenities():
	f = open('../Data/listings.csv')
	f.next()
	f_csv = csv.reader(f)
	for line in f_csv:
		line = line[58][1:-1].split(',')
		for amenity in line:
			if amenity not in amenities:
				amenities.append(amenity)
	f.close()



####################################################################
#This method was created by Piyush Choudhary
#Unity ID:pchoudh2
#Description: Plots an elbow plot to check which K for kmeans has 
#the lowest SSE
####################################################################

def plot_elbow(base_price1):
	inertia = []
	mini = sys.maxsize
	size =0
	for k in range(1,50):
		print k
		kmeans = KMeans(n_clusters=k).fit(base_price1)
		inertia.append(kmeans.inertia_)

	plt.plot(inertia)
	plt.savefig('1.png')

####################################################################
#This method was created by Mihir Mirajkar
#Unity ID: mmmirajk
#Description: Loads forecasted prices from csv file created using 
#file price_ts.R
####################################################################


forecasted_price = {}

def load_forecasted_price():
	global forecasted_price
	f = open('PredictedPrice.csv')
 	f.next()
 	f_csv = csv.reader(f)
	for line in f_csv:
		id = int(line[1])
		price = float(line[2])
		forecasted_price[id] = price


####################################################################
#This method was created by Mihir Mirajkar
#Unity ID:mmmirajk
#Description: This method uses the forecasted price and creates cluster to
# get labels for predicting the price 
####################################################################

price_range = {}
def load_prices():
	base_price1 = []
	f = open('../Data/listings.csv')
	f.next()
	f_csv = csv.reader(f)
	for line in f_csv:
		id = locale.atoi(line[0])
		price = forecasted_price[id]
		if line[56] != '' and line[56] != '0':
			base_price1.append([price/locale.atoi(line[56])])
		else:
			base_price1.append([price])
	f.close()
	# plot_elbow(base_price1)
	k = 10
	model = KMeans(n_clusters=k, random_state = 0).fit(base_price1)
	# model = MeanShift(bin_seeding=True).fit(base_price1)
	cluster_centers = model.cluster_centers_
	cluster_centers = cluster_centers.tolist()
	labels = model.labels_
	labels = labels.tolist()
	for i in range(len(cluster_centers)):
		temp = []
		for j in range(len(base_price1)):
			if labels[j] == i:
				temp.append(base_price1[j])

		price_range[int(cluster_centers[i][0])] = [min(temp)[0],max(temp)[0], len(temp)]


	for i in range(len(base_price1)):
		base_price.append(int(cluster_centers[labels[i]][0]))

	#rint price_range
	

####################################################################
#This method was created by Mihir Mirajkar
#Unity ID:mmmirajk
#Description: This method normalizes a coloum of numpy Matrix
####################################################################

def normalize_column(A, col):
    A[:,col] = 1*((A[:,col] - np.min(A[:,col])) / (np.max(A[:,col]) - np.min(A[:,col])))


####################################################################
#This method was created by Mihir Mirajkar
#Unity ID:mmmirajk
#Description: creates a feature vector with amenities of the house,
# adds location as a feature also adds review score as a feature 
####################################################################

def form_feature_vec():
	f = open('../Data/listings.csv')
	f.next()
	f_csv = csv.reader(f)
	temp_ame_fea =[]
	for line in f_csv:
		line1 = line[58][1:-1].split(',')
		temp =[]
		for amenity in amenities:
			if amenity in line1:
				temp.append(1)
			else:
				temp.append(0)
		temp.append(locale.atof(line[48]))
		temp.append(abs(locale.atof(line[49])))
		id = locale.atoi(line[0])
		#print id
		temp_id = 1178162

		if id in review_score:
			#print review_score[id]
			temp.append(review_score[id])
		else:
			temp.append(1)
		# print temp[48]
		temp_ame_fea.append(temp)
	
	f.close()
	amenities_fea = np.matrix(temp_ame_fea)
	#np.random.shuffle(amenities_fea)
	#normalize_column(amenities_fea,47)
	#normalize_column(amenities_fea,46)
	#print amenities_fea
	return amenities_fea

####################################################################
#This method was created by Mihir Mirajkar
#Unity ID:mmmirajk
#Description: Loads review scores of each house from review_dict.pkl
####################################################################

review_score = {}
def load_sentiment_score():
	global review_score
	output = open('review_dict.pkl', 'rb')
	review_score  = pickle.load(output)
	# review_score

feature_score = []

def assign_weights():
	for i in range(len(feature_score)):
		amenities_fea[:, i] *= feature_score[i]



####################################################################
#This method was created by Piyush Choudhary
#Unity ID:pchoudh2
#Description: This method plots accuracies of 500 k's to determine 
#with which k we get the best result.
####################################################################


def plot_accuracies():

	accuracies = []
	for k in range(1,1000):
		print k
		acc = train_model(k)
		accuracies.append(acc)
	print 'Max', max(accuracies)
	print accuracies.index(max(accuracies))
	plt.plot(accuracies)
	plt.savefig('2.png')
	return accuracies.index(max(accuracies))


####################################################################
#This method was created by Mihir Mirajkar
#Unity ID:mmmirajk
#Description:This method creates a model using the features from 
#earlier method and calculates the accuracies of predicted price
####################################################################

def train_model(number):
	X_new = SelectKBest(chi2, k=len(amenities)).fit(amenities_fea, base_price)
	feature_score =  X_new.scores_.tolist()
	clf = KNeighborsClassifier(n_neighbors=number, algorithm='brute', n_jobs = 4, weights = 'distance')
	ratio = 0.90
	clf = clf.fit(amenities_fea[:int(len(amenities_fea)*ratio)],base_price[:int(len(base_price)*ratio)] )
	prediction = clf.predict(amenities_fea[int(len(amenities_fea)*ratio):])
	actual_price = base_price[int(len(base_price)*ratio):]
	predict_for_user(clf, feature_score)
	return accuracy_score(prediction, actual_price)


####################################################################
#This method was created by Mihir Mirajkar
#Unity ID:mmmirajk
#Description: This method predicts price for new users and returns 
# a price range to the user.
####################################################################

def predict_for_user(clf, feature_score):
	print "Ammenities available"
	for i in range(len(amenities)):
		print i+1 , amenities[i]
	count = input('Number of features:')
	print 'Enter the number of features'
	amenity_list = []
	i=0
	while i < count:
		try:
			x = int(input())
		except:
			print "Invalid. Please enter a number between 1 and", len(amenities)
		if x>len(amenities) or x<1:
			print "Invalid. Please enter a number between 1 and", len(amenities)
		else:
			amenity_list.append(x-1)
			i += 1

	amenity_list = list(set(amenity_list))
	#print amenity_list
	pred_fea = [0]*(len(amenities))
	for x in amenity_list:
		pred_fea[x] += 1
	#print pred_fea
	try:
		lat = float(input('Enter Latitude:'))
		pred_fea.append(lat)
	except:
		print "Invalid Latitude"
		pred_fea.append(42.0)
	
	try:
		lon = abs(float(input('Enter Longitude:')))
		pred_fea.append(lon)
	except:
		print "Invalid longitude"
		pred_fea.append(71.0)
	
	pred_fea.append(1)


	for i in range(len(pred_fea)):
		pred_fea[i] *= feature_score[i]


	final_price = clf.predict([pred_fea])
	print final_price
	#print price_range[final_price[0]]
	people = input("Enter Number of people that can stay in the room")
	print "Base price of the room should be: $"+str(final_price[0]*people)
	print "For competative pricing the minimum you would want to go is $"+str(price_range[final_price[0]][0]*people)+" The max you can go is $"+str(price_range[final_price[0]][1]*people)
	print price_range[final_price[0]][2],"people have their prices in the same range"
	print "According to our analysis you can keep the price lowest on Tuesday and highest on Saturday"


load_amenities()

load_forecasted_price()

load_prices()

load_sentiment_score()
amenities_fea  = form_feature_vec()

#max_index = plot_accuracies()
print train_model(117)

