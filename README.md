# psz-crawler

The project was school homework project assignment.  
The task is to scrap all the information about music albums released in countries Yugoslavia and Serbia from https://www.discogs.com/ and do some data analysis with it.

### Installation
```pip install requirements.txt```

## Scraping

First part is to scrap all the data.
I have used [scrapy](https://scrapy.org/) framework for that matter.

### Task1 
Spider can be started with
```
cd discogs
scrapy crawl discogs
```
Be aware that this process can last for many hours.
All the downloaded data is stored in MySQL relation database (there are approx. 50k releases and 6k master albums and many more tracks).

## Data analysis

### Task 2

Task 2 performs couple of SQL queries on the data like which albums had most releases, top 50 persons per rating average in credits, top 50 persons with most appearances as vocal in credits etc.

```
python analysis/task2/task2.py
```

### Task 3

Task 3 performs SQL queries and visualize the data using [plotly](https://plot.ly/).
All produced results can be found in `~/charts`.
```
python analysis/task3/task3.py
```

### Task 4

Task 4 performs K-Means algorithm (from [scikit-learn](http://scikit-learn.org/stable/index.html)) on the data based on features like genre, style, format, year of release, number of tracks and rating.
It applies PCA algorithm and plots K clusters in 2D.
```
python analysis/task4/kmeans.py
```
