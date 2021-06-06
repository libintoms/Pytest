from selenium import webdriver
import pytest
import time
import pandas as pd
from openpyxl import load_workbook
from selenium.webdriver.chrome.options import Options
from prettytable import PrettyTable

class Test_main():

    @pytest.fixture()
    def test_setup(self):
        #initiating chrome driver
        global driver
        chrome_options=Options()
        chrome_options.add_argument('--start-maximized')
        driver = webdriver.Chrome(executable_path=
                                  r"D:/OneDrive - CACTUS/Python/Sel_python/drivers/chromedriver v86/chromedriver.exe",
                                  chrome_options=chrome_options)
        time.sleep(3)

        #initiating file reader
        file= r'D:\OneDrive - CACTUS\Python\Sel_python\Pytest\Data files\SEO_Data.xlsx'
        global df, urls, title, desc, key
        df=pd.read_excel(file, sheet_name='Data_01')
        urls=df['Address']
        title=df['Meta Title']
        desc=df['Meta Description']
        key=df['Meta Keywords']

        #initiating file writer
        global writer
        writer=pd.ExcelWriter(file, engine='openpyxl')
        book=load_workbook(file)
        writer.book=book
        writer.sheets=dict((ws.title, ws)for ws in book.worksheets)

        #terminate script
        yield
        driver.close()
        driver.quit()
        print("Test completed")


    def test_01(self, test_setup):

        #creating variables for data from sheet
        col_count=0
        row_count=1
        error=[]
        output=[]
        list=len(urls)
        print("Total number of urls in the sheet: "+str(list))
        t=PrettyTable(['Urls','Status'])

        for pages in urls:
            #fetching values from sheet
            page_url = urls[col_count]
            exptd_title = title[col_count]
            exptd_desc = desc[col_count]
            exptd_key = key[col_count]

            #opening pages
            driver.get(page_url)
            actual_title=driver.title
            # print("Title is: "+actual_title)

            site_desc = driver.find_elements_by_xpath("//meta[@name='description']|//meta[@name='Description']")
            for elements in site_desc:
                actual_desc = elements.get_attribute("content")
            # print("Desc is: "+actual_desc)

            # site_key=driver.find_elements_by_xpath("//meta[@name='keywords']|//meta[@name='Keywords']")
            # for elements in site_key:
            #     actual_key=elements.get_attribute("content")
            # print("Keyword is: "+actual_key)

            #conditions
            if actual_title == exptd_title:
                title_output = "Correct title"
                output.append(title_output)
            else:
                title_output = "Incorrect title"
                output.append(title_output)
                error.append(title_output)

            if actual_desc==exptd_desc:
                desc_output="Correct description"
                output.append(desc_output)
            else:
                desc_output = "Incorrect description"
                output.append(desc_output)
                error.append(desc_output)
            #
            # if actual_key==exptd_key:
            #     key_output="Correct keywords"
            #     output.append(key_output)
            # else:
            #     key_output = "Incorrect keywords"
            #     output.append(key_output)
            #     error.append(key_output)

            listToStr = '|'.join([str(elem) for elem in output])
            # print(listToStr)

            #writing to file
            df1=pd.DataFrame({'Actual title':[actual_title]})
            df1.to_excel(writer, sheet_name='Data_01', header=None, index=None,startrow=row_count,startcol=2)
            writer.save()

            df2=pd.DataFrame({'Actual Description':[actual_desc]})
            df2.to_excel(writer, sheet_name='Data_01', header=None, index=None,startrow=row_count,startcol=4 )
            writer.save()
            #
            # df3=pd.DataFrame({'Actual Keyword':[actual_key]})
            # df3.to_excel(writer, sheet_name='Data_01', header=None, index=None,startrow=row_count,startcol=6 )
            # writer.save()

            df4=pd.DataFrame({'Status':[listToStr]})
            df4.to_excel(writer, sheet_name='Data_01', header=None, index=None,startrow=row_count,startcol=7)
            writer.save()

            t.add_row([page_url, listToStr])

            #updating values
            output.clear()
            col_count+=1
            row_count+=1

        print(t)

        if error:
            raise Exception("There are errors in the list")








