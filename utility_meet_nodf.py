import csv
import json
import argparse
from collections import OrderedDict
from Utils import separator #Définir votre propre séparateur Ex: '\t', ' '


#/\/\/\/\/\/\ Nom de la métrique: Croisements /\/\/\/\/\/\
#Le but de cette métrique est d'identifier les cellules où circulent le plus d'utilisateurs.


##############################
# --- Taille des cellules ---#
##############################
size = 2
#  4 : cellule au mètre
#  3 : cellule à la rue
#  2 : cellule au quartier
#  1 : cellule à la ville
#  0 : cellule à la région Française
# -1 : cellule au pays
##############################
# --- Minimum de passage  ---#
# Le nombre de localisation  #
# comptées                                       #
##############################
min_meet = 0
# 0: tout est compté



def main(originalFile, anonymisedFile, parameters={"size":2, "min_meet":0}):
        global size
        size = parameters['size']
        global min_meet
        min_meet = parameters['min_meet']

        fd_original = open(originalFile, newline='')
        fd_anonymised = open(anonymisedFile, newline='')
        original_reader = csv.reader(fd_original, delimiter=separator)
        anonymised_reader = csv.reader(fd_anonymised, delimiter=separator)

        tabOri = OrderedDict()
        tabAno = OrderedDict()
        for lineOri, lineAno in zip(original_reader, anonymised_reader):

                #--- Original file
                gps1 = (round(float(lineOri[2]),size), round(float(lineOri[3]),size))
                key = gps1
                #key = ((latitude, longitude))
                if key not in tabOri:
                        tabOri[key] = 0
                else:
                        tabOri[key] += 1

                #--- Anonymisation file
                if lineAno[0] != "DEL":
                        gps2 = (round(float(lineAno[2]),size), round(float(lineAno[3]),size))
                        if gps2 not in tabAno:
                                tabAno[gps2] =0
                        else:
                                tabAno[gps2] +=1

        utility = 0
        total_size = 0
        key_list = list(tabAno.keys())
        tabAno_sorted = sorted(tabAno.items(), key=lambda t: t[1])

        i = min_meet
        if i == 0:
                for key in tabAno:
                        total_size +=1
                        if key in tabOri:
                                if tabAno[key] == 0 or tabOri[key] ==0 or tabOri[key]==tabAno[key]:
                                        score =1
                                else:
                                        score = tabAno[key]/(tabOri[key])
                                if score > 1:
                                        score = 1/score
                                utility+= score
        if i>0:
                tmp = 0
                while tmp < min_meet and tmp < len(tabAno):
                        total_size +=1
                        key = tabAno_sorted[-1-tmp][0]
                        if key in tabOri:
                                if tabAno[key] == 0 or tabOri[key] ==0 or tabOri[key]==tabAno[key]:
                                        score =1
                                else:
                                        score = tabAno[key]/(tabOri[key]+1)
                                if score > 1:
                                        score = 1/score
                                utility+= score
                        tmp +=1

        final_utility = utility/total_size
        #print("---- utility totale : "+str(utility) +"\n")
        #print("Utilité: "+str(final_utility) +"\n")
        #print("longueur:" +str(total_size)+"\n")
        return final_utility

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("anonymized", help="Anonymized Dataframe filename")
    parser.add_argument("original", help="Original Dataframe filename")
    args = parser.parse_args()
    print(main(args.anonymized, args.original))
