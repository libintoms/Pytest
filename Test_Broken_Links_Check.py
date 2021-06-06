from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest
import pandas as pd
import requests
from requests.exceptions import MissingSchema, InvalidSchema
from openpyxl import load_workbook
import time

class Test_broken_links:

    @pytest.fixture()
    def test_setup(self):
        #intiating browser instance
        chrome_options=Options()
        chrome_options.add_argument('--start-maximized')
        global driver
        driver=webdriver.Chrome(
            executable_path=r"D:/OneDrive - CACTUS/Python/Sel_python/drivers/chromedriver v86/chromedriver.exe", chrome_options=chrome_options
        )

        #initiating file reader
        file=r"D:/OneDrive - CACTUS/Python/Sel_python/Pytest/Data files/Broken_links_Data.xlsx"
        global df, Url
        df=pd.read_excel(file,sheet_name='Data_01')
        Url=df['URL']

        #initiating file writer
        global writer
        writer=pd.ExcelWriter(file,engine='openpyxl')
        book=load_workbook(file)
        writer.book=book
        writer.sheets=dict((ws.title, ws)for ws in book.worksheets)

        #closing driver instance
        yield
        driver.close()
        driver.quit()
        print("Test Completed")

    def test_dead_link_check(self, test_setup):
        page=Url[0]

        driver.get(page)
        print(page)

        brkn_link_count=0
        valid_link_count=0
        bad_request_count=0
        req_unaccepted_count=0
        server_error_count=0
        gateway_timeout_count=0
        row_count_a = 1
        row_count_b = 1
        row_count_c = 1
        row_count_d = 1
        row_count_e = 1

        list_links=driver.find_elements_by_xpath("//a")
        count=len(list_links)
        print("Total links in the page are: "+str(count))
        df=pd.DataFrame({'Total links':[count]})
        df.to_excel(writer,sheet_name='Data_01',header=None, index=None, startcol=1, startrow=row_count_a)
        writer.save()

        for link in list_links:
            try:
                request = requests.head(link.get_attribute('href'), data={'key': 'value'})
                print("Status of " + link.get_attribute('href') + " is: " + str(request.status_code))
                if (request.status_code == 404):
                    brkn_link_count += 1
                    broken_link=link.get_attribute("href")
                    df1=pd.DataFrame({'Dead links':[broken_link]})
                    df1.to_excel(writer, sheet_name='Data_01', header=None, index=None, startcol=2, startrow=row_count_a)
                    writer.save()
                    print(link.get_attribute('href'))
                    row_count_a += 1

                elif (request.status_code == 400):
                    bad_request_count += 1
                    bad_request=link.get_attribute("href")
                    df2 = pd.DataFrame({'Bad Requests': [bad_request]})
                    df2.to_excel(writer, sheet_name='Data_01', header=None, index=None, startcol=3, startrow=row_count_b)
                    writer.save()
                    print(link.get_attribute('href'))
                    row_count_b += 1

                elif (request.status_code == 406):
                    req_unaccepted_count += 1
                    unaccepted_requests=link.get_attribute("href")
                    df3 = pd.DataFrame({'Unaccepted Requests': [unaccepted_requests]})
                    df3.to_excel(writer, sheet_name='Data_01', header=None, index=None, startcol=4, startrow=row_count_c)
                    writer.save()
                    print(link.get_attribute('href'))
                    row_count_c += 1
                # 500 error and 504 error

                elif (request.status_code == 500):
                    server_error_count += 1
                    server_error=link.get_attribute("href")
                    df3 = pd.DataFrame({'Internal Server Error': [server_error]})
                    df3.to_excel(writer, sheet_name='Data_01', header=None, index=None, startcol=5, startrow=row_count_d)
                    writer.save()
                    print(link.get_attribute('href'))
                    row_count_d += 1

                elif (request.status_code == 504):
                    gateway_timeout_count += 1
                    gateway_timeout = link.get_attribute("href")
                    df3 = pd.DataFrame({'Gateway Timeout': [gateway_timeout]})
                    df3.to_excel(writer, sheet_name='Data_01', header=None, index=None, startcol=6,
                                 startrow=row_count_e)
                    writer.save()
                    print(link.get_attribute('href'))
                    row_count_e += 1

                else:
                    valid_link_count += 1

            except requests.exceptions.MissingSchema:
                print("Encountered MissingSchema Exception")

            except requests.exceptions.InvalidSchema:
                print("Encountered InvalidSchema Exception")

            except:
                print("Encountered some other execption")

        print("Detection of broken links completed with " + str(brkn_link_count) + " broken links and " + str(bad_request_count)
              + " bad requests and " + str(req_unaccepted_count) + " Unaccepted requests and " + str(server_error_count) + " Internal server error and " +
              str(gateway_timeout_count) + " Gateway timouts and " + str(valid_link_count) + " valid links")

        # row_count += 1
