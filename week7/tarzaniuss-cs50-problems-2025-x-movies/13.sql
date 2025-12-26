SELECT p.name
FROM movies m
JOIN stars s ON m.id = s.movie_id
JOIN people p ON s.person_id = p.id
WHERE s.movie_id in
(
    SELECT movie_id
    FROM stars as s
    JOIN people p ON s.person_id = p.id
    WHERE p.name = 'Kevin Bacon' and p.birth = 1958
 )
AND p.name != 'Kevin Bacon';

