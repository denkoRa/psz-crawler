import mysql.connector
from prettytable import PrettyTable
import queries2

_db = mysql.connector.connect(
    host="localhost",
    user="psz",
    password="123",
    database='discogs',
    auth_plugin='mysql_native_password'
)

def select(query):
    cursor = _db.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def print_query_results(query, *args):
    x = PrettyTable()
    x.field_names = queries2._all_queries[query]['c']
    q = queries2._all_queries[query]['q'].format(args[0] if args else None)
    for res in select(q):
        x.add_row(res)
    print(x)

def main():
    input("\nKoliko zapisa pripada svakom od zanrova?")
    print_query_results('genres_count')

    input("\nKoliko zapisa pripada svakom od stilova?")
    print_query_results('styles_count')

    input("\nRang lista prvih 10 albuma (ili vise ako ima neresenih) po broju izdatih verzija")
    print("\nDohvati 10. album po broju izdanja")
    _10th_release_count = select(queries2._10th_RELEASE_COUNT)[0][0]
    print(_10th_release_count)
    print_query_results('top_10_albums', _10th_release_count)

    input("\nPrvih 50 osoba koje imaju najveci generalni rejting (Credits)")
    print_query_results('top_50_artists_rating')
   
    input("\nPrvih 50 osoba koje imaju najvise ucesca kao vokal")
    print_query_results('top_50_artists_vocal')

    input("\nPrvih 50 osoba sa najvise napisanih pesama (Writing & Arrangement)")
    print_query_results('top_50_artists_writings')

    input("\n100 pesama koje se nalaze na najvise albuma")
    print_query_results('top_100_songs')

if __name__ == "__main__":
    main()