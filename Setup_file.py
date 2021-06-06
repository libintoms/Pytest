from selenium import webdriver
import pytest
from selenium.webdriver.chrome.options import Options

class Test_base():

    @pytest.fixture()
    def test_setup(self):
        # initiating browser
        chrome_options=Options()
        chrome_options.add_argument('--start-maximized')
        driver=webdriver.Chrome(executable_path=
                                  r"D:/OneDrive - CACTUS/Python/Sel_python/drivers/chromedriver v86/chromedriver.exe",
                                  chrome_options=chrome_options)

        # terminate script
        yield
        driver.close()
        driver.quit()
        print("Test completed")

    def testcase_01(self,test_setup):
        driver.get("https://www.google.com/")