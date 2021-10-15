from basics import findClosest,readCSV


df = readCSV('groundTruth.csv')

#We should define a list containing all the ids of our database seeing that the ids are random 
#Since we can't convert directly a Series Object to a set we do the following 

ids = list(set(df['ID'].tolist()))
ids_copy = list(set(df['ID'].tolist()))

#print(readCSV("smallBDD.csv"))
#switchLines("smallBDD.csv",0,4)

#In total we got 14 clusters: 249.94 secs to generate we have to optimize it later on

for id in ids_copy:
    if id in ids:
        findClosest(id,ids)

print(ids)
