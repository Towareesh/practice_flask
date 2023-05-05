from ftsmachine.extensions import get_logger
from flask import Flask
import pandas as pd
import sqlite3


logger = get_logger('FTSMachine')

class Engine:
    def __init__(self, app: Flask | None = None) -> None:
        self.db_uri = None
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app: Flask | None = None) -> None:
        app.extensions["ftsmachine"] = self
        self.db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')[10:]
        # self.db_uri = app.config.get('SQLALCHEMY_DATABASE_URI').replace(r'\w+\:[/]{3}', '')
    
    def sqlite_query(self, sqlite_query: str) -> iter:
        """Connect to SQLite database
        Args:
            sqlite_query (str): query on SQL
        Returns:
            Generator: record in db
        """        
        try:
            sqlite_connection = sqlite3.connect(self.db_uri)
            cursor = sqlite_connection.cursor()
            cursor.execute(sqlite_query)
            records = cursor.fetchall()
            cursor.close()
            logger.info('Connection to database is opened')
            for record in records:
                yield record

        except sqlite3.Error as error:
            logger.error(f'{error}: Failed connect to database')
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                logger.warning('Connection to database is closed')

    def get_data_frame(self, *columns_name, db_query) -> pd.DataFrame:
        data_frame = pd.DataFrame(data=[[columns for columns in record] for record in db_query],
                                  columns=[columns for columns in columns_name])
        return data_frame
            

class FTSMachine(Engine):
    def __init__(self, app: Flask | None = None) -> None:
        super().__init__(app)
        self.db     = None
        self.cursor = None

    def create_db_cursor(self) -> None:
        try:
            self.db     = sqlite3.connect(':memory:')
            self.cursor = self.db.cursor()
            logger.info('Сursor created successfully')
        except sqlite3.Error as error:
            logger.error(f'{error}: Failed to create cursor')
        
    
    def create_virtual_table(self, data_frame: pd.DataFrame, headers: list) -> None:
        columns     = ', '.join([i for i in headers])
        none_values = ', '.join(['?' for _ in range(len(headers))])

        self.create_db_cursor()
        self.cursor.execute(f"""CREATE VIRTUAL TABLE virtual_table
                                USING FTS5({columns}, tokenize="porter unicode61")""")
        
        self.cursor.executemany(f"""INSERT INTO virtual_table({columns})
                                    VALUES({none_values})""",
                                    data_frame.to_records(index=False))
        self.db.commit()

    def search_fetchall_query(self, value, column,
                              search_type='MATCH',
                              limit_answers='5') -> list:
        try:
            result = self.cursor.execute(f"""SELECT *, RANK
                                            FROM virtual_table
                                            WHERE {column} {search_type} "{value}"
                                            ORDER BY RANK
                                            LIMIT {limit_answers}
                                            """).fetchall()
            self.cursor.close()
            logger.warning('Cursor is closed')
        except sqlite3.Error as error:
            logger.error(f'{error}: Failed to create cursor')
        return result