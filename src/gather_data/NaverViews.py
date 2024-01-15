import time 

import datetime as dt 

from config.SeleniumSettings import SeleniumSettings 

class NaverViews: 
    def __init__(self, selenium_object: SeleniumSettings) -> None: 
        self.selenium_object = selenium_object 
        self.selenium_object.driver_settings()

    def naver_views_settings_method(self, naver_views_url: str, keywords_list: list[str]) -> None:
        self.naver_views_url = naver_views_url 
        self.keywords_list   = keywords_list 

        self.naver_views_status_check = {
            "date"               : [],
            "search_keyword"     : [],
            "completion_status"  : []
        }

        self.naver_views_dictionary = {
            "date"             : [],
            "search_keyword"   : [],
            "related_keywords" : [],
            "term_ranking"     : [],
            "load_more_yn"     : []
        }

    def get_keyword_data(self) -> None: 
        def press_button_yn(extraction_status: int, keyword_list: list[str]) -> list[str]: 
            output_list = keyword_list
            number_list = (lambda x: len(x) if (x[-1] != "더보기") else len(x) - 1)(output_list) * [0]

            if (keyword_list[-1] == "더보기"):
                self.selenium_object.search_for_element('/html/body/div[3]/div[2]/div/div[2]/section[1]/div/div[2]/div[1]/a').click()
                output_list = self.selenium_object.search_for_element("related_srch", "class").text.split("\n")
                number_list = number_list + ((len(output_list) - (len(keyword_list) - 1)) * [1])
            
            return [output_list, number_list]

        def save_data(keyword: str, keywords_and_numbers: list[list[str], list[int]]) -> None: 
            rank_list  = list(range(len(keywords_and_numbers[0])))
            zip_object = zip(rank_list, keywords_and_numbers[0], keywords_and_numbers[1])

            for (rank_num, sub_keyword, more_yn) in zip_object: 
                self.naver_views_dictionary["date"].append(str(dt.datetime.now())[0:19])
                self.naver_views_dictionary["search_keyword"].append(keyword)
                self.naver_views_dictionary["related_keywords"].append(sub_keyword)
                self.naver_views_dictionary["term_ranking"].append(str(rank_num + 1).zfill(2))
                self.naver_views_dictionary["load_more_yn"].append(more_yn)

        def check_exists_yn():
            extraction_status = 0

            if (self.selenium_object.check_for_element("related_srch", "class")):
                extraction_status = 1

            return extraction_status

        def status_check(keyword: str, extraction_status: int):
            self.naver_views_status_check["date"].append(str(dt.datetime.now())[0:19])
            self.naver_views_status_check["search_keyword"].append(keyword)
            self.naver_views_status_check["completion_status"].append(extraction_status)
        
        for keyword in self.keywords_list:
            self.selenium_object.driver.get(self.naver_views_url.format(keyword))
            time.sleep(5)
            extraction_status    = check_exists_yn()
            keywords_list        = self.selenium_object.search_for_element("related_srch", "class").text.split("\n") if (extraction_status == 1) else ["extraction_failed"]
            keywords_and_numbers = press_button_yn(extraction_status, keywords_list)
            status_check(keyword, extraction_status)
            save_data(keyword, keywords_and_numbers)
