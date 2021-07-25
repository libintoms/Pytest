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

        #Store cookies in dictionary
        all_cookies=self.driver.get_cookies()
        cookies_dict={}
        for cookie in all_cookies:
            cookies_dict[cookie['name']] = cookie['expiry']

        # fetch consent value
        consent_value = str
        if 'consent' in cookies_dict.keys():
            consent_value = cookies_dict['consent']

        # convert base64 to string
        acptd_conditions = base64.b64decode(consent_value).decode('utf-8')
        print(acptd_conditions)

        GA_code='_ga'
        Bigint_code='__ivc'
        if GA_code in cookies_dict.keys() and Bigint_code in cookies_dict.keys():
            print("GA cookie accepted with name= " + GA_code)
            print("Bigint cookie accepted with name= "+Bigint_code)
        else:
            print("Unable to fetch cookie details")
            raise AssertionError


        for request in self.driver.requests:
            # if request.response:
                # print(
                #     request.url,
                #     request.response.status_code,
                #     request.response.headers['Content-Type'],
                #     request.response.headers['set-cookie']
                # )
            if "https://www.googletagmanager.com/gtag/" in request.url and request.response.status_code==200:
                Gtag_url=request.url
                # print("Gtag js fired with id: "+Gtag_url)
                id=Gtag_url.split('=')
                print("Gtag js fired with id: "+id[1])
            else:
                print("Google tag manager script not fired")
                raise AssertionError

    @allure.title("Verify functional cookies")
    def testcase_02(self,test_setup):
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

