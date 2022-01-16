select employes.id, employes.nom, strftime('%W', emp_non_dispo.t_exact_debut) from employes
inner join emp_non_dispo
on employes.non_dispo_fk = emp_non_dispo.id