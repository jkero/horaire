Vrac pseudo-code
================

1- Obtenir p_aramètres modèle (selon semaine horaire)

2- Créer dictionnaire équipes

3- Créer dictionnaire semaine

4- Dans la liste générale des employés:

    sélectionner *p_nb_eq* seniors/leads et garder dans v_leads[]

    cpt_eq = 0

    TQ cpt_eq <= *p_nb_eq*  //param de modele

        vérifier dispo/conflit(v_leads[cpt_eq])

        vérifier heures travaillees (v_leads[0]) (v. heures normales conv.)

            si ht + *p_h_par_quart* >  h_conv

                émettre message surtemps ou passer au suivant (R?)

            sinon

                affecter v_leads[cpt_eq]) dans d_eqp[cpt_eq] //list(dico)[ix]

                cpt_eq++

# répéter étape 4 mais pour les employés non-lead et remplir équipes


.. note::
    Le nombre d'équipes est déterminé par le modèle désigné lors de la requête dans la table prev_num_semaine. C'est la prévision budgétaite en heures-personnes. Pour éclaircir le calcul: supposons qu'une tâche requiert 1000 heures-personnes alors si je divise par 25 (personnes), ça indique que que 25 personnes travaillant 40 heures pourraient théoriquement accomplir la tâche (en une semaine de 40 h). Ça pourrait être 5 équipes de 5, 2 équipes de 2 (en 6 semaines 1/4), etc. Pour les besoins de l'application, j'essaie de limiter les modèles et les tests pour générer un horaire sur un calendrier d'une semaine. Rien n'est fixe et je pourrais affecter des employés ad vitam aeternam sur un projet d'un milliard d'heures....

.. todo:: (dans scratch.py) methodes pour tester prefetch des leads, faire une passe partielle pour affecter chaque lead par equipe (après avoir testé/calculé valeur modele prev); ensuite finier affecter equipes avec autres non-leads (pourraient être récupérés à la passe leads)

.. todo:: Calculs simu pour les modeles et les valeurs qui serviront au xlsx

.. todo:: aussi contraintes de type calendrier

.. todo:: ecrire template pour modele xlsx (rangees, colonnes, plages nommees, onglets, etc.)

Pour tests
++++++++++

*Automatiser* la décision pour les équipes et les quarts, le seul paramètre à l'entrée est le nombre prévu de heures-personnes. Ensuite c'est un calcul basé sur le salaire moyen donc, *in fine*, les heures de jour (quart de jour seulement) et la quantité de personnel que le modèle propose.

À la base il y a déjà un modèle assigné pour chaque semaine, on va essayer de reviser et réécrire.

Remarque: si une projet a 10 employés à 8 heures pas jour, normalement il devrait pouvoir soutenir et saisir des semaines de 8 h * 10 pers * 5 jours = 400 hpers par semaine. Je suppose que ça prend une cohérence dans l'entrée de données. Ma db a une liste de 33 employes, avec des niveuax différents (lead, temps partiel, etc.) Il y a de quoi faire pas mal de règles.

Devrais-je ajouter un indicateur de surtemps dans la db ou alors c'est automatique selon la valeur de hpers ? Pour les tests je dois restreindre les paramètres et la portée. C'est la table des prévisions qui doit porter une partie de la cohérence, alors que cette app doit constituer des équipes et des quarts dans un calendrier. OK.

Donc, j'ai une table de modeles triée par hpers mais aussi par nb quarts, nb_equipes_par_quart (emp par équipe pourrait aussi être utilisé pour les hp égales..)

* 1 quart de jour < 2 quarts de jour < 3 quarts de jour;

* équipe(2) < equipe(3), etc.;

* Durée quart 7.5 < durée sup à 7.5 (surtemps)

modele = trier(t_mod).next \\trouver les modèles disponibles et les trier par (nbq * dq * nbeqq * nbempq)

tq modele:
    si hpers / nbquarts * dureequarts * nbequipequart * nbemployeparequipe > 37.5 (40) //règle déterminée ailleurs
    alors
    passer au modèle suivant


Sèlection des éuipes
+++++++++++++++++++++
MariaDB [horaire]> select * from employe where anciennete > 55 and niveau >= 3;
