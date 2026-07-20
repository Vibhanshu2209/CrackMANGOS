-- Write your PostgreSQL query statement below

with exam_counts as (

    select 
        student_id,
        subject_name,
        COUNT(*) as attended_exams
    from examinations
    group by student_id, subject_name
)
select 
    s.student_id,
    s.student_name,
    sub.subject_name,
    COALESCE(ec.attended_exams, 0) as attended_exams
from students s
cross join subjects sub
left join exam_counts ec 
on ec.student_id = s.student_id and ec.subject_name = sub.subject_name
order by s.student_id, sub.subject_name;