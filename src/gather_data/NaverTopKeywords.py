import time

import datetime as dt 

from config.SeleniumSettings import SeleniumSettings 

class NaverTopKeywords:
    def __init__(self, selenium_object: SeleniumSettings) -> None: 
        self.selenium_object = selenium_object 
        self.selenium_object.driver_settings()

    def naver_top_keyword_settings_method(self, naver_search_url: str, keywords_list: list[str], keyword_filter_list: list[str]) -> None:
        self.naver_search_url    = naver_search_url 
        self.keywords_list       = keywords_list 
        self.keyword_filter_list = keyword_filter_list

        self.naver_top_data_status_check = {
            "date"               : [],
            "search_keyword"     : [],
            "completion_status"  : []
        }

        self.naver_top_keywords_dictionary = {
            "date"              : [],
            "search_keyword"    : [],
            "trending_keywords" : [],
            "term_ranking"      : []
        }

    def get_keyword_data(self) -> None:
        def xpath_switch() -> list[str]: 
            keyword_list = ["extraction_failed"]
            keyword_list = self.selenium_object.search_for_element("fds-ugc-body-popular-topic-scroller", "class").text.split("\n") if (self.selenium_object.check_for_element('fds-ugc-body-popular-topic-scroller', "class")) else keyword_list

            return keyword_list
        
        def inner_function(keyword: str, keywords_list: list[str]) -> None:
            keywords_list = [i for i in keywords_list if (i not in self.keyword_filter_list)]

            for (rank_num, sub_keyword) in enumerate(keywords_list):
                self.naver_top_keywords_dictionary["date"].append(str(dt.datetime.now())[0:19])
                self.naver_top_keywords_dictionary["search_keyword"].append(keyword)
                self.naver_top_keywords_dictionary["trending_keywords"].append(sub_keyword)
                self.naver_top_keywords_dictionary["term_ranking"].append(str(rank_num + 1).zfill(2))
        
        def status_check(keyword: str, keywords_list: list[str]) -> int:
            extraction_status = 1 if (len(keywords_list) > 1) else 0
            
            self.naver_top_data_status_check["date"].append(str(dt.datetime.now())[0:19])
            self.naver_top_data_status_check["search_keyword"].append(keyword)
            self.naver_top_data_status_check["completion_status"].append(extraction_status)

            return extraction_status
                
        for keyword in self.keywords_list:
            self.selenium_object.driver.get(self.naver_search_url.format(keyword))
            time.sleep(5)
            keywords_list     = xpath_switch()
            extraction_status = status_check(keyword, keywords_list)
            inner_function(keyword, (lambda extraction_status, keywords_list: keywords_list if (extraction_status == 1) else ["extraction_failed"])(extraction_status, keywords_list))
