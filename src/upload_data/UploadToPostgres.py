import pandas as pd 

from config.SeleniumSettings         import SeleniumSettings 
from config.DBInterfacePostgres      import DBInterface
from src.process_data.FormOutputData import FormOutputData

class UploadToPostgres:
    def upload_to_postgres_settings(self, db_interface_config: dict, table_names_list: list[str], form_outputs_config_dict: dict, rename_dict: dict):
        self.db_interface_config      = db_interface_config 
        self.table_names_list         = table_names_list 
        self.form_outputs_config_dict = form_outputs_config_dict
        self.rename_dict              = rename_dict 
        self.db_connector_object      = DBInterface()
        self.db_connector_object.connection_settings(**self.db_interface_config["DBInterface"]["connection_settings"])
    
    def main_logic(self):
        output_data_object = FormOutputData(SeleniumSettings(**self.form_outputs_config_dict["FormOutputsData"]["constructor"]))
        output_data_object.form_output_settings_method(**self.form_outputs_config_dict["FormOutputsData"]["form_output_settings_method"])
        results_data_list = output_data_object.save_output_data()

        for (table_id, dataframe) in zip(self.table_names_list, results_data_list):
            dataframe = dataframe.rename(columns = self.rename_dict[table_id])            
            self.db_connector_object.upload_to_database(table_id, dataframe)
