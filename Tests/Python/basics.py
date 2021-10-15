from os import close
import pandas as pd

debug = 1

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
    temp = dataframe.iloc[index1]
    dataframe.iloc[lambda x : x.index == index1] = dataframe.iloc[lambda x : x.index == index2]
    dataframe.iloc[lambda x : x.index == index2] = temp
    dataframe.to_csv(fileName, index = False, sep='\t', header=None)
    
    if (debug):
        print("Switching line:\n",dataframe.iloc[lambda x : x.index == index1],"\n With the line:\n",dataframe.iloc[lambda x : x.index == index2],"\n")

def findClosest(id,ids):
    """
        This function is going to help us find, for a specific id, the ids of the people whose position is the closest to his and remove the ids from 
        our initial ids' list for optimization and to prevent repetition. 
        id: id of the specific person 
        ids: list of ids present in our ground truth file
    """
    #Access the element using loc with the ID attribute for optimization : df.loc[df['ID'] == 1] or with the coordinates attributes e.g: df.loc[df['X'] == x1]
    
    print("Id: ", id)
    ids.remove(id)
    df = readCSV("groundTruth.csv")
    person = df.loc[df['ID'] == id]
    x = person.iloc[0,2]
    y = person.iloc[0,3]
    closePeople = df.loc[(round(df['Y'],5) == round(y,5)) & (df['ID'] != id) & (round(df['X'],2) == round(x,2))]
    closeIDs = [id]
    for i in range(len(closePeople)):
        if(len(closeIDs) == 11):
            break
        if((closePeople.iloc[i,0] not in closeIDs) and (closePeople.iloc[i,0] in ids)):
            closeIDs.append(closePeople.iloc[i,0])
            ids.remove(closePeople.iloc[i,0])

    if(debug):
        print("Id: ", id, "\nclosest: \n",closeIDs)
        print("IDs left: \n",ids,"\n\n\n")

