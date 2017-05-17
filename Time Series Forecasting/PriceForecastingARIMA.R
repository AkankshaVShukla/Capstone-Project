library(forecast)

dataset= read.csv(file="daily_price.csv",header=TRUE, sep=",")
pt = as.ts(dataset)
plot(pt, main= "Average Price")
dif= diff(pt, differences=1)
plot(dif, main="Average Price")
acf(dif, lag.max=10, main= "ACF")
pacf(dif, lag.max=10, main= "PACF")
auto.arima(dif)
fit <- arima(dif, order=c(3,0,2))
fit
res <- residuals(fit)
Box.test(res, lag = 10, type='Ljung-Box')
#data:  res
#X-squared = 2.5549, df = 10, p-value = 0.2782
#We fail to reject null hypothesis. This is a good fit

#Forecast using ARMA Model
forecast_data <- forecast(fit,h=20)
plot(forecast_data)
