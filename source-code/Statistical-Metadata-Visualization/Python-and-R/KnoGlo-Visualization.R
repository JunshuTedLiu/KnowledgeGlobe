# setwd("~/Documents/GitHub/KnowledgeGlobe/source-code/Analysis-and-Visualization")

# Every time before you switch to a new folder, you need to go back to the upper menu.
setwd("../") # NOT FOR THE FIRST TIME OF USE!

# Set your work directory, which should be the folder that contains the datasets that you want to visualize.
setwd("keyword_computer_year_1988")

# Save CSV tables

subject <- read.csv('statistics_subject.csv', stringsAsFactors = FALSE)
keyword <- read.csv('statistics_keyword.csv', stringsAsFactors = FALSE)
pub     <- read.csv('statistics_pub.csv', stringsAsFactors = FALSE)
year    <- read.csv('statistics_year.csv', stringsAsFactors = FALSE)
country <- read.csv('statistics_country.csv', stringsAsFactors = FALSE)
type    <- read.csv('statistics_type.csv', stringsAsFactors = FALSE)

keywordInput <- readline(prompt="Enter the topic (keyword) name that you've used in KnowledgeGlobe.py: ")
keywordInput

yearInput <- readline(prompt="Enter the year that you've used in KnowledgeGlobe.py: ")
yearInput

# Visualizations

# 0. subject

# Bar Plot
par(mar=c(12,4,4,1)) # apply margins since the name will be so long
xcor <- barplot(subject$count, main = paste("Subjects of publications about", keywordInput, "in", yearInput), names.arg=c(subject$value), las = 2, cex.names = 0.6)
text(x = xcor, y = subject$count, label = subject$count, pos = 3, cex = 0.8, col = "red")
dev.off()
# The 'mar' argument of 'par' sets the width of the margins in the order: 'bottom', 'left', 'top', 'right'. The default is to set 'left' to 4,
# https://stackoverflow.com/questions/2807060/r-is-plotting-labels-off-the-page

# Pie Chart
# Not recommended! Unless you have paid API license with full access
# The Basic plan for Springer API will only return the top 20 results for the statistics for each attribute
slices <- c(subject$count)
lbls <- c(subject$value)
pct <- round(slices/sum(slices)*100)
lbls <- paste(lbls, pct) # add percents to labels 
lbls <- paste(lbls,"%",sep="") # ad % to labels 
pie(slices,labels = lbls, col=rainbow(length(lbls)), main=c("Subjects of publications about ", keywordInput, " in ", yearInput))

# 1. keyword

# Bar Plot
xcor1 <- barplot(keyword$count, main = c("Keywords of publications about ", keywordInput, " in ", yearInput), names.arg=c(keyword$value), las = 2)
text(x = xcor1, y = keyword$count, label = keyword$count, pos = 3, cex = 0.8, col = "red")

# Pie Chart
# Not recommended! Unless you have paid API license with full access
# The Basic plan for Springer API will only return the top 20 results for the statistics for each attribute
slices1 <- c(keyword$count)
lbls1 <- c(keyword$value)
pct1 <- round(slices1/sum(slices1)*100)
lbls1 <- paste(lbls1, pct1) # add percents to labels
lbls1 <- paste(lbls1,"%",sep="") # ad % to labels
pie(slices1,labels = lbls1, col=rainbow(length(lbls1)), main=c("Keywords of publications about ", keywordInput, " in ", yearInput))

# 2. pub
barplot(pub$count, main = c("Publishers of the journals about ", keywordInput, " in ", yearInput), names.arg=c(pub$value), col=rainbow(20, start=.7, end=.1), las = 2, cex.names = 0.9)

# 3. year (total)
year$count
barplot(year$count, main = c("Quantities of publications about ", keywordInput, " for each year"), names.arg=c(year$value), las = 2)

# 4. country
barplot(country$count, main = c("Quantities of publications about ", keywordInput, " for each countries in ", yearInput), names.arg=c(country$value), las = 2)

# 5. type
slices2 <- c(type$count)
lbls2 <- c(type$value)
pct2 <- round(slices2/sum(slices2)*100)
lbls2 <- paste(lbls2, pct2) # add percents to labels
lbls2 <- paste(lbls2,"%",sep="") # ad % to labels
pie(slices2,labels = lbls2, col=rainbow(length(lbls2)), main="Types of publications about ", keywordInput, " in ", yearInput)

dev.off()

# put everything together in one place.
# (Need to fix the margin problem)
par(mfrow = c(2,2))
# be sure to run the code above.
# 0. subject
xcor <- barplot(subject$count, main = paste("Subjects of publications about", keywordInput, "in", yearInput), names.arg=c(subject$value), las = 2, cex.names = 0.6)
text(x = xcor, y = subject$count, label = subject$count, pos = 3, cex = 0.8, col = "red")
# 1. keyword
xcor1 <- barplot(keyword$count, main = c("Keywords of publications about ", keywordInput, " in ", yearInput), names.arg=c(keyword$value), las = 2)
text(x = xcor1, y = keyword$count, label = keyword$count, pos = 3, cex = 0.8, col = "red")
# 2. pub
barplot(pub$count, main = c("Publishers of the journals about ", keywordInput, " in ", yearInput), names.arg=c(pub$value), col=rainbow(20, start=.7, end=.1), las = 2, cex.names = 0.9)
# 4. country
barplot(country$count, main = c("Quantities of publications about ", keywordInput, " for each countries in ", yearInput), names.arg=c(country$value), las = 2)

dev.off()

# now, let's make something fancy!

# R bokeh
# Learn more at http://hafen.github.io/rbokeh
# install.packages("rbokeh")
library(rbokeh)
p <- figure(width = 1000, height = 600) %>%
  ly_points(value, count, data = country,
            color = value, glyph = value,
            hover = list(value, count)) %>%
  x_axis(angle = 45)
p

# this looks better. I swapped the x and y axis.
p1 <- figure(width = 1000, height = 600) %>%
  ly_points(count, value, data = country,
            color = value, glyph = value,
            hover = list(count, value)) %>%
  theme_legend(background_fill_alpha = 0.25)
p1

# Feel free to use any other visualization frameworks like ggplot.
# install.packages("ggplot2")
library(ggplot2)