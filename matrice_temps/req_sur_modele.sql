select previsions_hpers.hpers, previsions_hpers.heures_par_jour, modele_assignation_hebdo.nb_emp_par_eq as nb_max_par_eq, 
round(previsions_hpers.hpers / previsions_hpers.heures_par_jour,1) as nb_quart_indivi, 
round(round(previsions_hpers.hpers / previsions_hpers.heures_par_jour,1)/modele_assignation_hebdo.nb_emp_par_eq,1) 
as nb_quarts_eq, round(round(previsions_hpers.hpers / previsions_hpers.heures_par_jour,1) /(modele_assignation_hebdo.nb_emp_par_eq *
modele_assignation_hebdo.nb_creneau_quart_jour * modele_assignation_hebdo.nb_eq_creneau)) as jours  

from previsions_hpers

inner join modele_assignation_hebdo

where modele_assignation_hebdo.id = 1 
--on previsions_hpers.modele = modele_assignation_hebdo.id 
