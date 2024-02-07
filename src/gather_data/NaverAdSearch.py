import hashlib, hmac, base64, time, requests, urllib, json

import datetime as dt
import pandas   as pd

class NaverAdSearch:
    def naver_ad_search_settings_method(self, search_api_url: str, search_api_key: str, search_secret_key: str, search_customer_id: str, keywords_tool_url: str, open_api_id: str, open_api_secret: str, open_api_url: str, start_date: str, end_date: str, dates_list: list[str], search_keywords: list[str]):
        self.__search_api_url     = search_api_url
        self.__search_api_key     = search_api_key
        self.__search_secret_key  = search_secret_key
        self.__search_customer_id = search_customer_id
        self.__keywords_tool_url  = keywords_tool_url
        self.__open_api_id        = open_api_id
        self.__open_api_secret    = open_api_secret
        self.__open_api_url       = open_api_url
        self.start_date           = start_date
        self.end_date             = end_date
        self.dates_list           = dates_list
        self.search_keywords      = search_keywords
        self.open_api_body_dict   = {
            "startDate" : self.start_date,
            "endDate"   : self.end_date,
            "timeUnit"  : "date"
        }

        self.naver_ad_monthly_search_values = {
            "month_string"         : [],
            "monthly_pc_count"     : [],
            "monthly_mobile_count" : [],
            "monthly_total_count"  : [],
            "search_keyword"       : []
        }

        self.naver_ad_daily_search_values = {
            "search_keyword"  : [],
            "date_string"     : [],
            "ratio_values"    : []
        }

    def __generate_credentials(self, timestamp: str, method: str, uri: str, secret_key: str):
        message  = f"{timestamp}.{method}.{uri}"
        hash_str = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)
        hash_str.hexdigest()

        return base64.b64encode(hash_str.digest())

    def __get_headers(self, uri: str, api_key: str, secret_key: str, customer_id: str):
        timestamp   = str(round(time.time() * 1000))
        signature   = self.__generate_credentials(timestamp, "GET", uri, secret_key)
        output_dict = {
            "Content-Type" : "application/json; charset=UTF-8",
            "X-Timestamp"  : timestamp,
            "X-API-KEY"    : api_key,
            "X-Customer"   : customer_id,
            "X-Signature"  : signature
        }

        return output_dict

    def get_monthly_search_results(self):
        for keyword in self.search_keywords:
            response_object      = requests.get(f"{self.__search_api_url}{self.__keywords_tool_url.format(keyword)}", headers = self.__get_headers("/keywordstool", self.__search_api_key, self.__search_secret_key, self.__search_customer_id)).json()
            month_string         = f"{str(dt.datetime.now())[0:7]}-01"
            monthly_pc_count     = response_object["keywordList"][0]["monthlyPcQcCnt"]
            monthly_mobile_count = response_object["keywordList"][0]["monthlyMobileQcCnt"]
            monthly_total_count  = monthly_pc_count + monthly_mobile_count
            results_list         = [month_string, monthly_pc_count, monthly_mobile_count, monthly_total_count, keyword]

            for (key, value) in zip(self.naver_ad_monthly_search_values.keys(), results_list):
                self.naver_ad_monthly_search_values[key].append(value)

    def get_daily_search_results(self):
        def get_response_object(keyword: str):
            self.open_api_body_dict["keywordGroups"] = [{
                "groupName" : str(keyword),
                "keywords"  : [str(keyword)]
            }]

            request_object = urllib.request.Request(self.__open_api_url)
            request_object.add_header("X-Naver-Client-Id", self.__open_api_id)
            request_object.add_header("X-Naver-Client-Secret", self.__open_api_secret)
            request_object.add_header("Content-Type", "application/json")

            return request_object

        def save_api_data(results_object: dict):
            for index in range(0, len(results_object["results"][0]["data"])):
                period_value = results_object["results"][0]["data"][index]["period"]
                ratio_value  = results_object["results"][0]["data"][index]["ratio"]
                results_list = [keyword, period_value, ratio_value]

                for (key, value) in zip(self.naver_ad_daily_search_values.keys(), results_list):
                    self.naver_ad_daily_search_values[key].append(value)

        for keyword in self.search_keywords:
            response_object = urllib.request.urlopen(get_response_object(keyword), data = json.dumps(self.open_api_body_dict).encode("utf-8"))
            results_object  = json.loads(response_object.read().decode("utf-8"))
            save_api_data(results_object)
            time.sleep(0.5)

    def form_output_data_table(self):
        month_dataframe = pd.DataFrame(self.naver_ad_monthly_search_values)
        daily_dataframe = pd.DataFrame(self.naver_ad_daily_search_values)
        dataframe_list  = []

        for keyword in self.search_keywords:
            sub_month_dataframe = month_dataframe[month_dataframe["search_keyword"] == keyword]
            sub_daily_dataframe = daily_dataframe[daily_dataframe["search_keyword"] == keyword]
            actual_value_sum    = sub_month_dataframe["monthly_total_count"].sum()
            ratio_value_sum     = sub_daily_dataframe["ratio_values"].sum()

            sub_daily_dataframe["actual_sum"]  = actual_value_sum
            sub_daily_dataframe["ratio_sum"]   = ratio_value_sum
            sub_daily_dataframe["final_value"] = (sub_daily_dataframe["ratio_values"] * sub_daily_dataframe["actual_sum"]) / sub_daily_dataframe["ratio_sum"]
            dataframe_list.append(sub_daily_dataframe)

        return pd.concat(dataframe_list)

if (__name__ == "__main__"):
    with open("NaverAdSearchConfig.json", "r", encoding = "utf-8") as f:
        config_dict = json.load(f)

    naver_ad_object = NaverAdSearch()
    naver_ad_object.naver_ad_search_settings_method(**config_dict["NaverAdSearch"]["naver_ad_search_settings_method"])
    naver_ad_object.get_monthly_search_results()
    naver_ad_object.get_daily_search_results()
    output_table = naver_ad_object.form_output_data_table()
