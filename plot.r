rm(list = ls())
library(readr)
library(tidyverse)
library(ggplot2)
library(dplyr)
library(scales)

# load files
data1 <- read_csv("mocasin-100/results.csv")
data1 <- mutate(data1, version = "mocasin")
data2 <- read_csv("linux-100/results.csv")
data2 <- mutate(data2, version = "linux")
data3 <- read_csv("linux-ondemand/results.csv")
data3 <- mutate(data3, version = "linux-ondemand")
data4 <- read_csv("linux-schedutil/results.csv")
data4 <- mutate(data4, version = "linux-schedutil")
data5 <- read_csv("linux-powersaver/results.csv")
data5 <- mutate(data5, version = "linux-powersaver")

data <- rbind(data1, data2, data3, data4, data5)
names(data) <- c("time_s", "total_energy_J", "average_power_W", "version")

# find average, min and max values for each parameter
data <- aggregate(cbind(data$time_s, data$total_energy_J, data$average_power_W), 
                  list(data$version), 
                  FUN= function(x) c(mn = mean(x), mi = min(x), mx = max(x)))

data <- as.data.frame(matrix(unlist(t(data)), byrow=T, 5, 10))
names(data) <- c("version",
                 "time_s",
                 "time_min",
                 "time_max",
                 "total_energy_J",
                 "energy_min",
                 "energy_max",
                 "average_power_W",
                 "power_min",
                 "power_max")

# plot
data <- data %>% 
  mutate(version = factor(version, levels = c("mocasin", "linux", "linux-ondemand", "linux-schedutil", "linux-powersaver"))) %>% 
  arrange(version)

plot = ggplot(data, aes(x=version, y=as.numeric(time_s)), position=position_dodge2(width=0.9)) +
  geom_bar(stat="identity", fill="#83c5be") +
  geom_text(aes(label = "96.2", x = "linux-powersaver", y = 17, vjust=0)) +
  xlab("version") + 
  ylab("exec. time (s)") +
  scale_y_continuous(limits = c(12,17), oob = rescale_none) +
  geom_errorbar(
    aes(ymin=as.numeric(time_min), ymax=as.numeric(time_max)), colour="black", width=.3
  ) +
  coord_cartesian(clip = 'on') +
  #ggtitle("my title") + 
theme(
  text = element_text(size=15),
  legend.position = "top",
  legend.margin = margin(),
  axis.text.x = element_text(size=15, angle=35, vjust=0.5),
  strip.text = element_text(size=15, margin = margin(t=1.5, b=1.5)),
  axis.title= element_text(size=15),
  legend.text= element_text(size=15),
)

#plot(plot)

# save
ggsave("time.pdf", plot, width=200, height =100, units="mm")