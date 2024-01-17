package org.config;

import java.time.Duration;
import java.util.Arrays;
import java.util.List;
import java.lang.Exception;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedCondition;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class SeleniumSettings {
    String  driverPath;
    Integer maxWaitTime;

    public ChromeDriver  driver;
    public WebDriverWait wait;

    SeleniumSettings(String driverPath, int maxWaitTime) {
        this.driverPath  = driverPath;
        this.maxWaitTime = maxWaitTime;
    }

    public void driverSettings() {
        String[] optionsList = new String[]{
                "window-size=1920x1080",
                "disable-gpu",
                "start-maximized",
                "--remote-allow-origins=*",
                "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        };

        ChromeOptions options = new ChromeOptions();
        System.setProperty("webdriver.chrome.driver", this.driverPath);
        options.addArguments(Arrays.asList(optionsList));
        this.driver = new ChromeDriver(options);
        this.wait   = new WebDriverWait(this.driver, Duration.ofSeconds(maxWaitTime));
    }

    public void waitForElement(String elementStr, String elementType) throws Exception {
        switch (elementType.toLowerCase()) {
            case "xpath" -> wait.until(ExpectedConditions.presenceOfElementLocated(By.xpath(elementStr)));
            case "id"    -> wait.until(ExpectedConditions.presenceOfElementLocated(By.id(elementStr)));
            case "class" -> wait.until(ExpectedConditions.presenceOfElementLocated(By.className(elementStr)));
            default      -> throw new Exception("Unrecognized element type");
        }
    }

    public boolean checkForElement(String elementStr, String elementType) throws Exception {
        boolean returnValue;

        switch (elementType.toLowerCase()) {
            case "xpath" -> returnValue = driver.findElements(By.xpath(elementStr)).size() > 0;
            case "id"    -> returnValue = driver.findElements(By.id(elementStr)).size() > 0;
            case "class" -> returnValue = driver.findElements(By.className(elementStr)).size() > 0;
            default      -> throw new Exception("Unrecognized element type");
        }

        return returnValue;
    }

    public WebElement searchForElement(String elementStr, String elementType) throws Exception {
        WebElement returnValue;

        switch (elementType.toLowerCase()) {
            case "xpath" -> returnValue = driver.findElement(By.xpath(elementStr));
            case "id"    -> returnValue = driver.findElement(By.id(elementStr));
            case "class" -> returnValue = driver.findElement(By.className(elementStr));
            default      -> throw new Exception("Unrecognized element type");
        }

        return returnValue;
    }

    public List<WebElement> searchForElements(String elementStr, String elementType) throws Exception {
        List<WebElement> returnValue;

        switch (elementType.toLowerCase()) {
            case "xpath" -> returnValue = driver.findElements(By.xpath(elementStr));
            case "id"    -> returnValue = driver.findElements(By.id(elementStr));
            case "class" -> returnValue = driver.findElements(By.className(elementStr));
            default      -> throw new Exception("Unrecognized element type");
        }

        return returnValue;
    }

    public void clickOnElement(String elementStr, String elementType) throws Exception {
        switch (elementType.toLowerCase()) {
            case "xpath" -> driver.findElement(By.xpath(elementStr)).click();
            case "id"    -> driver.findElement(By.id(elementStr)).click();
            case "class" -> driver.findElement(By.className(elementStr)).click();
            default      -> throw new Exception("Unrecognized element type");
        }
    }

    public void sendStringToElement(String elementStr, String elementType, String keyword) throws Exception {
        switch (elementType.toLowerCase()) {
            case "xpath" -> driver.findElement(By.xpath(elementStr)).sendKeys(keyword);
            case "id"    -> driver.findElement(By.id(elementStr)).sendKeys(keyword);
            case "class" -> driver.findElement(By.className(elementStr)).sendKeys(keyword);
            default      -> throw new Exception("Unrecognized element type");
        }
    }
}
