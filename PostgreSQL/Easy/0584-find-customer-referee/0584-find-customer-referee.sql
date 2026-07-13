-- Write your PostgreSQL query statement below

select c.name from customer c where c.referee_id is null or c.referee_id != 2;