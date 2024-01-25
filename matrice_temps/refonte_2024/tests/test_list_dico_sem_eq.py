"""Pour en finir avec les structures de structures"""

# de la plus petite structure à la plus grande

# liste d'équipe (venant de fusion liste de leads et liste des autres)
    # n listes d'équipes
        #dictionnaire de jours de semaine (K = date)
            # liste de dictionnaires de jours de semaine
                #dictionnaire ou liste de la semaine
from collections import defaultdict

emp_num1 = 'emp01'
emp_num2 = 'emp02'
emp_num3 = 'emp03'
emp_num4 = 'emp04'
emp_num5 = 'emp05'
emp_num6 = 'emp06'
nom1 = 'nom01'
nom2 = 'nom02'
nom3 = 'nom03'
nom4 = 'nom04'
nom5 = 'nom05'
nom6 = 'nom06'
prenom1 = 'prenom01'
prenom2 = 'prenom02'
prenom3 = 'prenom03'
prenom4 = 'prenom04'
prenom5 = 'prenom05'
prenom6 = 'prenom06'

liste_equipes_par_jour =[]
t = {'team1':[[[emp_num1],[nom1],[prenom1]],[[emp_num2],[nom2],[prenom2]]]}
liste_equipes_par_jour.append(t)
t = {'team2':[[[emp_num3],[nom3],[prenom3]],[[emp_num4],[nom4],[prenom4]]]}
liste_equipes_par_jour.append(t)
t = {'team3':[[[emp_num5],[nom5],[prenom5]],[[emp_num6],[nom6],[prenom6]]]}
liste_equipes_par_jour.append(t)

# print(liste_equipes_par_jour[0]) #premiere equipe
# print(liste_equipes_par_jour[0]['team1'])#liste premiere equipe
# print(liste_equipes_par_jour[0]['team1'][1]) #2e enr. employe sur la liste de premiere equipe
# print(liste_equipes_par_jour[0]['team1'][1][0]) # num_employe du 2e enr. sur la liste de premiere equipe
#
# for i in range(len(liste_equipes_par_jour)):
#     print(str(i) + "  "+ str(liste_equipes_par_jour[i]))

#liste_jours = [['Lundi'], ['Mardi'], ['Mercredi'], ['Jeudi'], ['Vendredi'], ['Samedi'], ['dimanche']]
liste_jours = ['Lundi','Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'dimanche']

liste_semaine = []

for j in range(len(liste_jours)):
    t = {}
    t[liste_jours[j]] = liste_equipes_par_jour
    liste_semaine.append(t)

print(liste_semaine)

for j in range(len(liste_jours)):
    print([liste_jours[j]])
    print(liste_semaine[j][liste_jours[j]])


