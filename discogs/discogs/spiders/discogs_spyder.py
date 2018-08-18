import scrapy


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


    def parse_album(self, response):
        """
        Parses master page
        TODO In each callback ensure that proxy /really/ returned your target page by checking 
        for site logo or some other significant element. If not - retry request with dont_filter=True
        """           
        album_id = response.url.split('/')[-1]
        album_title = response.css('h1#profile_title > span:nth-child(2)::text').extract_first().strip()
        
        artist_id = response.css('h1#profile_title > span > span > a::attr(href)').extract_first().split('/')[-1].split('-')[0]
        artist_name = response.css('h1#profile_title > span > span > a::text').extract_first()
        
        profile_divs = response.css('div.profile > div.content')

        genres_sel = profile_divs[0].css('a')
        genres = []
        for g in genres_sel:
            genres.append(g.css('::text').extract_first())

        styles_sel = profile_divs[1].css('a')
        styles = []
        for s in styles_sel:
            styles.append(s.css('::text').extract_first())

        year_sel = profile_divs[2]
        year = year_sel.css('a::attr(href)').extract_first().split('year=')[1]

        tracklist = response.css('table.playlist')
        tracks = tracklist.css('tr')
        for track in tracks:
            track_id = track.css('a::attr(href)').extract_first().split('/')[-1]
            track_title = track.css('td:nth-child(1) span::text').extract_first()
            track_duration =  track.css('td:nth-child(2) span::text').extract_first()
            track_duration_sec = int(track_duration.split(':')[0]) * 60 + int(track_duration.split(':')[1])
            #insert into tables

        releases = response.css('table#versions tr')[1:]
        release_count = len(releases)

        avg_rating = 0
        try:
            avg_rating = float(response.css('span.rating_value::text').extract_first())
        except ValueError:
            pass
        
        #for release in releases:
            
        
    