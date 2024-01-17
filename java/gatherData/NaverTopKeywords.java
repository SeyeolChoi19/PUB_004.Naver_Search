package org.gatherData;

import java.lang.Thread;
import java.time.Duration;
import java.time.LocalDateTime;
import java.util.Arrays;
import org.json.JSONArray;
import org.json.JSONObject;
import org.config.SeleniumSettings;

public class NaverTopKeywords {
    String   naverSearchUrl;
    String[] keywordsList, keywordFilterList;

    public JSONArray        naverTopDataStatusArray, naverTopKeywordsDictionary;
    public SeleniumSettings seleniumObject;

    NaverTopKeywords(SeleniumSettings seleniumObject) {
        this.seleniumObject = seleniumObject;
        seleniumObject.driverSettings();
    }

    public void naverTopKeywordsSettingsMethod(String naverSearchUrl, String[] keywordsList, String[] keywordFilterList) {
        this.naverSearchUrl             = naverSearchUrl;
        this.keywordsList               = keywordsList;
        this.keywordFilterList          = keywordFilterList;
        this.naverTopDataStatusArray    = new JSONArray();
        this.naverTopKeywordsDictionary = new JSONArray();
    }

    String[] xpathSwitch() throws Exception {
        String[] keywordList = new String[] {"extraction_failed"};

        return (seleniumObject.checkForElement("fds-ugc-body-popular-topic-scroller", "class")) ? seleniumObject.searchForElement("fds-ugc-body-popular-topic-scroller", "class").getText().split("\n") : keywordList;
    }

    int statusCheck(String keyword, String[] keywordsList) {
        JSONObject singleInnerJson  = new JSONObject();
        Integer    extractionStatus = (keywordsList.length > 1) ? 1 : 0;

        singleInnerJson.put("date",              String.valueOf(LocalDateTime.now()).substring(0, 10));
        singleInnerJson.put("search_keyword",    keyword);
        singleInnerJson.put("completion_status", extractionStatus);

        return extractionStatus;
    }

    void innerFunction(String keyword, String[] keywordsList) {
        int counterVar = 1;

        for (String subKeyword : keywordsList) {
            if (!Arrays.asList(keywordFilterList).contains(subKeyword)) {
                JSONObject naverTopDataJObject = new JSONObject();
                naverTopDataJObject.put("date", String.valueOf(LocalDateTime.now()).substring(0, 10));
                naverTopDataJObject.put("search_keyword", keyword);
                naverTopDataJObject.put("trending_keywords", subKeyword);
                naverTopDataJObject.put("term_ranking", String.format("%02d", counterVar));
                naverTopKeywordsDictionary.put(naverTopDataJObject);
                counterVar += 1;
            }
        }
    }

    public void getKeywordData() throws InterruptedException, Exception {
        for (String keyword : keywordsList) {
            seleniumObject.driver.get(String.format(naverSearchUrl, keyword));
            Thread.sleep(Duration.ofSeconds(5));
            String[] keywordsList      = xpathSwitch();
            Integer  extractionStatus  = statusCheck(keyword, keywordsList);
            String[] finalizedKeywords = (extractionStatus == 1) ? keywordsList : new String[] {"extraction_failed"};
            innerFunction(keyword, finalizedKeywords);
        }
    }
}
