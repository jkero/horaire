import locale
import calendar
from datetime import timedelta, datetime
from tests_connection import ma_connect

class LaSemaine:
    annee = 0
    la_num_semaine = 0
    connection = ma_connect()
    premier_jour_semaine = 0
    @staticmethod
    def utilitaire_prem_jour_sem(j): #obtenir la date du preier jour de la semaine donnee
        prem_jour = "monday" if (j == 0) else "sunday" if (j == 6) else "monday"
        # "SELECT STR_TO_DATE('200442 sunday', '%X%V %W')"
        querySemaine = "select annee, num_semaine, str_to_date(concat((?),(?), ?), '%X%V %W') as jour from previsions_par_semaine where num_semaine = ?"
        jkcur = LaSemaine.connection.conn.cursor()
        jkcur.execute(querySemaine, (LaSemaine.annee, LaSemaine.la_num_semaine, prem_jour, LaSemaine.la_num_semaine))
        return jkcur.fetchone()[2]

    @staticmethod
    def renseigne_jours_semaine(premier_jour_semaine, an, num_semaine):
        LaSemaine.annee = an
        LaSemaine.la_num_semaine = num_semaine
        LaSemaine.premier_jour_semaine = premier_jour_semaine
        calendar.setfirstweekday(premier_jour_semaine)
        locale.setlocale(locale.LC_ALL, 'fr_CA.utf8')
        les_jours = []
        if LaSemaine.premier_jour_semaine == 0:
            les_jours = [['Lundi', ''], ['Mardi', ''], ['Mercredi', ''], ['Jeudi', ''], ['Vendredi', ''], ['Samedi', ''], ['dimanche', '']]
        elif LaSemaine.premier_jour_semaine == 6:
            les_jours = [['dimanche', '']['Lundi', ''], ['Mardi', ''], ['Mercredi', ''], ['Jeudi', ''], ['Vendredi', ''], ['Samedi', '']]

        #lundi = datetime.strptime(self.utilitaire_lundi() , '%Y-%m-%d')
        #print("lundi type %s" % type(self.utilitaire_prem_jour_sem(6)))
        incr = -1
        for j in les_jours:
            incr = incr + 1
            les_jours[incr][1] = (LaSemaine.utilitaire_prem_jour_sem(premier_jour_semaine) + timedelta(days=incr)).strftime('%Y-%m-%d %H:%M')
        #print("\n" + str(les_jours))
        return les_jours


# if __name__ == '__main__':
#    list_jours = LaSemaine.renseigne_jours_semaine(6,2024,6)
#     LaSemaine.annee =2024
#     LaSemaine.la_num_semaine = 6
#     j = LaSemaine.utilitaire_prem_jour_sem(0)
#     print(j)
#    print(list_jours)

