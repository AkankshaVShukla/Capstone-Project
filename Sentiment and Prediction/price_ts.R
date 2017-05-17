####################################################################
#This method was created by Piyush Choudhary
#Unity ID: pchoudh2
#Description: This file reads data from price_ts.txt and does forecasting
# using arima 
####################################################################

library('rjson')
library('forecast')
json_data <- fromJSON(file='price_ts.txt')
final <- c()
length(json_data)
for(i in {1:length(json_data)}){
  test <- json_data[i]
  #names(test)
  print(i)
  y = auto.arima(unlist(test))
  fore <- forecast(y, h=30)

  
  final[[length(final)+1]] <- list(names(test), mean(fore$mean))
  
}
# final
length(final)
# unlist(final)
new_final <- as.data.frame(t(matrix(unlist(final), ncol=length(final))))
names(new_final)[1] <- 'Listing ID'
names(new_final)[2] <- 'Predicted Price'
# new_final
write.csv(new_final, file = 'PredictedPrice.csv')
# for(i in {1:length(final)}){
#   
# }
# new_final[2,1]