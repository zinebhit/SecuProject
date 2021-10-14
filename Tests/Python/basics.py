import pandas as pd

def readCSV(filename):
    column_names = ["ID", "DateTime", "X", "Y"]
    dtypes = {'ID': 'int64', 'DateTime': 'str', 'X': 'float64', 'Y': 'float64'}
    parse_dates = ['DateTime']
    df = pd.read_csv(filename, sep='\t', header=None, names=column_names, dtype=dtypes, parse_dates=parse_dates)
    return df

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
    # print(dataframe.iloc[lambda x : x.index == index1])
    # print(dataframe.iloc[lambda x : x.index == index2])
    temp = dataframe.iloc[index1]
    dataframe.iloc[lambda x : x.index == index1] = dataframe.iloc[lambda x : x.index == index2]
    dataframe.iloc[lambda x : x.index == index2] = temp
    dataframe.to_csv(fileName, index = False, sep='\t', header=None)


