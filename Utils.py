import pandas as pd
import numpy as np
import csv
import os
import zipfile

separator = "\t"

#################################
#       Global functions        #
#################################

def csv_length(filename):
    try:
        return sum(1 for line in open(filename))
    except:
        return -1

def csv_width(filename):
    return sum(1 for char in next(open(filename)) if char == separator) + 1

def del_indexes(filename):
    index=0
    indexes = []
    fd = open(filename, "r")
    nona_reader = csv.reader(fd, delimiter=separator)
    for row in nona_reader:
        if row[0] == "DEL":
            indexes += [index]
        index += 1
    return indexes

def checking_shape(input, default):
    length = 0
    size = (csv_length(default), csv_width(default))
    if size[0] < 0 or size[1] < 0 : return (-1, 0) #If the original file has a correct shape
    # Checking the number of rows and columns
    try:
        for line in open(input):
            if sum(1 for char in line if char == separator) + 1 != size[1]:
                return (-2, length)
            length += 1
    except:
        return (-3, 0)
    return (-4, length) if length != size[0] else (1, 0)


# Shuffling a chunk
def chunk_shuffler(filename, offset, toRead):
    df = pd.read_csv(filename, skiprows=offset, nrows=toRead, header=None, dtype=object, sep=separator)
    df.drop(del_indexes(filename), inplace=True)
    # Using pandas module to read only one chunk in a huge file (header=None must be removed for official files)
    return df.reindex(np.random.permutation(df.index))
    # Shuffling indexes created by the dataset shuffles also indexed rows

def unzip_inputfile(filename):
    filenamezip = filename+".zip"
    directoryname = filename+"_directory"

    with zipfile.ZipFile(filenamezip, 'r') as zip_ref:
        zip_ref.extract(zip_ref.infolist()[0], path=directoryname)
    os.rename(directoryname+"/"+zip_ref.infolist()[0].filename, filename)
    os.rmdir(directoryname)

def unzip_originfile(filename):
    filenamezip = filename+".zip"
    directoryname = filename+"_directory"

    with zipfile.ZipFile(filenamezip, 'r') as zip_ref:
        zip_ref.extract(zip_ref.infolist()[0], path=directoryname)
    os.rename(directoryname+"/"+zip_ref.infolist()[0].filename, filename)
    os.rmdir(directoryname)

def zip_outfileShuffle(filename):
    filenamezip = filename+".zip"
    with zipfile.ZipFile(filenamezip, 'w') as zip_ref:
        zip_ref.write(filename)

def error_messages(errortuple):
    #Returns the error type and the error source : a script name or a line number
    if errortuple[0] == -1:
        return "le fichier original est invalide"
    elif errortuple[0] == -2:
        return "le fichier déposé est invalide (mauvais nombre de colonnes)\n ligne " + str(errortuple[1])
    elif errortuple[0] == -3:
        return "le fichier déposé est invalide\n (mauvais format)"
    elif errortuple[0] == -4:
        return "le fichier déposé est invalide (mauvais nombre de lignes)"
    elif errortuple[0] == -5:
        return "un utilisateur posséde plusieurs identifiants par semaine\n ligne " + str(errortuple[1])
    elif errortuple[0] == -6:
        return "un identifiant est manquant\n ligne "+str(errortuple[1])
    elif errortuple[0] == -7:
        return "erreur dans le calcul d’utilité (Vérifiez votre fichier déposé)\n ligne " + str(errortuple[1])
    elif errortuple[0] == -8:
        return "erreur dans le script " + errortuple[1]
    elif errortuple[0] == -9:
        return "aucun script d'utilité fonctionnel trouvé"
    elif errortuple[0] == -10:
        return "La date est inexistante ou mal formatée\n ligne " + str(errortuple[1])
    elif errortuple[0] == -11:
        return "Le fichier ZIP est mal formatté"
    elif errortuple[0] == -12:
        return "Erreur fichier ZIP Administrateur"


# Custom default dict
def list_struct(): return [float(), float()]
