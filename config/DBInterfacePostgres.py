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
        df.to_sql(table_name, con = self.engine, if_exists = exist_option, index = False)
        
    def get_from_database(self, table_id: str, columns_list: list[str], filter_condition: str = None):
        query_str = (lambda x: x if (filter_condition == None) else f"{x} WHERE {filter_condition}")(f"SELECT {','.join(columns_list)} FROM {table_id}")
        self.df   = pd.DataFrame(self.engine.connect().execute(text(query_str)).fetchall())    

        return self.df
        
    def db_interaction(self, query_str: str):
        return_object = self.engine.connect().execute(text(query_str))

        return return_object
