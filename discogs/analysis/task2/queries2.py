_all_queries = dict()

_COUNT_GENRES_COLUMNS = ["Genre", "Count"]
_COUNT_GENRES = """ SELECT g.name, COUNT(*)
                    FROM collection_genre AS cg
                    INNER JOIN genre AS g ON g.name = cg.name
                    GROUP BY name"""
_all_queries['genres_count'] = {'q': _COUNT_GENRES, 'c': _COUNT_GENRES_COLUMNS}

_COUNT_STYLES_COLUMNS = ["STYLE", "Count"]
_COUNT_STYLES = """ SELECT s.name, COUNT(*)
                    FROM collection_style AS cs
                    INNER JOIN style AS s ON s.name = cs.name
                    GROUP BY name"""   
_all_queries['styles_count'] = {'q': _COUNT_STYLES, 'c': _COUNT_STYLES_COLUMNS}

_10th_RELEASE_COUNT = """SELECT release_count
                        FROM album
                        ORDER BY release_count DESC
                        LIMIT 9, 1"""

_GET_ALBUMS_ABOVE_COLUMNS = ["Title", "Release Count", "Year", "Track Count", "Average Rating"]
_GET_ALBUMS_ABOVE = """SELECT title, release_count, year, track_count, avg_rating
                        FROM album
                        WHERE release_count >= {0}
                        ORDER BY release_count DESC""" 
_all_queries['top_10_albums'] = {'q': _GET_ALBUMS_ABOVE, 'c': _GET_ALBUMS_ABOVE_COLUMNS}


_ARTISTS_TOP_50_PER_RATING_COLUMNS = ["Artist", "Release Count", "Average Rating"]
_ARTISTS_TOP_50_PER_RATING = """SELECT A.name, COUNT(R.idrelease ), AVG(R.avg_rating) AS rating
                                FROM artist AS A
                                INNER JOIN discogs.release AS R ON R.idartist = A.idartist AND R.avg_rating IS NOT NULL
                                GROUP BY A.idartist
                                HAVING COUNT(R.idrelease) > 10
                                ORDER BY rating DESC
                                LIMIT 50"""                                                    
_all_queries['top_50_artists_rating'] = {'q': _ARTISTS_TOP_50_PER_RATING, 'c': _ARTISTS_TOP_50_PER_RATING_COLUMNS}

_ARTISTS_TOP_50_PER_VOCAL_COLUMNS = ["Artist", "Participations"]
_ARTISTS_TOP_50_PER_VOCAL = """SELECT A.name, COUNT(*)
                                FROM artist AS A
                                INNER JOIN credit AS C ON A.idartist = C.idartist
                                WHERE C.role_name LIKE '%Vocals%'
                                GROUP BY A.idartist
                                ORDER BY COUNT(*) DESC
                                LIMIT 50
                                """
_all_queries['top_50_artists_vocal'] = {'q': _ARTISTS_TOP_50_PER_VOCAL, 'c': _ARTISTS_TOP_50_PER_VOCAL_COLUMNS}

_ARTISTS_TOP_50_PER_WRITINGS_COLUMNS = ["Artist", "Participations"]
_ARTISTS_TOP_50_PER_WRITINGS = """SELECT A.name, COUNT(*)
                                    FROM artist AS A
                                    INNER JOIN credit AS C ON A.idartist = C.idartist
                                    WHERE C.role_name LIKE '%Written-By, Arranged By%'
                                        OR C.role_name LIKE '%Lyrics By%'
                                    GROUP BY A.idartist
                                    ORDER BY COUNT(*) DESC
                                    LIMIT 50
                                    """
_all_queries['top_50_artists_writings'] = {'q': _ARTISTS_TOP_50_PER_WRITINGS, 'c': _ARTISTS_TOP_50_PER_WRITINGS_COLUMNS}

_TOP_100_SONGS_COLUMNS = ['Title', 'Appearances']
_TOP_100_SONGS = """SELECT t.title, count(ct.idcollection) as CNT
                    FROM track t
                    INNER JOIN collection_track AS ct ON ct.idtrack = t.idtrack
                    GROUP BY t.idtrack
                    ORDER BY cnt DESC
                    LIMIT 100"""
_all_queries['top_100_songs'] = {'q': _TOP_100_SONGS, 'c': _TOP_100_SONGS_COLUMNS}


