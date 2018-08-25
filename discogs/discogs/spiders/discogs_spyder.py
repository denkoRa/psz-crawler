import scrapy
import mysql.connector
from discogs.items.models import AlbumItem, ReleaseItem

class DiscogsSpider(scrapy.Spider):
    name = "discogs"    

    def start_requests(self):
        start_urls = ['https://www.discogs.com/search/?type=release&page=200&country_exact={country}',
            'https://www.discogs.com/search/?sort=date_added%2Cdesc&type=release&page=200&country_exact={country}',
            'https://www.discogs.com/search/?sort=date_changed%2Cdesc&type=release&page=200&country_exact={country}',
            'https://www.discogs.com/search/?sort=title%2Casc&type=release&page=200&country_exact={country}',
            'https://www.discogs.com/search/?sort=date_added%2Cdesc&type=release&page=200&country_exact={country}',
            'https://www.discogs.com/search/?sort=have%2Cdesc&type=release&page=200&country_exact={country}',
            'https://www.discogs.com/search/?sort=want%2Cdesc&type=release&page=200&country_exact={country}',
            'https://www.discogs.com/search/?sort=hot%2Cdesc&type=release&page=200&country_exact={country}',
            'https://www.discogs.com/search/?sort=year%2Cdesc&type=release&page=200&country_exact={country}',
            'https://www.discogs.com/search/?sort=year%2Casc&type=release&page=200&country_exact={country}'
        ]
        countries = ['Serbia', 'Yugoslavia']
       
        for url in start_urls:
            for country in countries:
                yield scrapy.Request(url=url.format(country=country), callback=self.parse)
       
    def parse(self, response):
        """
        Parses search results
        Yields request for album pages
        """
        masters = response.css('h4 a.search_result_title')
        for href in masters:
            yield response.follow(href, callback=self.parse_album)

        prev_page = response.css('ul.pagination_page_links li:nth-child(1) a::attr(href)').extract_first()
        if prev_page is not None:
            yield response.follow(prev_page, callback=self.parse)

    def parse_album(self, response):
        """
        Parses one album page
        """
        rel = True if response.url.split('/')[-2] == "release" else False
        ret_item = ReleaseItem() if rel else AlbumItem()
        ret_item['rel'] = rel

        ret_item['id'], ret_item['title'], ret_item['artist_id'], ret_item['artist_name'] = parse_title(response, rel)
        if ret_item['artist_name'] == 'Various':
            return

        ret_item['year'], ret_item['genres'], ret_item['styles'] = parse_headline(response)
        if rel:
            ret_item['country'], ret_item['format'] = parse_country_format(response)

       
        ret_item['tracks'] = parse_tracklist(response)

        if not rel:
            ret_item['releases'], ret_item['release_count'] = parse_releases(response)
        
        ret_item['avg_rating'] = parse_rating(response)
        
        if ret_item['rel']:
            ret_item['credits'] = parse_credits(response)

        yield ret_item

def parse_title(response, rel):
    id = response.url.split('/')[-1]
    title = response.css('h1#profile_title spanitemprop::text')[-1].extract().strip() if rel \
                    else response.css('h1#profile_title > span:nth-child(2)::text').extract_first().strip()
    try:
        artist_id = response.css('h1#profile_title a::attr(href)').extract_first().split('/')[-1].split('-')[0]
        artist_name = response.css('h1#profile_title a::text').extract_first()
    except AttributeError:
        return
    return id, title, artist_id, artist_name
       
def parse_headline(response):
    profile_links = response.css('div.profile div.content a')
    year = None
    genres = []
    styles = []
    for a in profile_links:
        link = a.css('::attr(href)').extract_first()
        if "year=" in link:
            try:
                year = link.split('year=')[1]
            except AttributeError:
                pass
        elif "genre" in link:
            genres.append(a.css('::text').extract_first())
        elif "style" in link:
            styles.append(a.css('::text').extract_first())
    return year, genres, styles

def parse_country_format(response):
    profile_links = response.css('div.profile div.content a')
    country, format = None, None
    for a in profile_links:
        link = a.css('::attr(href)').extract_first()
        if "format" in link:
            format = a.css('::text').extract_first()
        elif "country=" in link:
            try:
                country = link.split('country=')[1]
            except AttributeError:
                pass
    return country, format

def parse_tracklist(response):
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
        except (AttributeError, ValueError):
            pass
    return extracted_tracks

def parse_releases(response):
    releases = response.css('table#versions tr')[1:]
    release_count = len(releases)
    rel_list = []
    for rel in releases:
        rel_id = rel.css('td.title > a::attr(href)').extract_first().split('/')[-1]
        rel_list.append(rel_id)
    return rel_list, release_count

def parse_rating(response):
    try:
        return float(response.css('span.rating_value::text').extract_first())
    except (ValueError, TypeError):
        return None

def parse_credits(response):
    credits_sel = response.css('.credits > div.section_content > ul > li')
    extracted_credits = {}
    for cred in credits_sel:
        role = cred.css('span.role::text').extract_first()
        artists = []
        try:
            for a in cred.css('a'):
                id = a.css('::attr(href)').extract_first().split('/')[-1].split('-')[0]
                name = a.css('::text').extract_first()
                artists.append({"id": id, "name": name})
        except AttributeError:
            pass
        if artists:
            extracted_credits[role] = artists
    return extracted_credits