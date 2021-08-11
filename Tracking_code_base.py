from seleniumwire import webdriver
import pytest
from selenium.webdriver.chrome.options import Options
import time
import allure
from webdriver_manager.chrome import ChromeDriverManager


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
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
        # self.driver=webdriver.Remote(command_executor="http://localhost:4444/wd/hub", options=chrome_options)

        # terminate script
        yield
        self.driver.close()
        self.driver.quit()
        print("Test completed")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Verify BigInt script in page")
    def testcase_01(self, test_setup):
        self.driver.get("https://lifesciences.cactusglobal.com/")
        title = self.driver.title
        print("Page title: "+title)
        time.sleep(3)

        # Presence of GTM in the code
        scripts=self.driver.find_elements_by_tag_name('script')
        for script in scripts:
            # print(script.get_attribute('src'))
            if 'cf.cactusglobal.io/assets/client-track.js' in script.get_attribute('src'):
                print("The BigInt Script present in the page: "+script.get_attribute('src'))
        # print('*'*20)


        #Capturing network requests
        for request in self.driver.requests:
            if request.response:
                print(
                    request.url,
                    request.response.status_code,
                    request.response.headers['Content-Type'],
                    request.response.headers['set-cookie']
                )
            if "api.cactusglobal.io/v1/initialize" in request.url and request.response.status_code==200:
                bigint_url=request.url
                print("BigInt request url: "+bigint_url)

                # print(bigint_url,
                #       request.response.status_code,
                #       request.response.headers['content-type'])
                cookie=request.response.headers['set-cookie']
                print("Bigint script executed with status code: "+str(request.response.status_code))
                # print("The cookie generated is: "+cookie)

                split_cookie_data=cookie.split('=')

                cookie_name=split_cookie_data[0]
                print("Bigint generated cookie name: "+cookie_name)

                domain_data=split_cookie_data[1]
                domain_data=domain_data.split(';')
                cookie_value=domain_data[0]
                print("Cookie value: "+cookie_value)

                # validity=split_cookie_data[3]
                # validity=validity.split(';')
                # cookie_expiry=validity[0]
                # print("Cookie expiry: "+cookie_expiry)

            elif "api.cactusglobal.io/v1/initialize" in request.url and request.response.status_code!=200:
                print("Client track js responded back with an "+request.response.status_code+
                      " code. Please retry and/or check network requests")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify tag manager script in page")
    def testcase_02(self,test_setup):
        self.driver.get("https://lifesciences.cactusglobal.com/")
        title=self.driver.title
        print("Page title: "+title)

        #Presence of GTM in the code
        scripts = self.driver.find_elements_by_tag_name('script')
        for script in scripts:
            # print(script.get_attribute('src'))
            if 'www.googletagmanager.com/gtag/js' in script.get_attribute():
                print("The GTM Script present in the page: "+ script.get_attribute('src'))


        # Capturing network requests
        for request in self.driver.requests:
                if "www.googletagmanager.com/gtag/js" in request.url and request.response.status_code == 200:
                    # print(request.url,
                    #       request.response.status_code,
                    #       request.response.headers['content-type'])
                    gtag_url = request.url
                    print("Gtag request url: " + gtag_url)
                    print("Gtag script executed with status code: "+str(request.response.status_code))
                # cookie = request.response.headers['set-cookie']
                # print("The cookie generated is: " + cookie)


    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify BigInt cookie in storage")
    def testcase_03(self, test_setup, key='__ivc'):
        # __ivc,_ga_MNGCCS5STP,_ga
        self.driver.get("https://lifesciences.cactusglobal.com/")
        title = self.driver.title
        print("Page title: " + title)
        time.sleep(3)
        all_cookies=self.driver.get_cookies()


        cookies_dict = {}
        for cookie in all_cookies:
            cookies_dict[cookie['name']] = cookie['expiry']

        if key in cookies_dict.keys():
            print("Bigint cookie present with name= " + key)
            cookie_expiry=cookies_dict.get(key)
            expiry_date = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(cookie_expiry))
            print("Cookie expiry date: " + str(expiry_date))
            # print(cookie_expiry)
            # print(time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(cookie_expiry)))

    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Verify GA cookie in storage")
    def testcase_04(self, test_setup, key='_ga'):
        # __ivc,_ga_MNGCCS5STP,_ga
        self.driver.get("https://lifesciences.cactusglobal.com/")
        title = self.driver.title
        print("Page title: " + title)
        time.sleep(3)
        all_cookies = self.driver.get_cookies()

        cookies_dict = {}
        for cookie in all_cookies:
            cookies_dict[cookie['name']] = cookie['expiry']

        if key in cookies_dict.keys():
            print("Bigint cookie present with name= " + key)
            cookie_expiry = cookies_dict.get(key)
            # print(cookie_expiry)
            expiry_date=time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(cookie_expiry))
            print("Cookie expiry date: "+str(expiry_date))

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify Gtag cookie in storage")
    def testcase_05(self, test_setup, key='_ga_MNGCCS5STP'):
        # __ivc,_ga_MNGCCS5STP,_ga
        self.driver.get("https://lifesciences.cactusglobal.com/")
        title = self.driver.title
        print("Page title: " + title)
        time.sleep(3)
        all_cookies = self.driver.get_cookies()

        cookies_dict = {}
        for cookie in all_cookies:
            cookies_dict[cookie['name']] = cookie['expiry']

        if key in cookies_dict.keys():
            print("Bigint cookie present with name= " + key)
            cookie_expiry = cookies_dict.get(key)
            # print(cookie_expiry)
            # print(time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(cookie_expiry)))
            expiry_date = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(cookie_expiry))
            print("Cookie expiry date: " + str(expiry_date))









