from selenium import webdriver
import pandas as pd
import time
import pytest
from selenium.webdriver.chrome.options import Options
from openpyxl import load_workbook
import requests
from prettytable import PrettyTable
#trials:
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Test_RDcheck():

    @pytest.fixture()
    def test_setup(self):
        #initiating browser

        chrome_options=Options()
        chrome_options.add_argument('--start-maximized')
        global driver
        driver = webdriver.Chrome(executable_path=
                                  r"D:/OneDrive - CACTUS/Python/Sel_python/drivers/chromedriver v86/chromedriver.exe",
                                  chrome_options=chrome_options)
        driver.implicitly_wait(5)

        #initaiting file reader
        file= r'D:/OneDrive - CACTUS/Python/Sel_python/Pytest/Data files/Website_Redirection_Data.xlsx'
        global df, old_urls, expct_urls, act_urls
        df=pd.read_excel(file, sheet_name='Data_01')
        old_urls=df['Urls']
        expct_urls=df['Expected New Urls']
        act_urls=df['Actual New Urls']

        #initiating file writer
        global writer
        writer=pd.ExcelWriter(file, engine='openpyxl')
        book=load_workbook(file)
        writer.book=book
        writer.sheets=dict((ws.title,ws)for ws in book.worksheets)

        #exit browser
        yield
        driver.close()
        driver.quit()
        print("Test completed")

    def test01_check_urls(self, test_setup):
        __tracebackhide__ = True
        #reading the file
        Total_entries=len(old_urls)
        print("Total entries in the sheet: "+ str(Total_entries))
        col_count=0
        row_count=1

        #intializing variables for output
        url_mismatch=[]
        t = PrettyTable(['Url', 'Expct_url', 'Act_url', 'Status'])

        # opening urls
        for Webpage in old_urls:
            # print (Webpage)
            Old_Page=old_urls[col_count]
            New_page=expct_urls[col_count]
            driver.get(Old_Page)
            # print("The old page url is: "+Page)

            Redr_page=driver.current_url
            # print("The new url is: "+Redr_page)
            # print("New_url from sheet:"+Newpage)

            if Redr_page==New_page:
                result="Correct redirection"

            else:
                result="Incorrect redirection url"
                url_mismatch.append(result)

            #checking status code
            time.sleep(5)
            response=requests.get(Redr_page)
            http_status=response.status_code
            print(http_status)



            #writing to excel file
            df1=pd.DataFrame({'Actual New Urls':[Redr_page]})
            df1.to_excel(writer,sheet_name='Data_01',index=False, header=False, startrow=row_count, startcol=2)
            df2=pd.DataFrame({'Status':[result]})
            df2.to_excel(writer, sheet_name='Data_01', index=False, header=False, startrow=row_count, startcol=3)
            writer.save()

            #adding details in table
            t.add_row([Old_Page, New_page, Redr_page, result])

            #capturing screenshots
            correction = New_page.replace("/", "")
            ss_name = correction.replace(":", "")
            driver.get_screenshot_as_file('D:/OneDrive - CACTUS/Python/Sel_python/Pytest/Screenshots/Redirections/{}.png'.format(ss_name))


            col_count+=1
            row_count+=1
        print(t)

        #for errors in url_mismatch:
        if url_mismatch:
                raise Exception(("There are errors in the list"))



