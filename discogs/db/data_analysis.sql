
--Koliko zapisa pripada svakom zanru
SELECT g.name, COUNT(*)
FROM collection_genre AS cg
INNER JOIN genre AS g ON g.name = cg.name
GROUP BY name

--Koliko zapisa pripada svakom stilu
SELECT s.name, COUNT(*)
FROM collection_style AS cs
INNER JOIN style AS s ON s.name = cs.name
GROUP BY name

--Rang lista prvih 10 albuma (ili vise ako ima neresenih) po broju izdatih verzija
SELECT release_count
FROM album
ORDER BY release_count DESC
LIMIT 9, 1

SELECT title, release_count, year, track_count, avg_rating
FROM album
WHERE release_count >= @th
ORDER BY release_count DESC

--Top 50 osoba sortirane po najvecem generalnom rejtingu na svojim pesmama 
--Da bi bilo znacaja u rezultatu, mora da je izdato vise od 10 izdanja
SELECT A.idartist, A.name, COUNT(R.idrelease ),AVG(R.avg_rating) AS rating
FROM artist AS A
INNER JOIN discogs.release AS R ON R.idartist = A.idartist AND R.avg_rating IS NOT NULL
GROUP BY A.idartist
HAVING COUNT(R.idrelease) > 10
ORDER BY rating DESC
LIMIT 50

--Top 50 osoba po broju ucesca kao vokal
SELECT A.idartist, A.name, COUNT(*)
FROM artist AS A
INNER JOIN credit AS C ON A.idartist = C.idartist
WHERE C.role_name LIKE '%Vocals%'
GROUP BY A.idartist
ORDER BY COUNT(*) DESC
LIMIT 50

--Top 50 osoba po broju napisanih pesama
SELECT A.idartist, A.name, COUNT(*)
FROM artist AS A
INNER JOIN credit AS C ON A.idartist = C.idartist
WHERE C.role_name LIKE '%Written-By, Arranged By%'
GROUP BY A.idartist
ORDER BY COUNT(*) DESC
LIMIT 50


--Top 100 tracks that appear on most albums
SELECT t.title, count(ct.idcollection) as CNT
FROM track t
INNER JOIN collection_track AS ct ON ct.idtrack = t.idtrack
GROUP BY t.idtrack
ORDER BY cnt DESC
LIMIT 100


--Task 3

--Releases per decades
SELECT (r.released div 10 * 10) AS decade, COUNT(*)
FROM discogs.release AS r
WHERE r.released IS NOT NULL
GROUP BY decade
ORDER BY decade 

--Top 6 genres
SELECT g.name, COUNT(cg.idcollection) AS cnt
FROM genre AS g 
INNER JOIN collection_genre AS cg ON cg.name = g.name
GROUP BY g.name
ORDER BY cnt DESC
LIMIT 6

--Cyrillic
SELECT COUNT(*)
FROM discogs.release
WHERE title REGEXP '[Ѐ-ӿ]'

--Tracks per duration
SELECT COUNT(*)
FROM discogs.track
WHERE duration IS NOT NULL AND duration BETWEEN {} AND {}

--Total albums
SELECT COUNT(*)
FROM discogs.release

--Albums per number of genres
SELECT LEAST(genre_count, 4) AS g_count, SUM(release_cnt)
FROM 
(
    SELECT genre_count, count(*) as release_cnt
    FROM
    (
		SELECT r.idrelease, COUNT(*) as genre_count
		FROM discogs.release AS r
		INNER JOIN collection_genre AS cg ON cg.idcollection = r.idrelease
		INNER JOIN genre AS g ON g.name = cg.name
		GROUP BY r.idrelease
    ) AS tmp1
    GROUP BY genre_count
) AS tmp2
GROUP BY g_count