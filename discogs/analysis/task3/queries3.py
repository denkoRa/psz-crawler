_ALBUMS_PER_DECADES = """SELECT (r.released div 10 * 10) AS decade, COUNT(*)
                        FROM discogs.release AS r
                        WHERE r.released IS NOT NULL
                        GROUP BY decade
                        ORDER BY decade 
                        """

_TOP_6_GENRES = """SELECT g.name, COUNT(cg.idcollection) AS cnt
                FROM genre AS g 
                INNER JOIN collection_genre AS cg ON cg.name = g.name
                GROUP BY g.name
                ORDER BY cnt DESC
                LIMIT 6
                """

_TRACKS_PER_DURATION = """SELECT COUNT(*)
                        FROM discogs.track
                        WHERE duration IS NOT NULL AND duration BETWEEN {} AND {}
                        """

_FIND_CYRILLIC_ALBUMS = """SELECT COUNT(*)
                        FROM discogs.release
                        WHERE title REGEXP '[Ѐ-ӿ]'
                        """

_TOTAL_ALBUMS = """SELECT COUNT(*)
                FROM discogs.release"""


_ALBUMS_PER_GENRE_CNT = """SELECT LEAST(genre_count, 4) AS g_count, SUM(release_cnt)
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
                        """
                        