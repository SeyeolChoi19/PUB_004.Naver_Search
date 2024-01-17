package org.gatherData;

import java.lang.Thread;
import java.time.Duration;
import java.time.LocalDateTime;
import org.json.JSONArray;
import org.json.JSONObject;
import org.config.SeleniumSettings;

public class NaverKeywords {
    String   naverSearchUrl;
    String[] keywordsList;

    public JSONArray        naverDataStatusArray, naverDataDictionary;
    public SeleniumSettings seleniumObject;

    NaverKeywords(SeleniumSettings seleniumObject) {
        this.seleniumObject = seleniumObject;
        seleniumObject.driverSettings();
    }

    public void naverKeywordsSettingsMethod(String naverSearchUrl, String[] keywordsList) {
        this.naverSearchUrl       = naverSearchUrl;
        this.keywordsList         = keywordsList;
        this.naverDataStatusArray = new JSONArray();
        this.naverDataDictionary  = new JSONArray();
    }

    int saveStatusData(String keyword, String[] extractedKeywords) {
        JSONObject singleInnerJson  = new JSONObject();
        Integer    extractionStatus = ((extractedKeywords.length >= 1) && (!extractedKeywords[0].equals("extracted_failed"))) ? 1 : 0;

        singleInnerJson.put("date",              String.valueOf(LocalDateTime.now()).substring(0, 10));
        singleInnerJson.put("search_keyword",    keyword);
        singleInnerJson.put("completion_status", extractionStatus);
        naverDataStatusArray.put(singleInnerJson);

        return extractionStatus;
    }

    void saveCrawledData(String keyword, String[] extractedKeywords) {
        int counterVar = 1;

        for (String subKeyword : extractedKeywords) {
            if (!subKeyword.equals("추가")) {
                JSONObject naverDataJObject = new JSONObject();
                naverDataJObject.put("date",              String.valueOf(LocalDateTime.now()).substring(0, 10));
                naverDataJObject.put("search_keyword",    keyword);
                naverDataJObject.put("autocomplete_term", subKeyword);
                naverDataJObject.put("term_ranking",      String.format("%02d", counterVar));
                naverDataDictionary.put(naverDataJObject);
                counterVar += 1;
            }
        }
    }

    public void getKeywordData() throws InterruptedException, Exception {
        seleniumObject.driver.get(naverSearchUrl);
        Thread.sleep(Duration.ofSeconds(4));

        for (String keyword : keywordsList) {
            seleniumObject.sendStringToElement("/html/body/div[2]/div[1]/div/div[3]/div[2]/div/form/fieldset/div/input", "xpath", keyword);
            Thread.sleep(Duration.ofSeconds(4));
            String[] extractedKeywords = seleniumObject.searchForElement("/html/body/div[2]/div[1]/div/div[3]/div[2]/div/form/fieldset/div/input", "xpath").getText().split("\n");
            int      extractionStatus  = saveStatusData(keyword, extractedKeywords);
            String[] finalizedKeywords = (extractionStatus == 1) ? extractedKeywords : new String[] {"extraction_failed"};
            saveCrawledData(keyword, finalizedKeywords);
            seleniumObject.searchForElement("/html/body/div[2]/div[1]/div/div[3]/div[2]/div/form/fieldset/div/input", "xpath").clear();
        }
    }
}
