import pandas as pd

data = pd.read_csv('smallBDD.csv') # rename as how your groundtruth is 
data1 = data.to_numpy()

#copy = open("copy.csv","w")
#copy.write(data.to_string())
#copy.close()

#small column additon 

# print(df.shape)
# new_column = pd.Series(['1','2'],name="extra_column")
# df.update(new_column)

#big column modification 
