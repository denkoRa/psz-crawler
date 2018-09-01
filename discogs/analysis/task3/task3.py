import mysql.connector
import plotly.graph_objs as go
from plotly.offline import plot
from queries3 import _ALBUMS_PER_DECADES, _TOP_6_GENRES, _TRACKS_PER_DURATION, _FIND_CYRILLIC_ALBUMS, _TOTAL_ALBUMS, _ALBUMS_PER_GENRE_CNT

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


def main():
    results = select(_ALBUMS_PER_DECADES)
    labels = [res[0] for res in results]
    values = [res[1] for res in results]
    data = [go.Pie(
        labels=labels, 
        values=values, 
        hole=.3
    )]
    layout = go.Layout(
        title='Albums per decade',
        font=dict(family='Ubuntu', size=20)
    )
    plot(go.Figure(
        data=data, 
        layout=layout), 
        filename='a.html'
    )

    results = select(_TOP_6_GENRES)
    labels = [res[0] for res in results]
    values = [res[1] for res in results]
    layout = go.Layout(
        title='Top 6 genres',
        font=dict(family='Ubuntu', size=20)
    )
    data = [go.Pie(
        labels=labels, 
        values=values, 
        hole=.3
    )]
    plot(go.Figure(
        data=data, 
        layout=layout), 
        filename='b.html'
    )

    _90 = select(_TRACKS_PER_DURATION.format(0, 90))
    _91_180 = select(_TRACKS_PER_DURATION.format(91, 180))
    _181_240 = select(_TRACKS_PER_DURATION.format(181, 240))
    _241_300 = select(_TRACKS_PER_DURATION.format(241, 300))
    _301_360 = select(_TRACKS_PER_DURATION.format(301, 360))
    _361_ = select(_TRACKS_PER_DURATION.format(361, 100000))
    labels = ["90s or less", "91-180", "181-240", "241-300", "301-360", "361 or more"]
    values = [_90[0][0], _91_180[0][0], _181_240[0][0], _241_300[0][0], _301_360[0][0], _361_[0][0]]
    layout = go.Layout(
        title="Songs per duration", 
        font=dict(family='Ubuntu', size=20)
    )
    data = [go.Pie(
        labels=labels, 
        values=values, 
        hole=.3
    )]
    plot(go.Figure(
        data=data,
        layout=layout), 
        filename='c.html'
    )

    cyrillic = select(_FIND_CYRILLIC_ALBUMS)
    cyrillic_cnt = cyrillic[0][0]
    total = select(_TOTAL_ALBUMS)
    total_cnt = total[0][0]
    labels = ['Cyrillic', 'Latin']
    values = [cyrillic_cnt, total_cnt - cyrillic_cnt]
    layout = go.Layout(
        title="Cyrillic vs Latin alphabet", 
        font=dict(family='Ubuntu', size=20)
    )
    data = [go.Pie(
        labels=labels, 
        values=values, 
        hole=.3
    )]
    plot(go.Figure(
        data=data,
        layout=layout),
        filename='d.html'
    )

    results = select(_ALBUMS_PER_GENRE_CNT)
    labels = ["1 genre", "2 genres", "3 genres", "4 or more genres"]
    values = [res[1] for res in results]
    layout = go.Layout(
        title="Albums per number of genres", 
        font=dict(family='Ubuntu', size=20)
    )
    data = [go.Pie(
        labels=labels, 
        values=values, 
        hole=.3
    )]
    plot(go.Figure(
        data=data,
        layout=layout),
        filename='e.html'
    )

if __name__ == "__main__":
    main()