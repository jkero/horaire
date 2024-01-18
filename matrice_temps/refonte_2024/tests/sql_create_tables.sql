drop table employe;
create table employe (id smallint unsigned not null auto_increment primary key,
num_emp varchar(7) not null,
nom varchar(40) not null,
prenom varchar(40) not null,
anciennete smallint not null,
pref_creneau_deb datetime,
pref_creneau_fin datetime,
niveau smallint
) engine = InnoDB;

insert into test_temps (une_date, un_stamp) values ('2024-1-1 12:01','2024-2-1 17:01')

insert into employe(num_emp,nom,prenom,anciennete,pref_creneau_deb,pref_creneau_fin,niveau) values('jk_001', 'Kéroack','Jacques', 30, '2024-1-1 07:00','2024-1-1 15:00', 4)

create table non_dispo (id_dispo smallint unsigned not null auto_increment primary key,
creneaux varchar(240) not null,
emp_id smallint unsigned not null,
constraint `FK_emp`
foreign key (emp_id) references employe(id)
on delete cascade
) engine = InnoDB;

insert into non_dispo(creneaux, FK_emp) values ('2025-03-18 08:00@2025-03-28 17:00')

select id,nom, prenom, creneaux from employe right join non_dispo on employe.id = non_dispo.emp_id;

create table modele_affectations (id smallint unsigned not null auto_increment primary key,
nom varchar(240) not null,
description varchar(240),
nb_quarts int not null,
duree_quart decimal(2,1) unsigned zerofill not null,
nb_equipes_par_quart int,
nb_employe_par_equipe int
) engine = InnoDB;

insert into modele_affectations(nom, description, nb_quarts, duree_quart, nb_equipes_par_quart, nb_employe_par_equipe) values ('minimal', 'Pas ou peu de travail', 1, 7.5, 1,2);

create table previsions_par_semaine (id smallint unsigned not null auto_increment primary key,
annee int,
num_semaine int,
prevision_pers_h decimal(6,1) unsigned zerofill not null,
modele_id smallint unsigned not null,
constraint `FK_modele`
foreign key (modele_id) references modele_affectations(id)
on delete cascade
) engine = InnoDB;

insert into previsions_par_semaine(annee,num_semaine,prevision_pers_h, modele_id) values (2025,52,30,1);

select * from modele_affectations as p right join previsions_par_semaine as r on r.id = p.id;

**remarque windows: Load infile avec double \\ pour path, pas de "local"


