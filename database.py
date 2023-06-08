import sqlite3
import logging
from logger import logger

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            SELECT name FROM sqlite_master WHERE type='table' AND name='torrents'
        ''')
        table_exists = self.cursor.fetchone()

        if not table_exists:
            self.cursor.execute('''
                CREATE TABLE torrents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    url TEXT,
                    size TEXT,
                    seeds TEXT,
                    leeches TEXT,
                    date TEXT
                )
            ''')
            logger.info('Table "torrents" created in the database.')
        else:
            logger.info('Table "torrents" already exists in the database.')

    def insert_torrent(self, torrent):
        # Check if the torrent name already exists in the database
        self.cursor.execute(
            'SELECT id FROM torrents WHERE name = ?', (torrent.tName,))
        existing_record = self.cursor.fetchone()

        if existing_record:
            # Update the existing record
            self.cursor.execute('''
                UPDATE torrents
                SET url = ?, size = ?, seeds = ?, leeches = ?, date = ?
                WHERE id = ?
            ''', (torrent.tLink, torrent.tSize, torrent.tSeeds, torrent.tLeeches, torrent.tDate, existing_record[0]))
            logger.info(f'Torrent "{torrent.tName}" updated in the database.')
        else:
            # Insert a new record
            self.cursor.execute('''
                INSERT INTO torrents (name, url, size, seeds, leeches, date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (torrent.tName, torrent.tLink, torrent.tSize, torrent.tSeeds, torrent.tLeeches, torrent.tDate))
            logger.info(
                f'Torrent "{torrent.tName}" inserted into the database.')

    def commit_changes(self):
        self.conn.commit()
        logger.info('Changes committed to the database.')

    def close_connection(self):
        self.conn.close()
        logger.info('Database connection closed.')
