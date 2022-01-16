SELECT '2022-01-22' between 
date('2022-01-22','-6 day', 'weekday 0') 
and
date('2022-01-22','-6 day', 'weekday 0','+6 day') 