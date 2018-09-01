import argparse
import mysql.connector
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer, StandardScaler
from sklearn.cluster import KMeans
from queries4 import _GET_ALBUMS, _GET_ALBUMS_GENRES, _GET_ALBUMS_STYLES, _GET_ALL_GENRES, _GET_ALL_STYLES
import numpy as np


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


def get_albums_dict():
    results = select(_GET_ALBUMS)
    albums = {}
    for res in results:
        albums[res[0]] = {'title': res[1], 'artist': res[2], 'year': res[3], 'rating': res[4], 'keywords': []}
    return albums


def add_genre_keywords(albums, g):
    if not g: 
        return
    album_genres = select(_GET_ALBUMS_GENRES)
    for ag in album_genres:
        if ag[0] in albums:
            albums[ag[0]]['keywords'].append(ag[1])


def add_style_keywords(albums, s):
    if not s:
        return
    album_styles = select(_GET_ALBUMS_STYLES)
    for ast in album_styles:
        if ast[0] in albums:
            albums[ast[0]]['keywords'].append(ast[1])


def get_vocabulary(g, s):
    v = []
    if g:
        results = select(_GET_ALL_GENRES)
        for res in results:
            v.append(res[0])
    if s:
        results = select(_GET_ALL_STYLES)
        for res in results:
            v.append(res[0])
    return v


def add_single_feature_vector(data, col, feature, albums):
    f_list = np.transpose(np.array([[a[feature] for a in albums]], dtype=np.float))
    null_year_indexes = np.where(np.isnan(f_list))
    f_list[null_year_indexes] = np.nanmean(f_list)
    vector = StandardScaler().fit_transform(f_list)
    data[:, col] = vector[:, 0]


def main(args):
    albums = get_albums_dict()
    j = 0
     
    if args.genre or args.style:
        add_genre_keywords(albums, args.genre)
        add_style_keywords(albums, args.style)
        for key in albums:
            albums[key]['keywords'] = " ".join(albums[key]['keywords'])

        albums = list(albums.values())
        #print(albums)
        vocab = get_vocabulary(args.genre, args.style)
        count_vectorizer = CountVectorizer()
        count_vectorizer.fit(vocab)
        samples = [album['keywords'] for album in albums]
        print(samples)
        extracted_word_data = count_vectorizer.fit_transform(samples)
        extracted_word_data = Normalizer().fit_transform(extracted_word_data).A
        print(extracted_word_data.shape)
    else:
        albums = list(albums.values())
    
    data = np.zeros((len(albums), args.year + args.rating + extracted_word_data.shape[1]))

    if extracted_word_data is not None:
        data[:, :extracted_word_data.shape[1]] = extracted_word_data
        j = extracted_word_data.shape[1]

    if args.year:
        add_single_feature_vector(data, j, 'year', albums)
        j = j + 1

    if args.rating:
        add_single_feature_vector(data, j, 'rating', albums)

    print(data)
    print(data.shape)

    kmeans = KMeans(n_clusters=args.k, n_init=5, verbose=2, tol=1e-5).fit(data)
    print(len(kmeans.labels_))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("k", help="number of clusters", type=int)
    parser.add_argument("-g", "--genre", help="use genre", action="store_true")
    parser.add_argument("-s", "--style", help="use style", action="store_true")
    parser.add_argument("-r", "--rating", help="use rating", action="store_true")
    parser.add_argument("-y", "--year", help="use year", action="store_true")
    args = parser.parse_args()
    main(args)
