SELECT DISTINCT p.name
FROM directors as d
JOIN ratings as r on d.movie_id = r.movie_id
JOIN people as p on d.person_id = p.id
WHERE r.rating >= 9.0;
