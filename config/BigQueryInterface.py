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
        def form_column_string(columns_list: list[str]) -> str:
            output_str = ",".join(columns_list)

            return output_str
        
        query_string   = f"""
            SELECT 
                {form_column_string(columns_list)}
            FROM
                '{self.project_id}.{dataset_id}.{table_name}'
        """

        query_result = self.gcp_client.query(query_string)
        result_data  = pd.DataFrame([list(i) for i in query_result], columns = columns_list)

        return result_data
    
    def upload_data(self, upload_data: pd.DataFrame, project_id: str, table_id: str):
        pandas_gbq.to_gbq(upload_data, table_id, project_id = project_id)