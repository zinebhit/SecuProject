import pandas as pd

data = pd.read_csv('groundTruth.csv')
data1 = data.to_numpy()

copy = open("copy.csv","w")
copy.write(data.to_string())
copy.close()
