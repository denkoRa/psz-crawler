# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector

from .queries import *


class DiscogsPipeline(object):
    
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         database=crawler.settings.get('DATABASE')
    #     )

    def open_spider(self, spider):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="psz",
            password="123",
            database='discogs',
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.mydb.cursor()

        self.artist_ids = []
        self.cursor.execute("SELECT idartist FROM artist")
        rows = self.cursor.fetchall()
        for r in rows:
            self.artist_ids.append(r[0])

        self.genres = []
        self.cursor.execute("SELECT * FROM genre")
        rows = self.cursor.fetchall()
        for r in rows:
            self.genres.append(r[0])
        
        self.styles = []
        self.cursor.execute("SELECT * FROM style")
        rows = self.cursor.fetchall()
        for r in rows:
            self.styles.append(r[0])
        
        

    def process_item(self, item, spider):
        val = (item['album_id'], item['album_title'], item['release_count'], item['artist_id'], item['year'], len(item['tracks']), item['avg_rating'])
        self.cursor.execute(insert_album, val)
        
        if item['artist_id'] not in self.artist_ids:
            val = (item['artist_id'], item['artist_name'])
            try:
                self.cursor.execute(insert_artist, val)
                self.artist_ids.append(item['artist_id'])
            except mysql.connector.errors.IntegrityError:
                pass
                
        album_id = item['album_id']
        for track in item['tracks']:
            val = (track['id'], track['title'], track['duration'])
            self.cursor.execute(insert_track, val)

            val = (album_id, track['id'])
            self.cursor.execute(insert_collection_track, val)

        for genre in item['genres']:
            val = (album_id, genre)
            self.cursor.execute(insert_collection_genre, val)

            if genre not in self.genres:
                val = {"name": genre}
                self.cursor.execute(insert_genre, val)
                self.genres.append(genre)

        for style in item['styles']:
            val = (album_id, style)
            self.cursor.execute(insert_collection_style, val)

            if style not in self.styles:
                val = {"name": style}
                self.cursor.execute(insert_style, val)
                self.styles.append(style)
        
        for r in item['releases']:
            val = (album_id, r)
            self.cursor.execute(insert_album_release, val)

        self.mydb.commit()
        return item
