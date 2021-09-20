# Input 2010 CIP code with a "=" in front (due to weird formatting)
CIPCode = "=29.0201"
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
# simple estimation calculation of yearly income based on weighting median income across all OCCs equally
avg = 0
for(i in ind){
  val = 1/(length(ind))*(as.integer(bls$A_MEDIAN[i]))
  avg = avg + val
}
print(avg)
