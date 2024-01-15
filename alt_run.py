import json 

from src.upload_data.UploadToPostgres import UploadToPostgres 

if (__name__ == "__main__"):
    with open("./config/NaverScraperConfig.json", "r", encoding = "utf-8") as f:
        config_dict = json.load(f)
    
    upload_to_postgres = UploadToPostgres()
    upload_to_postgres.upload_to_postgres_settings(**config_dict["UploadToGoogleWithNotifications"]["upload_to_postgres_settings"])
    upload_to_postgres.main_logic()
