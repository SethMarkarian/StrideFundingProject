#bls = read_xlsx(file.choose()) 
#crosswalk = read_xlsx(file.choose(),"CIP-SOC")

newData <- c(crosswalk[1:100,1],crosswalk[1:100,3],crosswalk[1:100,2],crosswalk[1:100,4])
newData$CIP2 = str_trunc(newData$CIP2020Code,2,ellipsis="")
newData$CIP4 = str_trunc(newData$CIP2020Code,5,ellipsis="")
newData$freq = rep(seq(1,10),10)
#newData$freq = newData$freq/sum(newData$freq)


  
Data = as.data.frame(newData)

collapsibleTreeSummary(
  Data,
  hierarchy = c("CIP2","CIP4","CIP2020Title", "SOC2018Title"),
  #nodeSize = "freq",
  #fillByLevel = FALSE,
  attribute = "freq",
  zoomable = FALSE,
  tooltip = TRUE,
  width = 1000,
  percentOfParent = TRUE
)

