import json

from src.upload_data.UploadToGoogleWithNotifications import UploadToGoogleWithNotifications 

if (__name__ == "__main__"):
    with open("./config/NaverScraperConfig.json", "r", encoding = "utf-8") as f:
        config_dict = json.load(f)

    upload_to_google_object = UploadToGoogleWithNotifications()
    upload_to_google_object.upload_to_google_settings(**config_dict["UploadToGoogleWithNotifications"]["upload_to_google_settings"])
    upload_to_google_object.upload_to_gcp()
