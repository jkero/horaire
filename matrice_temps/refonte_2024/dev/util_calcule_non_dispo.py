"""Vérifie si une date d'une semaine donnée (jour heure) intersecte avec une plage de non-disponibilités, dates-heures inscrites à la base de données(ou vice-versa)

**contexte**: pour chaque jour d'une semaine, vérifier une liste d'employés qui ne seraient pas disponibles (selon table non-dispo) ce jour là.

// todo : prévoir la vérification de portions de journées (quarts) au lieu de 0 à 23h59

Attributes:
     semaine  int -- codé en dur  : La semaine de l'horaire à produire
     annee  int-- codé en dur  : année
     dict_semaine -- appelé dans utilitaire :

en sortie (Check_non_dispo): True ou False

"""
import locale
import calendar
from datetime import timedelta,datetime
class Check_non_dispo:
    deb = None
    fin = None
    le_jour = None
    @staticmethod
    def is_not_dispo(deb_fin, j):
        """
        :param deb, fin String obtenu de la colonne creneaux dans table non_dispo
        :param j String la date du jour de la semaine
        :returns Bool.
        """
        resultat = False
        d,f = deb_fin.split('@')
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
