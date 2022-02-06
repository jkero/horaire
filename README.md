# Horaire

Juste une classe de pratique (un prétexte) pour jouer avec Python. En soi, c'est une appli qui gère des équipes à assigner sur une semaine de travail; il y a un pool d'employés et modèle de gestion (sqlite). En fait ça prend 7 tables dans sqlite. Ça pourrait utiliser fichier de configration (xml ou txt par exemple), ici c'est une query dans sqlite).

Une fois vérifiées les non-dispos des "employés" et comment on répartit les équipes et les équipiers sur la semaine, jours et créneaux, on écrit le tout sur un workbook excel (voir images [ici](/matrice_temps/la_doc_test/doc/source/_static/).

Joué avec python, sqlite, sphinx (quelques problemes avec python 3.10), pas grand chose de plus comme exigences. Peut-être la lib xslwriter pour générer un fichier excel (générer c'est vite dit, il faut tout gérer...)
