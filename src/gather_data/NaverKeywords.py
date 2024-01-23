import time

import datetime as dt 

from config.SeleniumSettings import SeleniumSettings 

class NaverKeywords:
    def __init__(self, selenium_object: SeleniumSettings) -> None: 
        self.selenium_object = selenium_object 
        self.selenium_object.driver_settings()

    def naver_keywords_settings_method(self, naver_search_url: str, keywords_list: list[str]) -> None: 
        self.naver_search_url = naver_search_url 
        self.keywords_list    = keywords_list 
        
        self.naver_data_status_check = {
            "date"               : [],
            "search_keyword"     : [],
            "completion_status"  : []
        }

        self.naver_data_dictionary = {
            "date"              : [],
            "search_keyword"    : [],
            "autocomplete_term" : [],
            "term_ranking"      : []
        }

    def get_keyword_data(self) -> None: 
        def save_status_data(keyword: str, extracted_keywords: list[str]) -> int:
            extraction_status = 1 if ((len(extracted_keywords) >= 1) and (extracted_keywords[0] != "extraction_failed")) else 0

            self.naver_data_status_check["date"].append(str(dt.datetime.now())[0:10])
            self.naver_data_status_check["search_keyword"].append(keyword)
            self.naver_data_status_check["completion_status"].append(extraction_status)

            return extraction_status

        def save_crawled_data(keyword: str, extracted_keywords: str) -> None:
            for (rank_num, word) in enumerate(extracted_keywords):
                self.naver_data_dictionary["date"].append(str(dt.datetime.now())[0:10])
                self.naver_data_dictionary["search_keyword"].append(keyword)
                self.naver_data_dictionary["autocomplete_term"].append(word)
                self.naver_data_dictionary["term_ranking"].append(str(rank_num + 1).zfill(2))
        
        self.selenium_object.driver.get(self.naver_search_url)
        time.sleep(4)

        for keyword in self.keywords_list: 
            self.selenium_object.send_string_to_element("/html/body/div[2]/div[1]/div/div[3]/div[2]/div/form/fieldset/div/input", keyword)  
            time.sleep(4)
            extracted_keywords = [i for i in self.selenium_object.search_for_element("/html/body/div[2]/div[1]/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[1]/ul").text.split("\n") if ("추가" not in i)]
            extraction_status  = save_status_data(keyword, extracted_keywords)
            save_crawled_data(keyword, (lambda extraction_status, extracted_keywords: extracted_keywords if (extraction_status == 1) else ["extraction_failed"])(extraction_status, extracted_keywords))
            self.selenium_object.search_for_element("/html/body/div[2]/div[1]/div/div[3]/div[2]/div/form/fieldset/div/input").clear()
