import scrapy

class CommonItem(scrapy.Item):
    """
    Common fields between Master and Release
    """
    id = scrapy.Field()
    title = scrapy.Field()
    genres = scrapy.Field()
    styles = scrapy.Field()
    year = scrapy.Field()
    artist_id = scrapy.Field()
    artist_name = scrapy.Field()
    avg_rating = scrapy.Field()
    rel = scrapy.Field()
    tracks = scrapy.Field()
    
class AlbumItem(CommonItem):
    """
    Specific fields for master 
    """
    release_count = scrapy.Field()
    releases = scrapy.Field()

class ReleaseItem(CommonItem):
    """
    Specific fields for release
    credits: 
    {
        role: [artists]
    }
    """
    country = scrapy.Field()
    format = scrapy.Field()
    credits = scrapy.Field()
