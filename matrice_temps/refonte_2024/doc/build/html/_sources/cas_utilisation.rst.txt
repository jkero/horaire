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
* Types de conditions: avoir un employé *permanent* désigné comme leader pour chaque équipe, donc info employé doit contenir statut conventionnel.

Paramètres
----------
#. Comme gestionnaire, je veux créer des scénarios applicables sur des semaines précises, scénarios qui déterminent les heures de travail totales, la quantité de quarts, d'équipes, d'équipes par quart, de personnes par équipes, d'heures par quart. À la création de l'horaire, les scénarios seront alors reflétés dans les affectations.

À déterminer
------------
Règles pour l'affectation des équipes. Pour le moment on sélectionne les disponibles et on réaffecte les mêmes (s'ils sont disponibles) le jour suivant (la rotation pourrait se faire selon le roulement des quarts peu importe les heures ou le jour).

C'est ici que l'affectation devra tenir compte des heures travaillées consécutives de chaque employé et tenter d'appliquer des règles de convention collective.

Par ailleurs, la distinction entre les employés séniors/chefs d'équipe n'est pas faite. Idéalement une règle serait d'avoir une liste de chefs d'équipe/séniors/permanents/temps plein/ dont un membre est la première personne à affecter à une équipe donnée. Ensuite, les autres employés sont choisis selon a) des compétences b) leur statut partiel/permanent/ c) les heures déjà effectuées dans la semaine d) la période de repos



