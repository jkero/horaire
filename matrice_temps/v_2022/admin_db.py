# modifié 14 janv 2022 13-18h

# pseudo code pour admin db employe et prod. horaire + fdt

#tables: employes / quarts(auto) /t_assigne_equipes(auto) /equipes(auto) /periode / emp_non_dispos/ (UI ADM-6 - insertions nouveaux employés, admin employés)

# le produit final est une table qu'on peut interroger comme horaire ou fdt.

#pré-condition: (UI ADM-01) table des heures/personnes prévues pour une période déterminée. Ensuite, pour une période donnée
# on dérive le nb_employes requis et le nb équipes à former et assigner aux quarts

# tables des quarts (UI ADM-02) pour une période donnée, déterminer le nb de quarts v. (R. 13.a)

# composer table équipes (vide) la periode donnee (YYYY-mm-dd hh:mm) nb equipe = tb_/heurespersonnes.total / max_par_equipe % quarts (R.14)

# tables des équipes (UI ADM-03a onglet) visuel; assignation employés par équipe (UI ADM-03b onglet) visuel

#regles:  nb_empl_dispo(R.1.) /nb_max_par_equipe(R.2.) = nb_equipe_estimé

# --1 assigner les équipes aux quarts(R.3.) rotation automatique (équipe de fds, equip de sem.)
# --2 assigner les employes aux équipes -- appliquer validations "fds" et "temps max"

#********** il se peut que les règles de gestion par employées et non dipso soient les seules importantes, équipes sont des contenants,
# leur renseignement est soumis aux validations des non-dispos ************************

# un horaire est fait pour une semaine(num période).
# pour chaque jour e la periode (R.5. fds?) il y a des quarts de travail pour lesquels on assigne des équipes (R.4. répétitions etc.)

# R.6. valider temps max travail pour employes -comment compter le temps assigné (horaire, pas fdt) pour chaque emp ?
# R.6.a temps des quarts, contenu des équipes de quart. Calcul en h/pers ?
#R.7 validation des fds (non-dispo type1 fds rotative? type2 non-dispo autre) employes
#R.8. validation rotation des équipes
#R.9 cohérence equipes/employé v. periode off/fds
#   si je mets employé x dans eq A et que Eq A fait 08-16 pour une période de congéde employé (R.10), il faut recommencer assignation_equipe.

#R.10. comment calculer période repos employé (2 jours de sem. consec alternant avec sam+dim) : renseigner
# la table des nos-dispos employes avec type 1 à l'avance (creation_employe avec sequence non_dispo type1 (genre vsdlm/mjvlm))? Donc en balayant la tb employées pour assigner equipes, valider dispo?
# R.11. séquences des paires de congés (non-dispo) type 1 (sd/[sd][lm][mm][mj][jv])

#--3 renseigner l'horaire

# periode(sem#)
# rangée quarts n colonnes selon distribution des quarts (tests avec 8-16 12-20 15 24)
#rangée jour 1 assignation équipe par quart
# jour 2 à 7 idem

# lord de la création de l'horaire on dérive une table d'assignations pour fdt et paye ?
# l'horaire produit est archivé dans une table spéciale ou struct de données.

# présentation de l'horaire (UI ADM-4) et/ou exportation en txt/excel/autre ?

# rapport employés/heures assignées (UI ADM-5) / total hres/personnes v. prévisions, etc

# R.12. concillier nb équipes et nb quarts. 3 quarts et 5 équipes ??
# R.13. non-dispo type 13 : quarts-non_dispo.
#R.13.a : règle de gestion pour création des quarts (créneaux par jour par semaine -- avant assigner les équipes)
# R.14. nb equipe v. nb quarts v. hres/personnes : penser la logique.