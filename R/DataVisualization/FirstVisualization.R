newData <- c(crosswalk[1:100,1],crosswalk[1:100,3],crosswalk[1:100,2],crosswalk[1:100,4])
newData$CIP2 = str_trunc(newData$CIP2020Code,2,ellipsis="")
newData$CIP4 = str_trunc(newData$CIP2020Code,5,ellipsis="")
newData$freq = rep(seq(1,10),1)
newData$freq = newData$freq/sum(newData$freq)
#p = alluvial_wide(data.frame(newData), stratum_labels=FALSE)
alluvial_wide(data.frame(newData), stratum_labels=FALSE)
# parcats(p, marginal_histograms = FALSE)
to_lodes_form(as.data.frame(newData),weight=c(1))

alluvial_wide(as.data.frame(newData),weight=c(1,2,3,4,5))
titanic_wide <- data.frame(Titanic)
head(titanic_wide)
ggplot(data = as.data.frame(newData),
       aes(axis1 = CIP2020Code, axis2 = SOC2018Code, y =freq)) + 
  scale_x_discrete(limits = c("CIP", "SOC"), expand = c(.2, .05)) +
  xlab("Demographic") +
  geom_alluvium(aes(fill = CIP2020Code)) +
  geom_stratum()
  geom_text(stat = "stratum", aes(label = after_stat(stratum)))

alluvial_wide(as.data.frame(newData), aes(axis1 = CIP2020Code, axis2 = SOC2018Code, y =freq))

p = ggplot(data = titanic_wide,
       aes(axis1 = Class, axis2 = Sex, axis3 = Age,
           y = Freq)) +
  scale_x_discrete(limits = c("Class", "Sex", "Age"), expand = c(.2, .05)) +
  xlab("Demographic") +
  geom_alluvium(aes(fill = Survived)) +
  geom_stratum() +
  geom_text(stat = "stratum", aes(label = after_stat(stratum))) +
  theme_minimal()
  #ggtitle("passengers on the maiden voyage of the Titanic",
  #        "stratified by demographics and survival")
parcats(p,marginal_histograms = FALSE)

collapsibleTree(
  as.data.frame(newData),
  hierarchy = c("CIP2","CIP4","CIP2020Title", "SOC2018Title"),
  #nodeSize = "freq",
  width = 1300,
  #fillByLevel = FALSE,
  attribute = "freq",
  zoomable = FALSE
)
