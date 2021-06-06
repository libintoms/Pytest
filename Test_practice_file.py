from seleniumwire import webdriver
import pytest
from selenium.webdriver.chrome.options import Options
import time
import allure

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

            if "api.cactusglobal.io/v1/initialize" in request.url and request.response.status_code==200:
                bigint_url=request.url
                print("BigInt request url: "+bigint_url)

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


            elif "api.cactusglobal.io/v1/initialize" in request.url and request.response.status_code!=200:
                print("Client track js responded back with an "+request.response.status_code+
                      " code. Please retry and/or check network requests")