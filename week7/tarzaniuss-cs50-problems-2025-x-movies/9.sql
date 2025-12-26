SELECT DISTINCT people.name
FROM stars
JOIN people on stars.person_id = people.id
JOIN movies on stars.movie_id = movies.id
WHERE movies.year = 2004
ORDER BY people.birth
