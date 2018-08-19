import scrapy
import mysql.connector
from discogs.items.models import AlbumItem

class DiscogsSpyder(scrapy.Spider):
    name = "discogs"
    start_urls = [
        "https://www.discogs.com/search/?type=master&country_exact=Yugoslavia",
    ]

    def parse(self, response):
        """
        Exploring master search
        """
        masters = response.css('h4 a.search_result_title')
        for href in masters:
            yield response.follow(href, callback=self.parse_album)

        next_page = response.css('ul.pagination_page_links li:nth-child(2) a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_album(self, response):
        """
        Parses master page
        TODO In each callback ensure that proxy /really/ returned your target page by checking 
        for site logo or some other significant element. If not - retry request with dont_filter=True
        """       
        ret_item = AlbumItem()
        
        ret_item['album_id'] = response.url.split('/')[-1]
        ret_item['album_title'] = response.css('h1#profile_title > span:nth-child(2)::text').extract_first().strip()
        
        ret_item['artist_id'] = response.css('h1#profile_title > span > span > a::attr(href)').extract_first().split('/')[-1].split('-')[0]
        ret_item['artist_name'] = response.css('h1#profile_title > span > span > a::text').extract_first()
        if ret_item['artist_name'] == 'Various':
            return

        profile_divs = response.css('div.profile > div.content')

        genres_sel = profile_divs[0].css('a')
        genres = []
        for g in genres_sel:
            genres.append(g.css('::text').extract_first())
        ret_item['genres'] = genres

        styles_sel = profile_divs[1].css('a')
        styles = []
        for s in styles_sel:
            styles.append(s.css('::text').extract_first())
        ret_item['styles'] = styles

        year_sel = profile_divs[2] 
        year = None
        try:
            year = year_sel.css('a::attr(href)').extract_first().split('year=')[1]
        except AttributeError:
            pass
        ret_item['year'] = year

        tracklist = response.css('table.playlist')
        tracks = tracklist.css('tr')
        extracted_tracks = []
        for track in tracks:
            try:
                track_id = track.css('td.tracklist_track_title a::attr(href)').extract_first().split('/')[-1]
                track_title = track.css('td.tracklist_track_title span::text').extract_first()
                track_duration =  track.css('td.tracklist_track_duration span::text').extract_first()
                track_duration_sec = None
                if track_duration is not None:
                    track_duration_sec = int(track_duration.split(':')[0]) * 60 + int(track_duration.split(':')[1])
                extracted_tracks.append({"id": track_id, "title": track_title, "duration": track_duration_sec})
            except AttributeError:
                pass
            except ValueError:
                pass

        ret_item['tracks'] = extracted_tracks

        releases = response.css('table#versions tr')[1:]
        release_count = len(releases)
        ret_item['release_count'] = release_count
        rel_list = []
        for rel in releases:
            rel_id = rel.css('td.title > a::attr(href)').extract_first().split('/')[-1]
            rel_list.append(rel_id)
        ret_item['releases'] = rel_list

        avg_rating = None
        try:
            avg_rating = float(response.css('span.rating_value::text').extract_first())
        except ValueError:
            pass
        ret_item['avg_rating'] = avg_rating

        yield ret_item
            
        
    