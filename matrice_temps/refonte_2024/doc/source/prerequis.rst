Liste à faire
+++++++++++++
.. todo:: vérifier uml :octicon:`check`
.. todo:: vérifier dernière version pour xsltwriter ou autre
.. todo:: structure des règles de gestion 1- la base
.. todo:: structure des règles de gestion 1- les variantes

Par exemple: gestion des équipes, des quarts, horaires, modèles et **conventions collectives** (paramètre ancienneté pour l'affectation)

.. todo:: structure du modèle : la db, les 'presets', locale, semaine, etc. (prévisions pers-h, etc.)

.. todo:: structure uml de l'approche gestionnaire

Lors de la première version, il y a eu plusieurs chemins pour finalement générer un horaire et une liste d'équipes dans un tableur xlsx.

Dans cette nouvelle version je vais exposer des *use case* de base, du type qui veut quoi, par exemple générer à la volée un horaire basé sur les dernières données disoponibles.

Mais, quelles sont ces données et les contextes ? Service Air générait des horaires tous les dimanches et chacun avait sa copie personnalisée.

Aussi, les horaires fabriqués par les responsables à Statistique Canada étaient assez 'hot' et je me suis basé sur quelques idées que j'y ai vues pour faire cet exercice.

* Créer des équipes et
* Y assigner des personnes
* Générer une liste d'horaires par employé pour un intervalle donné (colonnes par jour et créneau horaire)

La première version crée les équipes en se basant sur un 'preset', un modèle théoriquement défini par un gestionnaire, où les quantités prévues de personnes, et tout ce qui regarde l'organisation de quarts, est inscrit (db).

Je vais représenter par un uml la logique d'exploitation de cette application (v. 1) et voir comment optimiser.

Il n'a pas été considéré de solutions d'installation (docker etc.) ou de déploiement, ou de sécurité des données , ni de tests orthodoxes. Ça pourra changer dans la v. 2.







.. uml::

    @startuml
    object liste_employes
    object employe
    object disponibilites
    object previsions_travail
    object semaines
    object pers_h
    object composition_quarts
    object calendrier
    object creation_doc_equipes
    object creation_doc_horaire_hebdo
    object nb_equipes_par_quart
    object emp_par_equip
    object nb_quarts
    object heures_quarts
    object composition_equipes
    object liste_affectations


    diamond d1

    liste_employes --> d1
    employe --> liste_employes
    disponibilites --> liste_employes
    d1 --> previsions_travail
    semaines --> previsions_travail
    previsions_travail --> composition_quarts
    pers_h --> previsions_travail
    calendrier --> composition_quarts
    composition_quarts --> creation_doc_equipes
    composition_quarts --> creation_doc_horaire_hebdo
    nb_equipes_par_quart --> composition_quarts
    nb_quarts --> composition_quarts
    composition_equipes --> composition_quarts
    emp_par_equip --> composition_equipes
    heures_quarts --> composition_quarts
    composition_quarts --> liste_affectations : "enregistrer"

    @enduml

ok there