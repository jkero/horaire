/*
 trouver pour une semaine donnee le total des employes dispo
    --donc chercher ceux dont fk_non_dispo = NULL
 union
  ceux dont il y a une fk et dont 
  les dates de non dispo != date de semaine en cours. 
  
 select employe.nom, emp_non_dispo.debut from employes
 inner join emp_non_dispo
 on non_dispo_fk = id
  select strftime('%W','now') 
 select employes.nom, emp_non_dispo.t_exact_debut from employes
 inner join emp_non_dispo
 on non_dispo_fk = emp_non_dispo.id */
 
select employes.nom from employes 
inner join emp_non_dispo
on employes.non_dispo_fk = emp_non_dispo.id
where
"2022-02-20 08:00" BETWEEN emp_non_dispo.t_exact_debut AND emp_non_dispo.t_exact_fin
 

 
 