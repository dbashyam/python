delete from aggregated_transaction
select * from aggregated_transaction where country like 'USA'
select * from aggregated_insurance
select * from aggregated_user where brand is null
select * from aggregated_user
TRUNCATE TABLE aggregated_transaction;
drop table aggregated_transaction;
drop table aggregated_user;
drop table aggregated_insurance;
