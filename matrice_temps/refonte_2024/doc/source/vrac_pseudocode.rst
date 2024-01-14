Vrac pseudo-code
================

1- Obtenir p_aramètres modèle (selon semaine horaire)

2- Créer dictionnaire équipes

3_ Créer dictionnaire semaine

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