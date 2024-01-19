import pandas as pd

from config.SeleniumSettings         import SeleniumSettings 
from config.BigQueryInterface        import BigQueryInterface
from src.process_data.FormOutputData import FormOutputData

class UploadToGoogleWithNotifications:
    def upload_to_google_settings(self, target_dataset: str, project_id_string: str, gcp_json_file: str, gcp_table_names_list: list[str], rename_dict: dict, form_outputs_config_dict: dict) -> None:
        self.target_dataset           = target_dataset
        self.project_id_string        = project_id_string
        self.gcp_json_file            = gcp_json_file
        self.gcp_table_names_list     = gcp_table_names_list
        self.rename_dict              = rename_dict
        self.form_outputs_config_dict = form_outputs_config_dict
        self.gcp_interface_object     = BigQueryInterface()
        self.gcp_interface_object.gcp_settings_method(self.project_id_string, self.gcp_json_file)

    def form_outputs_data(self) -> list[pd.DataFrame]:
        output_data_object = FormOutputData(SeleniumSettings(**self.form_outputs_config_dict["FormOutputData"]["constructor"]))
        output_data_object.form_output_settings_method(**self.form_outputs_config_dict["FormOutputData"]["form_output_settings_method"])
        results_data_list = output_data_object.save_output_data()

        return results_data_list
    
    def upload_to_gcp(self) -> None:
        results_data_list = self.form_outputs_data()

        for (table_id, dataframe) in zip(self.gcp_table_names_list, results_data_list):
            dataframe = dataframe.rename(columns = self.rename_dict[table_id])
            self.gcp_interface_object.upload_data(dataframe, self.project_id_string, f"{self.target_dataset}.{table_id}")
