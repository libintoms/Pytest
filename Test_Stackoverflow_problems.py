from seleniumwire import webdriver
import pytest
from selenium.webdriver.chrome.options import Options
import time
import allure
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Test_main():

    @pytest.fixture()
    def test_setup(self):
        # initiating browser
        chrome_options = Options()
        chrome_options.binary_location=\
            r"C:\Users\libin.thomas\AppData\Local\Google\Chrome\Application\chrome.exe"
        chrome_options.add_argument('--start-maximized')
        # chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(executable_path=
                                       r"D:/OneDrive - CACTUS/Python/Sel_python/drivers/chromedriver v86/chromedriver.exe",
                                       options=chrome_options)

        # terminate script
        yield
        self.driver.close()
        self.driver.quit()
        print("Test completed")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Verify BigInt script in page")
    def testcase_01(self, test_setup):
        self.driver.get('https://www.aliexpress.com/')
        # wait = WebDriverWait(self.driver, 500)
        # wait.until(EC.presence_of_element_located(
        #     (By.XPATH, '//a[@id="switcher-info"]')))
        time.sleep(10)
        self.driver.find_element_by_xpath('//span[@class="currency"]').click()
        time.sleep(5)
        self.driver.find_element_by_xpath('//a[@data-currency="EUR"]').click()
        time.sleep(5)
        # self.driver.find_element_by_class_name("accept_button").click()

        # self.driver.find_element_by_xpath('//div[@class="left_button_inner generic_menu_button ti-comments-smiley"]').click()
        # wait = WebDriverWait(self.driver, 500)
        # wait.until(EC.presence_of_element_located((By.XPATH, "//input[@class='phonemask']")))
        # self.driver.find_element_by_xpath('//input[@class="phonemask"]').click()
        # self.driver.find_element_by_xpath('//input[@class="phonemask"]').send_keys('122525')

