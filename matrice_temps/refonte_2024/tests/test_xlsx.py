import datetime
from datetime import timedelta, datetime
import locale
import calendar
import sys, os, unittest

import xlsxwriter.exceptions

from matrice_temps.refonte_2024.dev import util_xlsx
from matrice_temps.refonte_2024.dev import util_compose_equipes as cp

class TestProd_xlsx(unittest.TestCase):
    """
    Ce test est basé sur une db de test mariadb. Les valeurs sont testées sur la semaine # 44 (2024) de
    la table previsions_par_semaine (2360 heures de travail) avec une config pour le premier jour de la semaine = 0 (lundi).
    """

    horaire = None
    prem_jour = 0
    an = 0
    n_semaine = 0
    def setUp(self):
        self.prem_jour = 0
        self.an = 2024
        self.n_semaine = 44

        self.horaire = util_xlsx.Prod_chiffrier
        zefile = os.path.join('/', 'home', 'jack', 'python_projets', 'horaire', 'horaire', 'matrice_temps','refonte_2024', 'dev', 'builds_xlsx')
        #print("zefile :" + zefile)
        self.horaire.initialise(zefile, self.prem_jour, self.an, self.n_semaine)

    def test_initialise(self):
        try:
            #horaire = util_xlsx.Prod_chiffrier
            #zefile = os.path.join('C:\', 'sphynx_repo', 'sphinx_repo', 'horaire', 'matrice_temps', 'refonte_2024', 'dev', 'builds_xlsx')

            #print('Aujourd\'hui:')
            #print(str(self.horaire.aujourd))
            #print('La semaine selon ces paramètres: année: %s  num semaine: %s, prem_jour: %d (round trip mariadb)' % ( self.horaire.annee, self.horaire.semaine, self.horaire.prem_jour_sem))
            #print("sem ref %s" % str(self.horaire.date_sem_ref))
            #       xd = datetime.strptime(d, '%Y-%m-%d %H:%M')
            deb_sem = datetime.strptime(str(self.horaire.date_sem_ref[0][1]),"%Y-%m-%d %H:%M")
            #print("Début de la semaine: %s" % str(deb_sem))
            #print("Le premier jour : %d" % deb_sem.weekday())
            self.assertEqual(deb_sem.weekday(),0)
            self.assertEqual(str(deb_sem)[:10], '2024-11-04')

            # print("_______________________________________________")
            # print(str(horaire.dict_semaine))
        except  xlsxwriter.exceptions.FileCreateError as e:
            print(e)
        finally:
            self.horaire.wb.close()
            self.test_charges_heures()

    def test_charges_heures(self):
        """ Tester que le modèle calculé rencontres les valeurs (>=) des heures prévues """
        try:
            sem_modele = cp.CompositionEquipes.modele
            sem_modele.db_recup_modele(2024, 44)
            print("Heures prévues pour la semaine % d: %d" % (sem_modele.prev_num_sem, sem_modele.prev_heures_sem))
            print("Heures compatibles proposées par le modèle: %d" % (sem_modele.h_modele))
            print("Excédent des heures : %d " % sem_modele.excedent)
        except Exception as e:
           print(e)


