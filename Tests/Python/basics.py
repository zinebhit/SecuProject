import pandas as pd

def readCSV(filename):
    data = pd.read_csv(filename) 
    return data

def copyCSV(origin, destination):
    copy = open(destination,"w")
    copy.write(readCSV(origin))
    origin.close()
    copy.close()

def switchLines(fileName, index1, index2):
    """
        This function is used to switch the position of two lines.
        Attention: indexing starts at 0.
    """
    dataframe = readCSV(fileName)
    print(dataframe.iloc[index1][0])
    print(dataframe.iloc[index2][0])
    temp = dataframe.iloc[index1][0]
    dataframe.iloc[index1][0] = dataframe.iloc[index2][0]
    dataframe.iloc[index2][0] = temp
    dataframe.to_csv(fileName, index = False)
    print("\n\n\n", dataframe.iloc[0][0])

