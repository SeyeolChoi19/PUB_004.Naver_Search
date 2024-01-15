import psycopg2

import pandas as pd 
import numpy  as np 

from sqlalchemy import create_engine
from sqlalchemy import text

class DBInterface:
    def connection_settings(self, sql_type: str, username: str, password: str, hostname: str, server_name: str):
        self.sql_type    = sql_type
        self.username    = username
        self.password    = password 
        self.hostname    = hostname 
        self.server_name = server_name
        self.engine      = create_engine(f"{sql_type}://{username}:{password}@{hostname}/{server_name}", echo = False)
    
    def upload_to_database(self, table_name: str, df: pd.core.frame.DataFrame, exist_option: str = "append"):
        df.to_sql(table_name, con = self.engine, if_exists = exist_option)
        
    def get_from_database(self, query_str: str):
        self.df = pd.DataFrame(self.engine.connect().execute(text(query_str)).fetchall())    
        
    def db_interaction(self, query_str: str):
        self.engine.execute(query_str)
