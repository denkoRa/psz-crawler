_GET_ALBUMS = """SELECT idrelease, title, a.name, released, avg_rating
                FROM discogs.release AS r
                LEFT JOIN artist AS a ON a.idartist = r.idartist
                """

_GET_ALBUMS_GENRES = """SELECT idcollection, name
                    FROM collection_genre
                    """

_GET_ALBUMS_STYLES = """SELECT idcollection, name
                    FROM collection_style
                    """

_GET_ALL_GENRES = """SELECT name FROM genre"""

_GET_ALL_STYLES = """SELECT name FROM style"""