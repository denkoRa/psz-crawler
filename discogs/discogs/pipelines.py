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
        """
        Saves all the information from one album release to DB
        """
        rel = item['rel']
        if rel:
            val = (item['id'], item['title'], item['year'], item['avg_rating'], item['artist_id'], item['country'], len(item['tracks']), item['format'])
            self.cursor.execute(insert_release, val)
        else:
            val = (item['id'], item['title'], item['release_count'], item['artist_id'], item['year'], len(item['tracks']), item['avg_rating'])
            self.cursor.execute(insert_album, val)
        
        if item['artist_id'] not in self.artist_ids:
            val = (item['artist_id'], item['artist_name'])
            try:
                self.cursor.execute(insert_artist, val)
                self.artist_ids.append(item['artist_id'])
            except mysql.connector.errors.IntegrityError:
                pass

        collection_id = item['id']
        for track in item['tracks']:
            val = (track['id'], track['title'], track['duration'])
            try:
                self.cursor.execute(insert_track, val)
            except mysql.connector.errors.IntegrityError:
                pass
            try:
                val = (collection_id, track['id'])
                self.cursor.execute(insert_collection_track, val)
            except mysql.connector.errors.IntegrityError:
                pass
        
        for genre in item['genres']:
            val = (collection_id, genre)
            try:
                self.cursor.execute(insert_collection_genre, val)
            except mysql.connector.errors.IntegrityError:
                pass
            if genre not in self.genres:
                val = {"name": genre}
                self.cursor.execute(insert_genre, val)
                self.genres.append(genre)
        
        for style in item['styles']:
            val = (collection_id, style)
            try:
                self.cursor.execute(insert_collection_style, val)
            except mysql.connector.errors.IntegrityError:
                pass
            if style not in self.styles:
                val = {"name": style}
                self.cursor.execute(insert_style, val)
                self.styles.append(style)
        
        if not rel:
            for r in item['releases']:
                val = (collection_id, r)
                self.cursor.execute(insert_album_release, val)
        if rel:
            credits = item['credits']
            for role in credits:
                try:
                    val = {"name": role}
                    self.cursor.execute(insert_role, val)
                except mysql.connector.errors.IntegrityError:
                    pass
                people = credits[role]
                for person in people:
                    id = person['id']
                    try:
                        if id not in self.artist_ids:
                            val = (id, person['name'])
                            self.cursor.execute(insert_artist, val)
                            self.artist_ids.append(id)
                        val = (id, role, collection_id)
                        self.cursor.execute(insert_credit, val)
                    except mysql.connector.errors.IntegrityError:
                        pass
    
        self.mydb.commit()
        return item
