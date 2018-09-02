_GET_ALBUMS = """SELECT idrelease, title, a.name, released, avg_rating, track_count
                FROM discogs.release AS r
                LEFT JOIN artist AS a ON a.idartist = r.idartist
                """

_GET_ALBUMS_GENRES = """SELECT idcollection, cg.name
                    FROM collection_genre AS cg
                    INNER JOIN genre AS g ON g.name = cg.name
                    """

_GET_ALBUMS_STYLES = """SELECT idcollection, name
                    FROM collection_style AS cs
                    INNER JOIN style AS s on s.name = cs.name
                    """

_GET_ALBUMS_FORMAT = """SELECT idrelease, format
                    FROM discogs.release
                    """                    

_GET_ALL_GENRES = """SELECT name 
                    FROM genre
                    """

_GET_ALL_STYLES = """SELECT name 
                    FROM style
                    """

_GET_ALL_FORMATS = """SELECT distinct(format)
                    FROM discogs.release
                    """