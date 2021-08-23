from seleniumwire import webdriver
import pytest
from selenium.webdriver.chrome.options import Options
import time
import allure
import base64

class Test_main():

    @pytest.fixture()
    def test_setup(self):
        # initiating browser
        chrome_options = Options()
        chrome_options.binary_location=\
            r"C:\Users\libin.thomas\AppData\Local\Google\Chrome\Application\chrome.exe"
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(executable_path=
                                       r"D:/OneDrive - CACTUS/Python/Sel_python/drivers/chromedriver v86/chromedriver.exe",
                                       options=chrome_options)

        # terminate script
        yield
        self.driver.close()
        self.driver.quit()
        print("Test completed")

    @allure.title("Verify all cookies condition")
    def testcase_01(self, test_setup):
        self.driver.get("https://lifesciences.cactusglobal.com/")
        title = self.driver.title
        print("Page title: "+title)
        time.sleep(3)

        self.driver.find_element_by_xpath("//a[contains(text(),'here')]").click()
        self.driver.find_element_by_xpath("//a[contains(text(), 'Allow all')]").click()
        time.sleep(3)

        #Store cookies in dictionary
        all_cookies=self.driver.get_cookies()
        cookies_dict={}
        for cookie in all_cookies:
            cookies_dict[cookie['name']] = cookie['value']
        # print(cookies_dict)

        # fetch consent value
        consent_value = str
        if 'consent' in cookies_dict.keys():
            consent_value = cookies_dict['consent']


        # convert base64 to string
        acptd_conditions = base64.b64decode(consent_value).decode('utf-8')
        print(acptd_conditions)

        #verifying tracking code presence
        GA_code='_ga'
        if GA_code in cookies_dict.keys():
            print("GA cookie accepted with name= " + GA_code)

        else:
            print("Unable to fetch cookie details")
            raise AssertionError

        Bigint_code = '__ivc'
        if Bigint_code in cookies_dict.keys():
            print("Bigint cookie present with name= " + Bigint_code)

        else:
            print("BigInt script not fired")

        Gtag_code='_ga_MNGCCS5STP'
        if Gtag_code in cookies_dict.keys():
            print("Gtag cookie present with name= " + Gtag_code)

        else:
            print("Gtag script not fired")



    @allure.title("Verify functional cookies")
    def testcase_02(self, test_setup):
        self.driver.get("https://lifesciences.cactusglobal.com/")
        title = self.driver.title
        print("Page title: " + title)
        time.sleep(3)

        self.driver.find_element_by_xpath("//a[contains(text(),'here')]").click()
        self.driver.find_element_by_xpath("//label[@for='functional-switch']").click()
        self.driver.find_element_by_xpath("//a[@class='secondary-cta']").click()
        time.sleep(3)

        # Store cookies in dictionary
        all_cookies=self.driver.get_cookies()
        cookies_dict={}
        for cookie in all_cookies:
            cookies_dict[cookie['name']]=cookie['value']

        #fetch consent value
        consent_value=str
        if 'consent' in cookies_dict.keys():
            consent_value=cookies_dict['consent']

        #convert base64 to string
        acptd_conditions=base64.b64decode(consent_value).decode('utf-8')
        print(acptd_conditions)

        # verifying tracking code presence
        GA_code = '_ga'
        if GA_code in cookies_dict.keys():
            print("GA cookie accepted with name= " + GA_code)

        else:
            print("GA script not fired")
            # raise AssertionError

        Bigint_code = '__ivc'
        if Bigint_code in cookies_dict.keys():
            print("Bigint cookie present with name= " + Bigint_code)

        else:
            print("BigInt script not fired")

        Gtag_code = '_ga_MNGCCS5STP'
        if Gtag_code in cookies_dict.keys():
            print("Gtag cookie present with name= " + Gtag_code)

        else:
            print("Gtag script not fired")


    @allure.title("Verify functional & performance cookies")
    def testcase_03(self, test_setup):
        self.driver.get("https://lifesciences.cactusglobal.com/")
        title = self.driver.title
        print("Page title: " + title)
        time.sleep(3)

        self.driver.find_element_by_xpath("//a[contains(text(),'here')]").click()
        self.driver.find_element_by_xpath("//label[@for='functional-switch']").click()
        self.driver.find_element_by_xpath("//label[@for='performance-switch']").click()
        self.driver.find_element_by_xpath("//a[@class='secondary-cta']").click()
        time.sleep(3)

        # Store cookies in dictionary
        all_cookies = self.driver.get_cookies()
        cookies_dict = {}
        for cookie in all_cookies:
            cookies_dict[cookie['name']]=cookie['value']

        # fetch consent value
        consent_value = str
        if 'consent' in cookies_dict.keys():
            consent_value = cookies_dict['consent']

        # convert base64 to string
        acptd_conditions = base64.b64decode(consent_value).decode('utf-8')
        print(acptd_conditions)

        # verifying tracking code presence
        GA_code = '_ga'
        if GA_code in cookies_dict.keys():
            print("GA cookie accepted with name= " + GA_code)

        else:
            print("GA script not fired")
            # raise AssertionError

        Bigint_code = '__ivc'
        if Bigint_code in cookies_dict.keys():
            print("Bigint cookie present with name= " + Bigint_code)

        else:
            print("BigInt script not fired")

        Gtag_code = '_ga_MNGCCS5STP'
        if Gtag_code in cookies_dict.keys():
            print("Gtag cookie present with name= " + Gtag_code)

        else:
            print("Gtag script not fired")

