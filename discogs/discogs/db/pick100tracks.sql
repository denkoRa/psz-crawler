SELECT t.title, count(ct.idcollection) as CNT
FROM track t
INNER JOIN collection_track AS ct ON ct.idtrack = t.idtrack
GROUP BY t.idtrack
ORDER BY cnt DESC
LIMIT 100