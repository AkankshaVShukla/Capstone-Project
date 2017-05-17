# Airbnb Reccomendation System

Submitted By:
1. Piyush Choudhary(pchoudh2)
2. Mihir Mirajkar(mmmirajk)
3. Akanksha Shukla(apshukla)


There are 4 main components in this project:
1. Time series Daily Average price forecasting by Akansha Shukla
2. Sentiment Analysis for each listing by Mihir Mirajkar
3. Time series forecasting for each house by Piyush Choudhary
4. Model Creation, accuracy calculation and prediction for new users by Mihir Mirajkar

Part 1: Time series Daily Average price forecasting
   Run Capstone.py file in Time Series Forecasting folder. This will create file daily_price.csv which is in same folder.

	Command to run  this python file:	
	python Capstone.py

   Run PriceForecastingARIMA.R file which will load daily_price.csv having time series data and forecast price of the houses.

Part 2: Sentiment Analysis for each listing:
   Run the sentiment.py file in Sentiment and Prediction. This file analyses all the sentiment scores using positive.txt, negative.txt and stopwords.txt for each listing and stores it in a pickle file
   
Part 3: Time series forecasting for each house:
   Run the timeseries.py file in Sentiment and Prediction. This will create a csv file(price_ts.txt), This is a cleaned version of calender.csv. Then run price_ts.R which creates price_ts.txt which has the average of one month of forecasted price for each house.
   
Part 4: Model Creation, accuracy calculation and prediction for new users:
   This part uses the sentiment scores from part 2 as a features with amenities as other features and forecasted price from part3 as the label for each house, creates a model for predicting prices of test cases and new users. Run pricepred.py file in Sentiment and Prediction, add the which amenities are present in the house you want to rent and the location of the house in latitude and longitude, this will return a price which your house should be listed with minimum and maximum price at which can be given to the house to get the maximum chance of house getting rented. This will also return on which day of the week should the price of the house be highest and lowest based on analysis from part 1 for the most competative pricing. 

Installation for python:
1. pip install matplotlib
2. pip install sklearn
3. pip install pickle
4. pip install locale

Installation for R:
1. install.packages("rjson")
2. install.packages("forecast")
