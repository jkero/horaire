select p.hpers, p.heures_par_jour, m.nb_emp_par_eq as nb_max_par_eq, 
round(p.hpers / p.heures_par_jour,1) as nb_quart_indivi, m.nb_eq,
round(round(p.hpers / p.heures_par_jour,1)/m.nb_emp_par_eq,1) 
as nb_quarts_eq, round(round(p.hpers / p.heures_par_jour,1) /(m.nb_emp_par_eq *
m.nb_creneau_quart_jour * m.nb_eq_creneau),1) as jours  

from previsions_hpers as p

inner join modele_assignation_hebdo as m

where m.id = 1 
--on p.modele = m.id 
