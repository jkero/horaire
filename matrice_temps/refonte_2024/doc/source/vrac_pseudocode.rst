Vrac pseudo-code
================

1- Obtenir p_aramètres modèle (selon semaine horaire)

2- Créer dictionnaire équipes

3_ Créer dictionnaire semaine

4- Dans la liste générale des employés:

    sélectionner *p_nb_eq* seniors/leads et garder dans v_leads[]

    cpt_eq = 0

    TQ cpt_eq <= *p_nb_eq*

        vérifier dispo/conflit(v_leads[cpt_eq])

        vérifier heures travailleesv_leads[0]) (v. heures normales conv.)

            si ht + *p_h_par_quart* >  h_conv

                émettre message surtemos ou passer au suivant (R?)

            sinon

                affecter v_leads[cpt_eq]) dans d_eqp[cpt_eq] //list(dico)[ix]

                cpt_eq++
