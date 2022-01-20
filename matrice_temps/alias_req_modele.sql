select p.hpers, p.heures_par_jour, round(p.hpers / p.heures_par_jour,1) as presences, m.nb_eq,m.nb_emp_par_eq as nb_par_eq, 
round(round(p.hpers *1.0 / p.heures_par_jour,1)/m.nb_emp_par_eq,1) 
as nb_quarts_eq, m.nb_eq_par_creneau, m.nb_creneau_disp ,round(round(cast(p.hpers as float) / p.heures_par_jour,2) /(m.nb_emp_par_eq *
m.nb_eq_par_creneau * m.nb_creneau_disp),2) as jours, m.nom  

from previsions_hpers as p

inner join modele_assignation_hebdo as m

--where m.id = 2
on p.modele = m.id 
