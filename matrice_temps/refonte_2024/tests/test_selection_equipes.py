import datetime
import locale
import calendar
from tests_connection import ma_connect
import unittest
import tests_connection

class test_affect_equipes(unittest.TestCase):
    dummy_dico_staff ={}
    la_conn = None
    an = 2024
    num_semaine = 6
    hpers = 0.0
    def test_1etablir_conn(self):
        self.la_conn = ma_connect()
        print("TEST ---- connection != None")
        self.assertNotEqual(self.la_conn.conn,None)
        #self.getLeads()

    def test_2getLeads(self):
        self.la_conn = ma_connect()
        jkcur = self.la_conn.conn.cursor()
        queryLeads = "select * from employe where anciennete > 55 and niveau >= 3 order by niveau desc"
        jkcur.execute(queryLeads)
        print("TEST ---- query niveau des employes != None")
        self.assertNotEqual(jkcur, None)
        # for emp in jkcur:
        #     print(" %s, %s, n = %d" % (emp[2],emp[3],emp[7]))

    def test_3get_hpers(self):
        an = self.an
        num_semaine = self.num_semaine
        self.la_conn = ma_connect()
        jkcur = self.la_conn.conn.cursor()
        queryHpers = "select prevision_pers_h from previsions_par_semaine where annee =  ? and num_semaine = ?"
        jkcur.execute(queryHpers,(an,num_semaine))
        print("TEST ---- querysemaine != None")
        self.assertNotEqual(jkcur, None)
        if jkcur is not None:
            h = jkcur.fetchone()
            self.hpers = h[0]

    def test_4ventile_hpers_v_modeles(self):
        """ pour un nombre d'heures prévues hprevues, pour chaque modele hmod disponible
            par ordre asc de hmod resource disponible,
                si hmod < hprevues(le modele prevoit ou non une config pour ce nombre)
                    passe au modele suivant
                sinon
                    utiliser le modele (le modele accomode la charge, ou plus).
        """
        an = self.an
        num_semaine = self.num_semaine
        self.la_conn = ma_connect()
        jkcur = self.la_conn.conn.cursor()
        query_mod_hres = sem_hpers = 0
        queryHpers = "select prevision_pers_h from previsions_par_semaine where annee =  ? and num_semaine = ? order by prevision_pers_h asc"
        jkcur.execute(queryHpers,(an,num_semaine))
        print("TEST ---- curseur != None (la charge de la semmaine)")
        self.assertNotEqual(jkcur, None)
        sem_hpers = jkcur.fetchone()[0]
        print( "hpers " + str(sem_hpers))
        queryModeles = "select id, nb_quarts, duree_quart, nb_equipes_par_quart, nb_employe_par_equipe, jours_trav_par_semaine, ((nb_quarts * duree_quart * nb_equipes_par_quart * nb_employe_par_equipe)) as hp from modele_affectations order by hp asc, nb_quarts asc, nb_equipes_par_quart asc"
        #la requête ordonne en préférant le nb heures , le nb de quarts et le nb equipes minimaux (si h est pareil), dans cet ordre.
        jkcur.execute(queryModeles)
        id_mod = 0
        for row in jkcur.fetchall():
            print(row)
            h_quot = sem_hpers / row[5]
            print("la charge hebdo. de %d implique  %d heures par jour (%d) " % (sem_hpers, h_quot, row[5] ))
            #print(str(row))
            print(" query modele %d >= hquot %d ?" % (row[6],h_quot))
            if row[6] >= h_quot : #le nb heures le plus rapproché dans le modele
                query_mod_hres = row[6]
                id_mod = row[0]
                print("\nTEST 1 ---- modele trouvé ! (%d, id %d) >= que charge travail (%d)" % (
                    query_mod_hres, id_mod, h_quot))
                break
            else:
                # print("pass")
                continue
        # le modele
                self.assertGreaterEqual(query_mod_hres,h_quot)

    def test_5liste_equipes(self):
        """
        Avec les param de modele trouvé plut tôt, on a le nb équipes et emp par equipes et nb de quarts.
        Donc, nb_eq * nb_quarts = nb_leads à affecter (liste equipes) (emp_reste = nb_emp_par_eq - 1);
        S'en suit l'affectation des equipes avec les niveaux autres que leads tq emp_reste < query.
        """
        an = self.an
        num_semaine = self.num_semaine
        self.la_conn = ma_connect()
        jkcur = self.la_conn.conn.cursor()
        query_mod_hres = sem_hpers = 0
        queryHpers = "select prevision_pers_h from previsions_par_semaine where annee =  ? and num_semaine = ? order by prevision_pers_h asc"
        jkcur.execute(queryHpers,(an,num_semaine))
        sem_hpers = jkcur.fetchone()[0]
        queryModeles = "select id, nb_quarts, duree_quart, nb_equipes_par_quart, nb_employe_par_equipe, jours_trav_par_semaine, ((nb_quarts * duree_quart * nb_equipes_par_quart * nb_employe_par_equipe)) as hp from modele_affectations order by hp asc, nb_quarts asc, nb_equipes_par_quart asc"
        jkcur.execute(queryModeles)
        #charge de la semaine / jours travaillés par semaine dans le modele
        id_modele = 0
        for row in jkcur:
            h_quot = sem_hpers / row[5]
            if row[6] >= h_quot:  # le nb heures le plus rapproché dans le modele
                query_mod_hres = row[6]
                id_mod = row[0]
                print("\nTEST 2 ---- modele trouvé ! (%d, id %d) >= que charge travail (%d)" % (
                    query_mod_hres, id_mod, h_quot))
                break
            else:
                # print("pass")
                continue
                #equipes --leads
        liste_leads = []
        #soit une charge de 150 heures pour une semaine donnée
        # prédéfini: 5 jours semaine, même modele chaque jour (répétition equipe sauf non-dispo)
        #1- répartir cette charge sur une semaine (5 jours)
        #2- 150/5 = 30 h par jour
        #3- diviser 30 par h_par_quart (7.5) = 4 personnes
        #4- trouver le modele (à reviser)
        jkcur = self.la_conn.conn.cursor()
        queryLeads = "select * from employe where anciennete > 55 and niveau >= 3 order by niveau desc"
        jkcur.execute(queryLeads)


