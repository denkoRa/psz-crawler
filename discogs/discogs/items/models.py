import scrapy

class AlbumItem(scrapy.Item):
    album_id = scrapy.Field()
    album_title = scrapy.Field()
    artist_id = scrapy.Field()
    artist_name = scrapy.Field()
    genres = scrapy.Field()
    styles = scrapy.Field()
    year = scrapy.Field()
    tracks = scrapy.Field()
    release_count = scrapy.Field()
    avg_rating = scrapy.Field()
    releases = scrapy.Field()