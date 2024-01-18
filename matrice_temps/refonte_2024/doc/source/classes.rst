Classes
=======

.. uml::

    @startuml
        class employe{
                    id: int
                    num_emp: varchar
                    nom: string
                    prenom: string
                    anciennete: int
                    pref_creneau_deb: datetime
                    pref_creneau_fin: datetime
                    niveau: int
                    }
        note left
            niveau détermine
            anciennete + leads
        end note
        class non_dispos{
                        id:int
                        debut: datetime
                        fin: datetime
                        type: string
                        ref: string
                        FK_employe(id) int
                    }
        class modele_affectations{
                    id: int
                    nom; string
                    description: string
                    nb_quarts: int
                    duree_quart: decimal
                    nb_equipes_par_quart: int
                    nb_employe_par equipe: int
                    }
        class prev_num_semaine{
                    id: int
                    annee: int
                    num: int
                    prev_h_pers: int
                    FK_modele_affectation(id) int
                    }
        employe "1" --> "n" non_dispos : a soumis
        modele_affectations "1" --> "n" prev_num_semaine
    @enduml