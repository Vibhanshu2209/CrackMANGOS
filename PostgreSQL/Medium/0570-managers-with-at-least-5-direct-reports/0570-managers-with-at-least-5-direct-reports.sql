-- Write your PostgreSQL query statement below

select 
    e.name as name
    from employee e
join employee e2 on e.id = e2.managerId
group by e.id, e.name
having count(*) >= 5;
