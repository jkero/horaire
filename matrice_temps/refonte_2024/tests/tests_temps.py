import sys, datetime
import locale
import calendar
from datetime import datetime, date, timedelta
import traceback, sqlite3
from sqlite3 import Error
from urllib.parse import urljoin
import os.path
import unittest


class test_semaine:

    les_jours = []
    auj = ''
    conn = None
    dbfile = urljoin("..", "letemps2024.db")
    dict_modele_vals = {}


    def __init__(self, la_journee):
        self.auj = datetime.fromisoformat(la_journee)
        self.week = str(self.auj.isocalendar()[1])
        #print("semaine # "+ str(self.week))
        self.semaine()
        try:
            self.create_connection(self.dbfile)
            self.post_init()
        except Exception as e:
            print(e)
            traceback.print_exc(file=sys.stdout)

    def post_init(self):
        try:
            if self.conn is not None:
                print("connecté à "+ self.dbfile)
        except Exception as e:
            print(e)

    def create_connection(self,
                          db_file):  # //TODO reorganiser le code sasn rapport avec la connection (sortir de cette methode)
        """ create a database connection to a SQLite database """
        try:
            self.conn = sqlite3.connect(db_file)
            if self.conn is not None:
                count = 0
                # for key in self.equipes_maximales:
                #     if count < round(self.employes_requis/self.max_emp_par_equipe):
                #         self.equipes[key] = self.equipes_maximales[key]
                #         count  = count + 1
            else:
                print("Error! cannot create the database connection.")

        except Error as e:
            print(e)
    def semaine(self):
            calendar.setfirstweekday(6)
            locale.setlocale(locale.LC_ALL, 'fr_CA.utf8')
            self.les_jours = [['Lundi', ''], ['Mardi', ''], ['Mercredi', ''], ['Jeudi', ''], ['Vendredi', ''], ['Samedi', ''],['dimanche', '']]
            lundi = self.auj + timedelta(days=-self.auj.weekday())
            #print('lundi ' + str(lundi))
            incr = self.auj.weekday()
            #print("aujour jour "+ str(incr))
            for jours in self.les_jours:
                #print(incr)
                jours[1] = (self.auj + timedelta(days=-incr)).strftime('%Y-%m-%d')
                #print(str(jours))
                incr = incr - 1
            #print("\n" + str(self.les_jours))

# def get_model_values(self, week_num):
#     model_query = self.conn.cursor)


if __name__ == "__main__":
    test_semaine('2024-01-12 11:49')