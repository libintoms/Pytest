from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from openpyxl import load_workbook
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import pytest
from selenium.webdriver.common.keys import Keys


class Test_SIcheck():

    @pytest.fixture()
    def test_setup(self):
        # initiating browser
        global driver
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        driver = webdriver.Chrome(
            "D:/OneDrive - CACTUS/Python/Sel_python/drivers/chromedriver.exe", chrome_options=chrome_options)
        driver.implicitly_wait(5)

        # exit browser
        yield
        driver.close()
        driver.quit()
        print("Test completed")

    def test_01(self,test_setup):
        driver.get('https://www.sportsadda.com/')
        driver.find_element_by_xpath("//div[@id='cookiebtn']").click()

        actions = ActionChains(driver)

        card_window=driver.find_element_by_xpath("//div[@class='si-fixCntnr si-fix-widget']")
        # card_window.click()

        actions.move_to_element(card_window).perform()
        top_card=driver.find_element_by_xpath(
            "//span[contains(text(),'Match 28')]")

        scroll_bar=driver.find_element_by_xpath("//div[@class='swiper-scrollbar']")
        scroll_bar.click()

        # driver.execute_script("arguments[0].scrollIntoView();", top_card)

        # card_window=driver.switch_to.active_element
        driver.execute_script("arguments[0].focus();", card_window)
        actions.move_to_element(top_card).perform()
        actions.move_to_element(top_card).perform()
        # top_card.location_once_scrolled_into_view
        wait=WebDriverWait(driver, 300)
        wait.until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'Match 28')]")))

        top_card.click()



        time.sleep(10)



