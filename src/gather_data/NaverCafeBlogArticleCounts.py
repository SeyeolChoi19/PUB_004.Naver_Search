import datetime as dt 

from config.SeleniumSettings import SeleniumSettings 

class NaverCafeBlogArticleCounts:
    def __init__(self, selenium_object: SeleniumSettings):
        self.selenium_object = selenium_object 
        self.selenium_object.driver_settings()

    def naver_article_counts_settings_method(self, naver_cafe_urls: list[str], naver_blog_url: str, keywords_list: list[str]):
        self.naver_cafe_urls = naver_cafe_urls 
        self.naver_blog_url  = naver_blog_url 
        self.keywords_list   = keywords_list 

        self.naver_article_counts_status_check = {
            "date"                                : [str(dt.datetime.now())[0:10] for i in range(len(self.keywords_list))],
            "search_keyword"                      : self.keywords_list,
            "cafe_article_count_status"           : [],
            "cafe_article_count_non_trade_status" : [],
            "blog_article_count_status"           : []
        }

        self.naver_article_counts_dictionary = {
            "date"                         : [],
            "search_keyword"               : [],
            "cafe_article_count"           : [],
            "cafe_article_count_non_trade" : [],
            "blog_article_count"           : []
        }

    def article_count_yn(self, element_str: str, str_type: str):
        article_count = 0
        status_check  = 0

        if (self.selenium_object.check_for_element(element_str, str_type)):
            article_count = int(self.selenium_object.search_for_element(element_str, str_type).text.replace(",", "").replace("건", ""))
            status_check  = 1

        return article_count, status_check

    def get_cafe_article_counts(self):    
        def save_article_count(keyword: str):
            for url in self.naver_cafe_urls:
                self.selenium_object.driver.get(url.format(keyword))
                self.selenium_object.wait_for_element_to_be_visible("sub_text", "class")
                article_count, status_check = self.article_count_yn("sub_text", "class")
                self.naver_article_counts_status_check[(lambda x: "cafe_article_count_non_trade_status" if ("&em=" in x) else "cafe_article_count_status")(url)].append(status_check)
                self.naver_article_counts_dictionary[(lambda x: "cafe_article_count_non_trade" if ("&em=" in x) else "cafe_article_count")(url)].append(article_count)                
            
        for keyword in self.keywords_list:
            self.naver_article_counts_dictionary["date"].append(str(dt.datetime.now())[0:10])
            self.naver_article_counts_dictionary["search_keyword"].append(keyword)
            save_article_count(keyword)

    def get_blog_article_counts(self):
        for keyword in self.keywords_list:
            self.selenium_object.driver.get(self.naver_blog_url.format(keyword))
            self.selenium_object.wait_for_element_to_be_visible("search_number", "class")
            article_count, article_status = self.article_count_yn("search_number", "class")
            self.naver_article_counts_status_check["blog_article_count_status"].append(article_status)
            self.naver_article_counts_dictionary["blog_article_count"].append(article_count)
