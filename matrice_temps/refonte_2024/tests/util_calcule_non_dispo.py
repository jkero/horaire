"""Vérifie si une date (jour 24h) intersecte avec une plage de dates-heures (ou vice-versa)
**contexte**: pour chaque jour d'une semaine, vérifier une liste d'employés
qui ne seraient pas disponibles (selon table non-dispo) ce jour là.

// todo : prévoir la vérification de portions de journées (quarts) au lieu de 0 à 23h59

en entrée: une plage (deb et fin en datetime) de non-dispos et un jour (date).

en sortie: True ou False

"""
import locale
import calendar
from datetime import timedelta,datetime
class check_non_dispo:
    deb = None
    fin = None
    le_jour = None
    # def __init__(self):
    #     print("classe instanciée")

    @staticmethod
    def is_not_dispo(d, f, j):
        resultat = False
        xd = datetime.strptime(d, '%Y-%m-%d %H:%M')
        xf = datetime.strptime(f, '%Y-%m-%d %H:%M')
        xjd = datetime.strptime(j, '%Y-%m-%d %H:%M')
        xjf = datetime.strptime(j, '%Y-%m-%d %H:%M')  + timedelta(hours=23.999)
        # print("\t %s %s \t %s" % (d,f,j))
        # print("\t %s %s \t %s %s" % (str(xd), str(xf), str(xjd), str(xjf)))
        if xd <= xjd and xf > xjd:
            resultat = True
        elif xd < xjf and xf >= xjf:
            resultat = True
        elif xd >= xjd and xf <= xjf:
            resultat = True

        return resultat

#pour les tests
# rawd = '2024-03-23  08:00'
# rawf = '2024-03-23  17:00'
# rawj ='2024-03-23  00:00'
#
# list_jeu_de_tests = [['non_dispo n\'intercepte pas la journée','2024-03-23 08:00','2024-03-23 17:00','2024-03-24 00:00'],
#           ['non_dispo intercepte la journée','2024-03-23 08:00','2024-03-23 17:00','2024-03-23 07:00'],
#            ['non_dispo n\'intercepte pas la journée','2024-03-23 08:00', '2024-03-23 17:00', '2024-03-23 18:00'],
#            ['non_dispo n\'intercepte pas la journée', '2024-03-23 08:00', '2024-03-23 17:00', '2024-03-22 05:00'],
#            ['dispo intercepte la journée', '2024-03-23 08:00', '2024-03-23 17:00', '2024-03-22 12:00'],
#            ['dispo intercepte la journée', '2024-03-23 08:00', '2024-03-23 17:00', '2024-03-23 12:00']
#            ]
#
# if __name__ == '__main__':
#     #app = check_non_dispo()
#     for jeu in list_jeu_de_tests:
#         print(jeu[0])
#         print(check_non_dispo.is_not_dispo(jeu[1],jeu[2],jeu[3]))


