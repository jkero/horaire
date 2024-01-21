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
    def test_etablir_conn(self):
        self.la_conn = ma_connect()
        print("TEST ---- connection != None")
        self.assertNotEqual(self.la_conn.conn,None)
        #self.getLeads()

    def test_getLeads(self):
        self.la_conn = ma_connect()
        jkcur = self.la_conn.conn.cursor()
        queryLeads = "select * from employe where anciennete > 55 and niveau >= 3 order by niveau desc"
        jkcur.execute(queryLeads)
        print("TEST ---- query niveau des employes != None")
        self.assertNotEqual(jkcur, None)
        for emp in jkcur:
            print(" %s, %s, n = %d" % (emp[2],emp[3],emp[7]))

    def test_get_hpers(self):
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

    def test_ventile_hpers_v_modeles(self):
        """ pour un nombre n, pour chaque modele disponible
            par ordre de modele resource disponible,
                si n/modele ressource > 1 (le modele prevoit ou non une config pour ce nombre)
                    passe au modele suivant
                sinon
                    utiliser le modele.
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
        queryModeles = "select *, (nb_quarts * duree_quart * nb_equipes_par_quart * nb_employe_par_equipe) as hp from modele_affectations order by hp asc, nb_quarts asc, nb_equipes_par_quart asc"
        #la requête ordonne en préférant le nb heures , le nb de quarts et le nb equipes minimaux (si h est pareil), dans cet ordre.
        jkcur.execute(queryModeles)
        for row in jkcur.fetchall():
            #print(str(row))
            # 3: nb_quart 4:h par quart 5:nb_equipes 6:emp_par_eq 7: le produit des précédentes
            print(str(row[7]))
            if sem_hpers > row[7]: #le nb heures le plus rapproché dans le modele
                #print("pass")
                continue
            else:
                query_mod_hres = row[7]
                print("+++++")
                print(row)
                print("+++++")
                break
        # le modele
        print("TEST ---- modele trouvé (%d) >= que charge travail (%d)" % (query_mod_hres,sem_hpers))
        self.assertGreaterEqual(query_mod_hres,sem_hpers)



