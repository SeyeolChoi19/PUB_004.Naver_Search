import json

import pandas   as pd 
import datetime as dt 

from config.SeleniumSettings          import SeleniumSettings 
from src.gather_data.NaverKeywords    import NaverKeywords    
from src.gather_data.NaverTopKeywords import NaverTopKeywords    
from src.gather_data.NaverViews       import NaverViews 

class FormOutputData:
    def __init__(self, selenium_object: SeleniumSettings) -> None:
        self.selenium_object = selenium_object 

    def form_output_settings_method(self, status_merge_col: str, output_file_name: str, output_sheets_names: list[str], naver_keywords_settings_dict: dict, naver_top_keywords_settings_dict: dict, naver_views_settings_dict: dict, status_rename_dict: dict, keywords_rename_dict: dict, keywords_status_rename_dict: dict, top_keywords_rename_dict: dict, top_keywords_status_rename_dict: dict, views_rename_dict: dict, views_status_rename_dict: dict) -> None:
        self.status_merge_col                 = status_merge_col
        self.output_file_name                 = output_file_name 
        self.output_sheets_names              = output_sheets_names 
        self.naver_keywords_settings_dict     = naver_keywords_settings_dict 
        self.naver_top_keywords_settings_dict = naver_top_keywords_settings_dict 
        self.naver_views_settings_dict        = naver_views_settings_dict 
        self.status_rename_dict               = status_rename_dict
        self.keywords_rename_dict             = keywords_rename_dict 
        self.keywords_status_rename_dict      = keywords_status_rename_dict 
        self.top_keywords_rename_dict         = top_keywords_rename_dict 
        self.top_keywords_status_rename_dict  = top_keywords_status_rename_dict
        self.views_rename_dict                = views_rename_dict 
        self.views_status_rename_dict         = views_status_rename_dict

    def naver_keywords_method(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        self.naver_keywords_object = NaverKeywords(self.selenium_object)
        self.naver_keywords_object.naver_keywords_settings_method(**self.naver_keywords_settings_dict)
        self.naver_keywords_object.get_keyword_data()

        naver_keyword_status_data = pd.DataFrame(self.naver_keywords_object.naver_data_status_check)
        naver_keyword_status_data["search_keyword"] = naver_keyword_status_data["search_keyword"].replace("티파니", "티파니앤코")

        naver_keyword_status_data = naver_keyword_status_data.rename(columns = self.keywords_status_rename_dict)
        naver_data_dataframe      = pd.DataFrame(self.naver_keywords_object.naver_data_dictionary).rename(columns = self.keywords_rename_dict)
        
        return naver_keyword_status_data, naver_data_dataframe 
    
    def naver_top_keywords_method(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        self.naver_top_keywords_object = NaverTopKeywords(self.selenium_object)
        self.naver_top_keywords_object.naver_top_keyword_settings_method(**self.naver_top_keywords_settings_dict)
        self.naver_top_keywords_object.get_keyword_data()

        naver_top_keywords_status_data = pd.DataFrame(self.naver_top_keywords_object.naver_top_data_status_check).drop(columns = ["date"]).rename(columns = self.top_keywords_status_rename_dict)
        naver_top_keywords_dataframe   = pd.DataFrame(self.naver_top_keywords_object.naver_top_keywords_dictionary).rename(columns = self.top_keywords_rename_dict)

        return naver_top_keywords_status_data, naver_top_keywords_dataframe
    
    def naver_views_method(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        self.naver_views_object = NaverViews(self.selenium_object)
        self.naver_views_object.naver_views_settings_method(**self.naver_views_settings_dict)
        self.naver_views_object.get_keyword_data()

        naver_views_status_data = pd.DataFrame(self.naver_views_object.naver_views_status_check).drop(columns = ["date"]).rename(columns = self.views_status_rename_dict)
        naver_views_dataframe   = pd.DataFrame(self.naver_views_object.naver_views_dictionary).rename(columns = self.views_rename_dict)

        return naver_views_status_data, naver_views_dataframe 
    
    def finalize_outputs(self) -> tuple[pd.ExcelWriter, list[pd.DataFrame]]:
        naver_keyword_status_dataframe, naver_data_dataframe    = self.naver_keywords_method()
        naver_top_keywords_status_data, naver_top_keywords_data = self.naver_top_keywords_method()
        naver_views_status_dataframe, naver_views_dataframe     = self.naver_views_method()

        output_status_data  = pd.merge(naver_keyword_status_dataframe, pd.merge(naver_top_keywords_status_data, naver_views_status_dataframe, how = "left", on = self.status_merge_col), how = "left", on = self.status_merge_col).rename(columns = self.status_rename_dict)
        excel_writer_object = pd.ExcelWriter(self.output_file_name.format(str(dt.datetime.now())[0:10]), engine = "openpyxl")
        results_data_list   = [output_status_data, naver_data_dataframe, naver_top_keywords_data, naver_views_dataframe]

        return excel_writer_object, results_data_list 
    
    def save_output_data(self):
        excel_writer_object, results_data_list = self.finalize_outputs()

        for (sheet_name, dataframe) in zip(self.output_sheets_names, results_data_list):
            dataframe.to_excel(excel_writer_object, sheet_name = sheet_name, index = False)

        excel_writer_object.close()

        return results_data_list
