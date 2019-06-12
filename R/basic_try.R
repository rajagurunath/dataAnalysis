library(data.table)
library(tidyverse)

library(ggplot2)
df=fread("D:\\experiments\\data\\Research_data\\ochctp\\pivoted_ochctp.csv")


set.seed(15)
a = c(1,2,-2,4,2,3,1,0,3,4,2,3,1)
b = a + rnorm(length(a), sd = 0.4)
plot(ts(b), col="#f44e2e", lwd=3)
corr = ccf(a,b)
points(a, col="#27ccc0", lwd=3)
points(b,col="red",lwd=2)
corr
df$performance_metrics.ts
dev1=df[df$performance_metrics.module=='13-L1-10']

plot(ts(dev1$BerPostFecAve))

dev1$

dev2=na.omit(dev1$BerPostFecAve)
  
dev1=data.frame(dev1)
for(i in 1:ncol(dev1)){
  dev1[is.na(dev1[,i]), i] <- mean(dev1[,i], na.rm = TRUE)
}
library(lubridate)


ymd(ts(dev1$performance_metrics.ts))
ggplot(data = dev1) +
  geom_line(mapping = aes(x =as.Date(performance_metrics.ts), y=Qmin,colour='Qmin')) +
  geom_line(mapping = aes(x =as.Date(performance_metrics.ts), y=Qmax,colour='Qmax'))+
  geom_line(mapping = aes(x =as.Date(performance_metrics.ts), y=Qave,colour='Qve'))+
  
  theme(axis.text.x = element_text(angle=90, vjust = 0.5))
  
ts(dev1$performance_metrics.ts)
  
library(forecast)
fit=ets(dev1$Qmin)
plot(forecast(fit))
plot(dev1$Qmin)


fit<- auto.arima(dev1$Qave)
ggplot(data=data.frame(forecast(fit)))+
  geom_line(aes(x=index,y=Point.Forecast))
   


Point.Forecast    Lo.80    Hi.80    Lo.95    Hi.95



ggplot(data = dev1) +
  geom_line(mapping = aes(x =performance_metrics.ts, y=BerPostFecAve))


 











