import requests, time, json, urllib.request 

import pandas as pd 

class GetMonthlySearch:
    def monthly_search_settings_method(self, keywords_tool_url: str, search_ad_login_url: str, naver_account: str, naver_password: str, open_api_id: str, open_api_secret: str, open_api_url: str, start_date: str, end_date: str, keywords_list: list[str], dates_list: list[str], login_headers: dict, authorization_headers: dict, parameters_dict: dict):
        def return_base_dataframe(dates_list: list[str], keywords_list: list[str]):
            empty_dataframe = {
                "date"    : [],
                "keyword" : []
            }

            for keyword in keywords_list: 
                for date in dates_list:
                    empty_dataframe["date"].append(date)
                    empty_dataframe["keyword"].append(keyword)

            return pd.DataFrame(empty_dataframe)

        self.keywords_tool_url     = keywords_tool_url 
        self.search_ad_login_url   = search_ad_login_url
        self.keywords_list         = keywords_list 
        self.dates_list            = dates_list
        self.login_headers         = login_headers
        self.authorization_headers = authorization_headers
        self.parameters_dict       = parameters_dict 
        self.naver_login_dict      = {"loginId" : naver_account, "loginPwd" : naver_password}
        self.base_dataframe        = return_base_dataframe(dates_list, keywords_list)
        self.__open_api_url        = open_api_url 
        self.__open_api_id         = open_api_id 
        self.__open_api_secret     = open_api_secret
        self.open_api_body_dict    = { 
            "startDate" : start_date,
            "endDate"   : end_date,
            "timeUnit"  : "date"
        }

        self.naver_ad_daily_search_values = {
            "keyword"      : [],
            "date"         : [],
            "ratio_values" : []
        }

    def get_monthly_data(self):
        def modify_headers(keyword: str, login_request: requests):
            self.authorization_headers["authorization"] = f"Bearer {login_request.json()['token']}"
            
            self.parameters_dict["hintKeywords"] = keyword 
            self.parameters_dict["keyword"]      = keyword 

        self.parse_list = []
        
        for keyword in self.keywords_list:
            login_request   = requests.post(self.search_ad_login_url, headers = self.login_headers, data = json.dumps(self.naver_login_dict))
            session_object  = requests.session()
            modify_headers(keyword, login_request)
            response_object = session_object.get(self.keywords_tool_url, headers = self.authorization_headers, params = self.parameters_dict)
            self.parse_list.append({"keyword" : keyword, "ntp" : response_object.json()})

    def parse_monthly_data(self):
        index_num, temp_list, temp_length = 0, [], len(self.parse_list[0]["ntp"]["keywordList"][0]["monthlyProgressList"]["monthlyLabel"])

        for keyword in self.keywords_list:
            for json_index in range(temp_length):
                try:
                    monthly_progress_pc_count     = self.parse_list[index_num]["ntp"]["keywordList"][0]["monthlyProgressList"]["monthlyProgressPcQcCnt"][json_index]
                    monthly_progress_mobile_count = self.parse_list[index_num]["ntp"]["keywordList"][0]["monthlyProgressList"]["monthlyProgressMobileQcCnt"][json_index]
                    monthly_label                 = f'{self.parse_list[index_num]["ntp"]["keywordList"][0]["monthlyProgressList"]["monthlyLabel"][json_index]}-01'
                    monthly_total_progress_count  = monthly_progress_pc_count + monthly_progress_mobile_count 
                    temp_list.append({
                        "keyword"        : keyword, 
                        "date"           : monthly_label,
                        "absolute_value" : monthly_total_progress_count
                    })
                except:
                    pass 
                index_num += 1

        self.naver_ad_monthly_search_values = pd.merge(self.base_dataframe, pd.DataFrame(temp_list), how = "left")

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
        
        def save_api_data(keyword: str, results_object: dict):
            for index in range(0, len(results_object["results"][0]["data"])):
                period_value = results_object["results"][0]["data"][index]["period"]
                ratio_value  = results_object["results"][0]["data"][index]["ratio"]
                results_list = [keyword, period_value, ratio_value]

                for (key, value) in zip(self.naver_ad_daily_search_values.keys(), results_list):
                    self.naver_ad_daily_search_values[key].append(value)

        for keyword in self.keywords_list:
            response_object = urllib.request.urlopen(get_response_object(keyword), data = json.dumps(self.open_api_body_dict).encode("utf-8"))
            results_object  = json.loads(response_object.read().decode("utf-8"))
            save_api_data(keyword, results_object)
            time.sleep(0.5)

    def form_output_data_table(self):
        month_dataframe = self.naver_ad_monthly_search_values.copy()
        daily_dataframe = pd.DataFrame(self.naver_ad_daily_search_values)
        dataframe_list  = []

        for keyword in self.keywords_list:
            sub_month_dataframe = month_dataframe[month_dataframe["keyword"] == keyword]
            sub_daily_dataframe = daily_dataframe[daily_dataframe["keyword"] == keyword]
            actual_value_sum    = sub_month_dataframe["absolute_value"].sum()
            ratio_value_sum     = sub_daily_dataframe["ratio_values"].sum()

            sub_daily_dataframe["absolute_sum"] = actual_value_sum
            sub_daily_dataframe["ratio_sum"]    = ratio_value_sum 
            sub_daily_dataframe["final_value"]  = (sub_daily_dataframe["ratio_values"] * sub_daily_dataframe["absolute_sum"]) / sub_daily_dataframe["ratio_sum"]
            dataframe_list.append(sub_daily_dataframe)
        
        return pd.concat(dataframe_list)
