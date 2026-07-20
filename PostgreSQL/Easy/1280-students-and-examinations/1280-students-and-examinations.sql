-- Write your PostgreSQL query statement below

select 
    s.student_id,
    s.student_name,
    subs.subject_name,
    COUNT(e.subject_name) as attended_exams
from students s
cross join subjects subs
left join examinations e on s.student_id = e.student_id and subs.subject_name = e.subject_name
group by s.student_id, s.student_name, subs.subject_name
order by s.student_id, subs.subject_name;