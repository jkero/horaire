import datetime
import time
from datetime import timedelta, datetime
import locale
import calendar
import sys, os, unittest

import xlsxwriter.exceptions

from matrice_temps.refonte_2024.dev import util_xlsx

class TestProd_xlsx(unittest.TestCase):
    """
    Ce test est basé sur une db de test mariadb. Les valeurs sont testées sur la semaine # 44 (2024) de
    la table previsions_par_semaine (2360 heures de travail) avec une config pour le premier jour de la semaine = 0 (lundi).
    """

    def test_initialise(self):
        try:
            horaire = util_xlsx.Prod_chiffrier
            zefile = os.path.join('C:\\' ,'sphynx_repo', 'sphinx_repo', 'horaire', 'matrice_temps', 'refonte_2024', 'dev', 'builds_xlsx')
            print("zefile :" + zefile)
            props = horaire.initialise(zefile, 0, 2024, 44)
            print('Aujourd\'hui:')
            print(str(horaire.aujourd))
            print('La semaine selon ces paramètres: année: %s  num semaine: %s, prem_jour: %d (round trip mariadb)' % ( horaire.annee, horaire.semaine, horaire.prem_jour_sem))
            print(str(horaire.date_sem_ref))
            #       xd = datetime.strptime(d, '%Y-%m-%d %H:%M')
            print("Start of week:", datetime.strptime(str(horaire.date_sem_ref[0][1]),"%Y-%m-%d %H:%M"))
            print(datetime.strptime(str(horaire.date_sem_ref[0][1]),"%Y-%m-%d %H:%M").weekday())
            # print("_______________________________________________")
            # print(str(horaire.dict_semaine))
        except xlsxwriter.exceptions.FileCreateError as e:
            print(e)
        finally:
            time.sleep(5)
            horaire.wb.close()



