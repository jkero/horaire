select employes.id, employes.nom, emp_non_dispo.type_non_dispo, emp_non_dispo.t_exact_debut, emp_non_dispo.t_exact_fin, emp_non_dispo.type_non_dispo from employes 
inner join emp_non_dispo 
on employes.id = emp_non_dispo.id_empl_fk
