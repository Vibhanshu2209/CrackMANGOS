-- Write your PostgreSQL query statement below

select tweet_id from tweets where CHAR_LENGTH(content) > 15;