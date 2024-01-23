import json, pandas_gbq 

import pandas as pd 

from google.cloud  import bigquery 
from google.oauth2 import service_account 

class BigQueryInterface:
    def gcp_settings_method(self, project_id: str, gcp_json_file: str) -> None:
        self.project_id    = project_id 
        self.gcp_json_file = gcp_json_file 

        self.gcp_client = bigquery.Client(
            credentials = service_account.Credentials.from_service_account_file(self.gcp_json_file)
        )

    def get_data_from_gcp(self, table_name: str, columns_list: list[str], dataset_id: str) -> list[pd.DataFrame]:        
        query_string   = f"""
            SELECT 
                {','.join(columns_list)}
            FROM
                '{self.project_id}.{dataset_id}.{table_name}'
        """

        query_result = self.gcp_client.query(query_string)
        result_data  = pd.DataFrame([list(i) for i in query_result], columns = columns_list)

        return result_data
    
    def upload_data(self, upload_data: pd.DataFrame, project_id: str, table_id: str):
        pandas_gbq.to_gbq(upload_data, table_id, project_id = project_id, if_exists = "append")

if (__name__ == "__main__"):
    for (sheet_name, table_name) in zip(["수집 상태", "자동완성키워드", "인기주제", "연관검색어"], ["CHSCRAPE_STATUS", "CHSCRAPE_001", "CHSCRAPE_002", "CHSCRAPE_003"]):
        df  = pd.read_excel(r"C:\Users\User\NaverKeywords\data\2024-01-23 네이버 검색어 키워드 데이터 - 복사본.xlsx", sheet_name = sheet_name)
        bqi = BigQueryInterface()
        bqi.gcp_settings_method("sincere-night-367502", "C:/Users/User/Downloads/sincere-night-367502-d1ed9f50d1d7.json")
        bqi.upload_data(df, "sincere-night-367502", f"test.{table_name}")
