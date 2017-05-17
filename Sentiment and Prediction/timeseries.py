import csv
import locale
import sys
import json
####################################################################
#This File was created by Piyush Choudhary
#Unity ID: pchoudh2
####################################################################
base_price1 = {}
def load_base_prices():
	
	f = open('../Data/listings.csv')
	f.next()
	f_csv = csv.reader(f)
	for line in f_csv:
		line[60] = line[60].replace(",","") 
		id = int(line[0])
		if line[56] != '' and line[56] != '0':
			base_price1[id]= [locale.atof(line[60][1:-3]),locale.atoi(line[56])]
		else:
			base_price1[id] = [locale.atof(line[60][1:-3]),1]
	f.close()

####################################################################
#This method was created by Piyush Choudhary
#Unity ID: pchoudh2
#Description: This method pulls data from calender.csv to stores it 
#in a dictionary 
####################################################################

price_ts = {}
def load_price_ts():
	f = open('../Data/calendar.csv')
	f.next()
	f_csv = csv.reader(f)
	for line in f_csv:
		id = int(line[0])
		#print id,line
		if line[3] != '':
			line[3] = line[3].replace(",","")
		if id not in price_ts:
			if line[3] == '':
				temp_price = float(base_price1[id][0])/float(base_price1[id][1])
				price_ts[id] = [temp_price]
			else:
				price_ts[id] = [locale.atof(line[3][1:])/float(base_price1[id][1])]
		elif line[3]=='':
			price_ts[id].append(price_ts[id][-1])
		else :
			price_ts[id].append(locale.atof(line[3][1:])/float(base_price1[id][1]))


load_base_prices()
load_price_ts()

json.dump(price_ts, open('price_ts.txt','w'))