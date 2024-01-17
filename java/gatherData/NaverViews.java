package org.gatherData;

import java.lang.Thread;
import java.util.stream.IntStream;
import java.time.Duration;
import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.ArrayList;
import org.json.JSONArray;
import org.json.JSONObject;
import org.config.SeleniumSettings;

public class NaverViews {
    String   naverViewsUrl;
    String[] keywordsList;

    public JSONArray        naverViewsStatusArray, naverViewsDataDictionary;
    public SeleniumSettings seleniumObject;

    NaverViews(SeleniumSettings seleniumObject) {
        this.seleniumObject = seleniumObject;
        seleniumObject.driverSettings();
    }

    public void naverViewsSettingsMethod(String naverViewsUrl, String[] keywordsList) {
        this.naverViewsUrl            = naverViewsUrl;
        this.keywordsList             = keywordsList;
        this.naverViewsStatusArray    = new JSONArray();
        this.naverViewsDataDictionary = new JSONArray();
    }

    int checkExistsYn() throws Exception {
        int extractionStatus = 0;

        if (seleniumObject.checkForElement("related_srch", "class")) {
            extractionStatus = 1;
        }

        return extractionStatus;
    }

    ArrayList<String> pressButtonYn(String[] keywordsList) throws Exception {
        int               listSize    = (!keywordsList[keywordsList.length - 1].equals("더보기")) ? keywordsList.length : keywordsList.length - 1;
        ArrayList<String> stringArray = new ArrayList<>(Arrays.asList(keywordsList));

        if (keywordsList[keywordsList.length - 1].equals("더보기")) {
            seleniumObject.searchForElement("/html/body/div[3]/div[2]/div/div[2]/section[1]/div/div[2]/div[1]/a", "xpath").click();
            String[] outputList     = seleniumObject.searchForElement("related_srch", "class").getText().split("\n");
            IntStream.range(0, listSize).forEach((int member) -> stringArray.add("0"));
            IntStream.range(0, outputList.length - (keywordsList.length - 1)).forEach((int member) -> stringArray.add("1"));
        }

        return stringArray;
    }

    void statusCheck(String keyword, int extractionStatus) {
        JSONObject naverInnerJsonObject = new JSONObject();
        naverInnerJsonObject.put("date",              String.valueOf(LocalDateTime.now()).substring(0, 10));
        naverInnerJsonObject.put("search_keyword",    keyword);
        naverInnerJsonObject.put("completion_status", extractionStatus);
        naverViewsStatusArray.put(naverInnerJsonObject);
    }

    void saveData(String keyword, ArrayList<String> wordsAndNumbers) {
        Integer            counterVar     = 1;
        ArrayList<String>  keywordsArray  = new ArrayList<>();
        ArrayList<Integer> numbersArray   = new ArrayList<>();
        IntStream.range(0, wordsAndNumbers.size() / 2).forEach((int indexNumber) -> keywordsArray.add(wordsAndNumbers.get(indexNumber)));
        IntStream.range(wordsAndNumbers.size() / 2, wordsAndNumbers.size()).forEach((int indexNumber) -> numbersArray.add(Integer.valueOf(wordsAndNumbers.get(indexNumber))));

        for (int i = 0; i < keywordsArray.size(); i++) {
            JSONObject naverInnerJson = new JSONObject();
            naverInnerJson.put("date",             String.valueOf(LocalDateTime.now()).substring(0, 10));
            naverInnerJson.put("search_keyword",   keyword);
            naverInnerJson.put("related_keywords", keywordsArray.get(i));
            naverInnerJson.put("term_ranking",     counterVar);
            naverInnerJson.put("load_more_yn",     numbersArray.get(i));
            naverViewsDataDictionary.put(naverInnerJson);
        }
    }

    public void getKeywordData() throws InterruptedException, Exception {
        for (String keyword : keywordsList) {
            seleniumObject.driver.get(String.format(naverViewsUrl, keyword));
            Thread.sleep(Duration.ofSeconds(5));
            int               extractionStatus = checkExistsYn();
            String[]          keywordsList     = (extractionStatus == 1) ? seleniumObject.searchForElement("related_srch", "class").getText().split("\n") : new String[] {"extraction_failed"};
            ArrayList<String> wordsAndNumbers  = pressButtonYn(keywordsList);
            statusCheck(keyword, extractionStatus);
            saveData(keyword, wordsAndNumbers);
        }
    }
}
