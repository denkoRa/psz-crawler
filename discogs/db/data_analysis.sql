
--Koliko zapisa pripada svakom zanru
SELECT name, COUNT(*)
FROM collection_genre
GROUP BY name

--Koliko zapisa pripada svakom stilu
SELECT name, COUNT(*)
FROM collection_style
GROUP BY name

--Rang lista prvih 10 albuma (ili vise ako ima neresenih) po broju izdatih verzija
SELECT @th := release_count
FROM album
ORDER BY release_count DESC
LIMIT 9, 1

SELECT *
FROM album
WHERE release_count >= @th

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
