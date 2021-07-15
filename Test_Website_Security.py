from selenium import webdriver
import pytest
from selenium.webdriver.chrome.options import Options

class Test_main():

    @pytest.fixture()
    def test_setup(self):

        # initiating browser
        chrome_options = Options()
        chrome_options.binary_location = \
            r"C:\Users\libin.thomas\AppData\Local\Google\Chrome\Application\chrome.exe"
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(executable_path=
                                       r"D:/OneDrive - CACTUS/Python/Sel_python/drivers/chromedriver v86/chromedriver.exe",
                                       options=chrome_options)

        yield
        self.driver.close()
        self.driver.quit()
        print("Test Completed")

    @staticmethod
    def test_case01():
        url='lifesciences.cactusglobal.com'
        return url


    def test_case02(self):
        import subprocess
        subprocess.run('python SSL_trial.py')









