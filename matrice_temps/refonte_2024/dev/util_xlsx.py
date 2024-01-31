"""
Cette  classe contient les appels à tous les autres utilitaires pour finalement générer un chiffrier.
Ici, les valeurs de lancement sont codées en dur.

Attributes:
     semaine  int -- codé en dur  : La semaine de l'horaire à produire
     annee  int-- codé en dur  : année
     dict_semaine -- appelé dans utilitaire : La grosse structure : dict de liste de dictionnaires de listes.  n jours -> n equipes -> membres
     date_sem_ref -- appelé dans utilitaire : Liste des jours-dates correspondant à la semaine
     aujourd -- appelé dans utilitaire : pour nom de fichier et signer l'horaire

"""
import calendar
import locale
import sys
import traceback

from datetime import datetime, date, timedelta
from util_compose_equipes import CompositionEquipes
import xlsxwriter as xl
from xlsxwriter import format

class Prod_chiffrier:
    """

    """
    prem_jour_sem = 0 # 0=lundi 6=dimanche
    semaine = 44
    annee = 2024
    dict_semaine = None
    date_sem_ref = None
    aujourd = None

    @staticmethod
    def initialise():
        """
        Cette méthde statique est appelée pour générer l'horaire
        """
        Prod_chiffrier.dict_semaine =  CompositionEquipes.get_emp_dispo(Prod_chiffrier.prem_jour_sem,Prod_chiffrier.annee,Prod_chiffrier.semaine)
        #Prod_chiffrier.print_dict(Prod_chiffrier.dict_semaine)
        Prod_chiffrier.date_sem_ref = CompositionEquipes.semaine
        e = datetime
        Prod_chiffrier.aujourd = e.today()
        nomfich = Prod_chiffrier.aujourd.strftime('%y_%m_%d_%H%M')
        wb = xl.Workbook('builds_xlsx/rev3_' + nomfich + '.xlsx')


        Prod_chiffrier.onglet_equipes(wb)
        Prod_chiffrier.onglet_modele(wb)



    @staticmethod
    def print_dict(le_dict):
        for j in le_dict:
            print(j)
            for v in le_dict.values():
                print(v)
    @staticmethod
    def onglet_equipes(wb):
        """
        La répartition à travers le ou les quarts est déterminée selon le niveau et l'ancienneté
        """
        ws = wb.add_worksheet('Équipes')
        bold = wb.add_format({'bold': True})
        cell_format_red_small = wb.add_format({'bold': False, 'font_color': 'red', 'font_size': '13','align': 'right','valign':'vcenter' })
        cell_format_noir = wb.add_format({'bold': True, 'font_color': 'black','text_wrap':'true','align':'right','valign':'vcenter'})
        cell_format_bleu = wb.add_format({'bold': False, 'font_color': 'blue', 'font_size': '15','text_wrap': 'true', 'align': 'center', 'valign': 'vcenter'})
        cell_format_vert = wb.add_format({'italic': True, 'bold': False, 'font_color': '#337722', 'font_size': '13','text_wrap': 'true', 'align': 'right', 'valign': 'vcenter'})
        cell_format_ardoise = wb.add_format({'italic': True, 'bold': False, 'font_color': '#2F4F4F', 'font_size': '12','text_wrap': 'true', 'align': 'center', 'valign': 'vcenter'})
        une_string = "Semaine # " + str(CompositionEquipes.modele.prev_num_sem) \
            + ", Nb quarts: " + str(CompositionEquipes.modele.nb_quarts) \
            + ", Nb équipes par quart: " + str(CompositionEquipes.modele.nb_equipes_par_q)  \
            + ", Nb employés par équipes: " \
            + str(CompositionEquipes.modele.nb_emplo_par_eq) + " , Heures prévues: " \
            + str(CompositionEquipes.modele.prev_heures_sem) + " Excédent " + str(CompositionEquipes.modele.excedent)  +" h , Modele : " + str(CompositionEquipes.modele.id_mod)
        ws.merge_range(0, 2, 0, 5, '')
        print(une_string)
        ws.write(0,2, str(une_string), cell_format_ardoise)
        col_quart = col_date = 1 #repères pour excel
        col_nom_equipiers = 3
        col_chef_equipe = 2
        ws.set_column('A:A', 20)
        ws.write(1,0, "Émis le :")
        ws.set_row(2, 20)
        ws.write(2, 0, Prod_chiffrier.aujourd.strftime('%y-%m-%d %H:%M'), cell_format_bleu)
        ws.set_row(0, 44)
        ws.write('A1', 'Equipes', cell_format_red_small)
        debut_donnees = row = 3
        s_equipe_jour = Prod_chiffrier.dict_semaine
        compte_jours = 0
        for date_jour in s_equipe_jour.keys():
            if compte_jours < CompositionEquipes.modele.nb_jours_sem:
                eq_pop = s_equipe_jour[date_jour]
                col = col_date # dates
                ws.set_column(1, 1, 22)
                ws.write_string(row, col, str(date_jour), cell_format_red_small)
                row = row + 1
                les_chefs = list(eq_pop) # pas plus bas : doit être poppé
                for q in range(CompositionEquipes.modele.nb_quarts):
                    row = row +1
                    #print("quart %s" % str(q+1))
                    col = col_quart
                    ws.write_string(row, col, "quart " + str(q + 1), cell_format_ardoise)
                    for eq_p_q in range(CompositionEquipes.modele.nb_equipes_par_q):
                        chef = les_chefs.pop(0)
                        col = col_chef_equipe
                        ws.set_column(col, col, 19)
                        ws.write_string(row, col, str(chef), cell_format_vert)
                        col = col_nom_equipiers
                        for equipiers in s_equipe_jour[date_jour][chef]:
                            ws.set_column(col, col, 29)
                            a = str(" %s, %s (%s)" % (equipiers[2], equipiers[3], equipiers[1]))
                            ws.write_string(row, col, a, cell_format_noir)
                            col = col + 1
                        row = row + 1
                row = row + 1    #print(eq_p_q)
            compte_jours = compte_jours + 1


    @staticmethod
    def onglet_modele(wb):
        ws = wb.add_worksheet('Modèle')
        le_modele = CompositionEquipes.modele
        cell_format_red = wb.add_format({'bold': True, 'font_color': 'red', 'font_size': '20', 'align': 'center', 'valign': 'vcenter'})
        une_string = "Semaine # " + str(le_modele.prev_num_sem) + ", Nb quarts: " + str(le_modele.nb_quarts) + ", Nb équipes par quart: " + str(le_modele.nb_equipes_par_q) + ", Nb employés par équipes: " + str(le_modele.nb_emplo_par_eq) + "Heures totales : " + str(le_modele.prev_heures_sem)
        #cell_format = wb.add_format({'bold': True, 'font_color': 'red'})
        ws.merge_range(1,1,3,25, '')
        ws.write_string(1,1, str(une_string),cell_format_red)
        wb.close()

Prod_chiffrier.initialise() #juste pourverifier quelques lignes sinon ça plante pour le moment
