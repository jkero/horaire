import locale
import calendar
from datetime import timedelta, datetime
from tests_connection import ma_connect

class MesSemaines():
    annee = 0
    le_num_semaine = 0
    maria = ma_connect()
    lundi = ""

    def __init__(self):
        self.renseigne_jours_semaine()

    def utilitaire_prem_jour_sem(self,j):
        prem_jour = "monday" if j == 6 else "sunday"
        conn = self.maria.conn
        self.le_num_semaine = 6;
        self.annee = 2024
        # "SELECT STR_TO_DATE('200442 sunday', '%X%V %W')"
        querySemaine = "select annee, num_semaine, str_to_date(concat((?),(?), ?), '%X%V %W') as jour from previsions_par_semaine where num_semaine = ?"
        #print("TEST 1 ---- ? connection is None : " + str((conn == None)))
        #self.assertNotEqual(conn, None)
        jkcur = conn.cursor()
        jkcur.execute(querySemaine, (self.annee, self.le_num_semaine, prem_jour, self.le_num_semaine))
        return jkcur.fetchone()[2]

    def semaine(self):
        mon_lundi = self.utilitaire_prem_jour_sem(6)


    def renseigne_jours_semaine(self):
        calendar.setfirstweekday(6)
        locale.setlocale(locale.LC_ALL, 'fr_CA.utf8')
        les_jours = [['Lundi', ''], ['Mardi', ''], ['Mercredi', ''], ['Jeudi', ''], ['Vendredi', ''],
                          ['Samedi', ''], ['dimanche', '']]

        #lundi = datetime.strptime(self.utilitaire_lundi() , '%Y-%m-%d')
        #print("lundi type %s" % type(self.utilitaire_prem_jour_sem(6)))
        incr = -1
        for j in les_jours:
            incr = incr + 1
            les_jours[incr][1] = (self.utilitaire_prem_jour_sem(6) + timedelta(days=incr)).strftime('%Y-%m-%d %H:%M')
        print("\n" + str(les_jours))
        return les_jours


if __name__ == '__main__':
    MesSemaines()
