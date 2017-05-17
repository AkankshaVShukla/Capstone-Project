####################################################################
#This method was created by Mihir Mirajkar
#Unity ID:mmmirajk
#Description: This file is just for exploration of data, it shows
#which houses are occipied for 98% of the year and which ones are free 
#for 98% of the year.
####################################################################
import csv
mydict = dict()
myset = set()
file = open("calendar.csv", "r") 
i =0
for line in file: 
	if i==0:
		i=1
		continue
	if i%10000==0:
		print(i)
	line = line.split(",")
	line[0] = int(line[0])
	if line[0] not in mydict:
		mydict[line[0]] = [line[2]]
	else:
		mydict[line[0]].append(line[2])

	myset.add(line[0])
	i+=1
Avail = dict()
for key in mydict.keys():
	mylist = mydict[key]
	true = 0
	false = 0
	for t in mylist:
		if t =='t':
			true += 1
		else:
			false += 1
	Avail[key] = (true/(true+false))*100
mostpop = []
mostunpop = []
for key in Avail.keys():
	if Avail[key]>98:
		mostpop.append(key)
	elif Avail[key]<2:
		mostunpop.append(key)

print("####################Most Popular####################\n",mostpop,len(mostpop),len(mostpop)*100/len(Avail))
print("####################Most Unpopular####################\n",mostunpop,len(mostunpop),len(mostunpop)*100/len(Avail))
print(len(Avail))