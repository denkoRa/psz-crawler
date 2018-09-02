import argparse
import mysql.connector
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer, StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from queries4 import _GET_ALBUMS, _GET_ALBUMS_GENRES, _GET_ALBUMS_STYLES, _GET_ALL_GENRES, _GET_ALL_STYLES
import numpy as np
from plotly.offline import plot
import plotly.graph_objs as go
from random import sample

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
        albums[res[0]] = {'title': res[1], 'artist': res[2], 'year': res[3], 'rating': res[4], 'word_features': []}
    return albums


def add_genre_word_features(albums, g):
    if not g: 
        return
    album_genres = select(_GET_ALBUMS_GENRES)
    for ag in album_genres:
        if ag[0] in albums:
            albums[ag[0]]['word_features'].append(ag[1])


def add_style_word_features(albums, s):
    if not s:
        return
    album_styles = select(_GET_ALBUMS_STYLES)
    for ast in album_styles:
        if ast[0] in albums:
            albums[ast[0]]['word_features'].append(ast[1])


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
        add_genre_word_features(albums, args.genre)
        add_style_word_features(albums, args.style)
        for key in albums:
            albums[key]['word_features'] = " ".join(albums[key]['word_features'])

        albums = list(albums.values())
        vocab = get_vocabulary(args.genre, args.style)
        count_vectorizer = CountVectorizer()
        count_vectorizer.fit(vocab)
        samples = [album['word_features'] for album in albums]
        extracted_word_data = count_vectorizer.fit_transform(samples)
        extracted_word_data = Normalizer().fit_transform(extracted_word_data).A
        extra_f = extracted_word_data.shape[1]
    else:
        albums = list(albums.values())
        extracted_word_data = None
        extra_f = 0
    
    data = np.zeros((len(albums), args.year + args.rating + extra_f))

    if extracted_word_data is not None:
        data[:, :extracted_word_data.shape[1]] = extracted_word_data
        j = extracted_word_data.shape[1]

    if args.year:
        add_single_feature_vector(data, j, 'year', albums)
        j = j + 1

    if args.rating:
        add_single_feature_vector(data, j, 'rating', albums)

    kmeans = KMeans(n_clusters=args.k, n_init=5, verbose=1, tol=1e-5).fit(data)

    labels = kmeans.labels_

    colors = [list(np.random.choice(range(30, 220), size=3)) for k in range(args.k)]
    indices = sample(range(len(albums)), 500)

    #2D projektovanje
    pca2d = PCA(n_components=2)
    data_points = pca2d.fit_transform(data)
    
    plot_data = []
    clustered_data = [[] for k in range(args.k)]
    for i in indices:
        clustered_data[labels[i]].append({'points': data_points[i], 'idx': i})

    for k in range(args.k):
        plot_data.append(
            go.Scatter(
                mode="markers",
                name="cluster{}".format(k+1),
                marker=dict(
                    color="rgb({},{},{})".format(colors[k][0], colors[k][1], colors[k][2]),
                ),
                x=[d['points'][0] for d in clustered_data[k]],
                y=[d['points'][1] for d in clustered_data[k]],
                text=["{}-{}\nreleased={} rating={}\nword_features={}".  
                    format(albums[d['idx']]['title'], albums[d['idx']]['artist'], albums[d['idx']]['year'], albums[d['idx']]['rating'], albums[d['idx']]['word_features']) for d in clustered_data[k]]
            )
        )
    layout = go.Layout(
        title="K means 2d projection for {} clusters".format(args.k)
    )
    plot(go.Figure(data=plot_data, layout=layout), filename="charts/clusters2d.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("k", help="number of clusters", type=int)
    parser.add_argument("-g", "--genre", help="use genre", action="store_true")
    parser.add_argument("-s", "--style", help="use style", action="store_true")
    parser.add_argument("-r", "--rating", help="use rating", action="store_true")
    parser.add_argument("-y", "--year", help="use year", action="store_true")
    args = parser.parse_args()
    main(args)
