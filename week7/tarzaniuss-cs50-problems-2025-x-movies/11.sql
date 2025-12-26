SELECT m.title
FROM stars as s
JOIN movies as m on s.movie_id = m.id
JOIN people as p on s.person_id = p.id
JOIN ratings as r on s.movie_id = r.movie_id
WHERE p.name = 'Chadwick Boseman'
ORDER BY rating DESC
LIMIT 5
