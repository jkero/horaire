Cas d'utilisation
=================

Général
-------
    #. Comme gestionnaire, je veux automatiser la création d'horaires.
    #. Comme employé, je veux pouvoir consulter mon horaire de travail et optionnellement mes tâches.
    #. Comme gestionnaire, je veux optimiser la création et la gestion des feuilles de temps.
    #. Comme employé, je veux optimiser la production de ma feuille de temps, normalement basée sur l'horaire de travail.

Données
-------
    #. L'horaire créé doit montrer un calendrier hebdomadaire ou bi-hebdomadaire ou, optionnellement, mensuel, dans lequel on voit qui travaille à quelle date-heure.
    #. L'horaire doit affficher les quarts ou créneaux dans lesquels sont affectés les employés/équipes.
    #. Les employés sont optionnellement regroupés en équipes, auquel cas ce sont celles-ci qui figurent sur l'horaire. Les équipes et leurs composition sont définies ailleurs que sur l'horaire, autre onglet ou autre page.

Conditions
++++++++++
* Une liste générale des employés doit être accessible ainsi que l'information à jour pour les non-disponibilités des employés. Ces informations doivebt être sous forme d'enregistrements dans la base de données retenue pour l'application. Selon l'interface de l'application, ces informations peuvent être maintenues dans l'application ou indépendamment d'elle.
* L'application emploie un modèle prévisionnel reflétant les exigences en heures de travail pour des semaines à venir.

Paramètres
----------
#. Comme gestionnaire, je veux créer des scénarios applicables sur des semaines précises, scénarios qui déterminent les heures de travail totales, la quantité de quarts, d'équipes, d'équipes par quart, de personnes par équipes, d'heures par quart. À la création de l'horaire, les scénarios seront alors reflétés dans les affectations.


