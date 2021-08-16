from seleniumwire import webdriver
import pytest
from selenium.webdriver.chrome.options import Options
import time
import allure
import pandas as pd
from openpyxl import load_workbook


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

        # initiating file reader
        file = r'D:\OneDrive - CACTUS\Python\Sel_python\Pytest\Data files\Tracking_codes_Data.xlsx'
        global df, Urls, Gtag_cookie_id, GA_cookie_id, BigInt_cookie_id

        df = pd.read_excel(file, sheet_name='Data_01')
        Urls = df['URL']
        Gtag_cookie_id = df['GTAG ID']
        GA_cookie_id = df['GA ID']
        BigInt_cookie_id = df['BigInt ID']

        # initiating file writer
        global writer
        writer = pd.ExcelWriter(file, engine='openpyxl')
        book = load_workbook(file)
        writer.book = book
        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

        # terminate script
        yield
        self.driver.close()
        self.driver.quit()
        print("Test completed")

    @allure.title("Verify Gtag script")
    def testcase_01(self, test_setup):
        col_count=0

        for webpages in Urls:
            self.driver.get(Urls[col_count])
            title = self.driver.title
            print("Page title: " + title)
            time.sleep(3)

            self.driver.find_element_by_xpath("//a[contains(text(),'here')]").click()
            self.driver.find_element_by_xpath("//a[contains(text(), 'Allow all')]").click()
            time.sleep(5)

            Gtag_id=Gtag_cookie_id[col_count]

            # Store cookies in dictionary
            all_cookies = self.driver.get_cookies()
            cookies_dict = {}
            for cookie in all_cookies:
                cookies_dict[cookie['name']] = cookie['expiry']

            if Gtag_id in cookies_dict.keys():
                print("Gtag cookie present with name= " + str(Gtag_id))
                df1=pd.DataFrame({'Gtag code verified':["Yes"]})
                df1.to_excel(writer, sheet_name='Data_01',index=None, header=None,startcol=4,startrow=col_count+1)
                writer.save()

                cookie_expiry=cookies_dict.get(Gtag_id)
                expiry_date = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(cookie_expiry))
                print("Cookie expiry date: " + str(expiry_date))
                df2=pd.DataFrame({'Gtag code expiry':[expiry_date]})
                df2.to_excel(writer, sheet_name='Data_01', index=None, header=None, startcol=5, startrow=col_count+1)
                writer.save()

            else:
                print("Google tag manager script not fired")
                raise AssertionError

            col_count+=1

    @allure.title("Verify GA script")
    def testcase_02(self, test_setup):
        col_count=0

        for webpages in Urls:
            self.driver.get(Urls[0])
            title = self.driver.title
            print("Page title: " + title)
            time.sleep(3)

            self.driver.find_element_by_xpath("//a[contains(text(),'here')]").click()
            self.driver.find_element_by_xpath("//a[contains(text(), 'Allow all')]").click()
            time.sleep(5)

            GA_cookie = GA_cookie_id[col_count]

            # Store cookies in dictionary
            all_cookies = self.driver.get_cookies()
            cookies_dict = {}
            for cookie in all_cookies:
                cookies_dict[cookie['name']] = cookie['expiry']

            if GA_cookie in cookies_dict.keys():
                print("GA cookie present with name= " + GA_cookie)
                df3 = pd.DataFrame({'GA code verified': ["Yes"]})
                df3.to_excel(writer, sheet_name='Data_01', index=None, header=None, startcol=6, startrow=col_count + 1)
                writer.save()

                cookie_expiry = cookies_dict.get(GA_cookie)
                expiry_date = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(cookie_expiry))
                print("Cookie expiry date: " + str(expiry_date))
                df4 = pd.DataFrame({'GA code expiry': [expiry_date]})
                df4.to_excel(writer, sheet_name='Data_01', index=None, header=None, startcol=7, startrow=col_count + 1)
                writer.save()

            else:
                print("Google analytics script not fired")
                df5 = pd.DataFrame({'GA code verified': ["Google analytics script not fired"]})
                df5.to_excel(writer, sheet_name='Data_01', index=None, header=None, startcol=6, startrow=col_count + 1)
                writer.save()


            col_count+=1

    @allure.title("Verify BigInt script")
    def testcase_03(self, test_setup):
        col_count=0

        for webpages in Urls:
            self.driver.get(Urls[0])
            title = self.driver.title
            print("Page title: " + title)
            time.sleep(3)

            self.driver.find_element_by_xpath("//a[contains(text(),'here')]").click()
            self.driver.find_element_by_xpath("//a[contains(text(), 'Allow all')]").click()
            time.sleep(5)

            BigInt_cookie = BigInt_cookie_id[col_count]

            # Store cookies in dictionary
            all_cookies = self.driver.get_cookies()
            cookies_dict = {}
            for cookie in all_cookies:
                cookies_dict[cookie['name']] = cookie['expiry']

            if BigInt_cookie in cookies_dict.keys():
                print("Bigint cookie present with name= " + BigInt_cookie)
                df6 = pd.DataFrame({'BigInt code verified': ["Yes"]})
                df6.to_excel(writer, sheet_name='Data_01', index=None, header=None, startcol=8, startrow=col_count + 1)
                writer.save()

                cookie_expiry = cookies_dict.get(BigInt_cookie)
                expiry_date = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(cookie_expiry))
                print("Cookie expiry date: " + str(expiry_date))
                df7 = pd.DataFrame({'BigInt code expiry': [cookie_expiry]})
                df7.to_excel(writer, sheet_name='Data_01', index=None, header=None, startcol=9, startrow=col_count + 1)
                writer.save()

            else:
                print("BigInt script not fired")
                df8 = pd.DataFrame({'BigInt code verified': ["BigInt script not fired"]})
                df8.to_excel(writer, sheet_name='Data_01', index=None, header=None, startcol=8, startrow=col_count + 1)
                writer.save()
                # raise AssertionError

            col_count += 1





