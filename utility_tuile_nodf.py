import csv
import json
import datetime
import argparse
from Utils import separator #Définir votre propre séparateur Ex: '\t', ' '

from collections import defaultdict
def dictstruc(): return defaultdict(int)

#/\/\/\/\/\/\ Nom de la métrique: Déplacements effectués /\/\/\/\/\/\
#Le but de cette métrique est de calculer la différence de zone de couverture d’un individu durant les 12 semaines d’étude.
#L’idée est la suivante : la métrique permet de vérifier que, globalement, la version anonymisée garde les informations de déplacement et de couverture d’un individu.
#Pour ce faire on mesure le nombre de cellules différentes dans laquelle l’utilisateur a séjourné.
#Le score est calculé de la manière suivante :

#       Somme [pour chaque i individu] :
#               Si nb_cellule_fichier_original_pour_i > nb_cellule_fichier_anonyme_pour_i :
#                       nb_cellule_fichier_anonyme_pour_i / nb_cellule_fichier_original_pour_i
#               Sinon :
#                       nb_cellule_fichier_original_pour_i / nb_cellule_fichier_anonyme_pour_i
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

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

def main(originalFile, anonymisedFile, parameters={"size":2}):
        global size
        size = parameters['size']

        fd_original = open(originalFile, newline='')
        fd_anonymised = open(anonymisedFile, newline='')
        original_reader = csv.reader(fd_original, delimiter=separator)
        anonymised_reader = csv.reader(fd_anonymised, delimiter=separator)

        tabOri = defaultdict(dictstruc)
        tabAno = defaultdict(dictstruc)
        for lineOri, lineAno in zip(original_reader, anonymised_reader):

                #--- Original file
                id = lineOri[0]
                gps1 = (round(float(lineOri[2]),size), round(float(lineOri[3]),size))
                date = datetime.date.fromisoformat(lineOri[1][0:10])
                calendar = date.isocalendar()
                key = (id)
                #key = (id, calendar[0], calendar[1])
                tabOri[key][gps1] += 1

                #--- Anonymisation file
                if lineAno[0] != "DEL":
                        gps2 = (round(float(lineAno[2]),size), round(float(lineAno[3]),size))
                        tabAno[key][gps2] += 1

        final_tab_original = defaultdict(int)
        final_tab_anonymised = defaultdict(int)
        for id in tabOri:
                final_tab_original[id] = len(tabOri[id])
                final_tab_anonymised[id] = len(tabAno[id])

        total_size = len(final_tab_original)
        score = 0
        for id in final_tab_original:
                if final_tab_original[id]>final_tab_anonymised[id]:
                        score += final_tab_anonymised[id] / final_tab_original[id]
                else:
                        score += final_tab_original[id] / final_tab_anonymised[id]

        return score/total_size

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("anonymized", help="Anonymized Dataframe filename")
    parser.add_argument("original", help="Original Dataframe filename")
    args = parser.parse_args()
    print(main(args.anonymized, args.original))
