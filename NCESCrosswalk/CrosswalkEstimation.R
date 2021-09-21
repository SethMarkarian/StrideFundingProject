# Input 2010 CIP code with a "=" in front (due to weird formatting)
CIPCode = "=01.0000"
# First locate index of 2010 CIP Code, then obtain the 2020 CIP code from the same indexed location
CIP = sub("=","",CIPCrosswalk$Current.code[which(CIPCrosswalk$Original.code == CIPCode)])

# Locate SOC codes based on CIP code
SOCs = crosswalk$SOC2018Code[which(crosswalk$CIP2020Code == CIP)]

# Check if SOC code exists in BLS dataset. If it does, add its index to the list of indices 
ind = NULL
j=1
for(i in SOCs){
  k = which(bls$OCC_CODE == i)
  if(length(k) != 0){
    ind[j] = k
    j = j + 1
  }
}
#This weights the average based on emplyoment numbers i.e. expected value
employment = as.integer(bls$TOT_EMP[ind])
# simple estimation calculation of yearly income based on weighting median income across all OCCs
avg = 0
for(i in 1:length(ind)){
  val = employment[i]/(sum(employment))*(as.integer(bls$A_MEDIAN[ind[i]])) # Can be edited for different percentiles eg. A_PCT25 or A_PCT10
  print(val)
  avg = avg + val
}
print(avg)


