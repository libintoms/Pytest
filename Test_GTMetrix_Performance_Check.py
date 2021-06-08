from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from openpyxl import load_workbook
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import pytest
from Screenshot import Screenshot_Clipping


class Test_GTScan():

    @pytest.fixture()
    def test_setup(self):
        #initiating chrome driver
        chrome_options=Options()
        chrome_options.add_argument('--start-maximized')
        # chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        global driver
        driver=webdriver.Chrome(executable_path=
            r"D:/OneDrive - CACTUS/Python/Sel_python/drivers/chromedriver v86/chromedriver.exe", chrome_options=chrome_options)
        driver.implicitly_wait(5)

        #initiating file reader
        file= r'D:/OneDrive - CACTUS/Python/Sel_python/Pytest/Data files/Performance_Scan_Data.xlsx'
        global df, URLs, Server, Creds, Username, Password
        df=pd.read_excel(file,sheet_name='Data_01')
        URLs=df['Urls']
        Server=df['Server']
        Creds=df['Credentials']
        Username=df['Username']
        Password=df['Password']

        #initiating file writer
        global writer
        writer=pd.ExcelWriter(file, engine='openpyxl')
        book=load_workbook(file)
        writer.book=book
        writer.sheets=dict((ws.title,ws)for ws in book.worksheets)

        yield
        driver.close()
        driver.quit()
        print("Test completed")


    def test01_scanpage(self, test_setup):
        #reading from urls column
        col_count=0
        row_count=1

        url_list = len(URLs)
        print("Total urls in the sheet:" + str(url_list))

        # GTmetrix login
        driver.get("https://gtmetrix.com/")
        driver.find_element_by_xpath("//a[@class='js-auth-widget-link'][contains(text(),'Log In')]").click()
        driver.find_element_by_name("email").send_keys("libin.thomas@cactusglobal.com")
        driver.find_element_by_name("password").send_keys("L!b!n20O4")
        # driver.find_element_by_name("email").send_keys("anupam@getdefault.in")
        # driver.find_element_by_name("password").send_keys("Default@123")
        driver.find_element_by_xpath("//button[contains(text(),'Log In')]").click()
        wait = WebDriverWait(driver, 500)
        wait.until(EC.presence_of_element_located((By.XPATH, "//h1[@class='page-heading']")))
        driver.implicitly_wait(10)


        while col_count<url_list:
            driver.find_element_by_xpath("//div[@class='header-content clear']//i[@class='sprite-gtmetrix sprite-display-block']").click()

            # Passing urls
            page_url = URLs[col_count]
            driver.find_element_by_name("url").send_keys(page_url)
            print("="*15)
            print("Selected webpage: "+page_url)
            #print a table for output

            # Server selection
            country = Server[col_count]
            print("Server location: "+country)
            if country == 'India':
                cn_value = '5'
            elif country == 'China':
                cn_value = '7'
            elif country == 'UK':
                cn_value = '2'
            elif country == 'Canada':
                cn_value = '1'
            elif country == 'USA':
                cn_value = '4'
            # print("Value"+cn_value)

            #Staging site check
            Credentials= Creds[col_count]
            print("Test server: "+Credentials)

            #fecthing credentials
            User=Username[col_count]
            Pswd=Password[col_count]

            #Conditions
            driver.find_element_by_xpath("//a[@class='btn analyze-form-options-trigger']").click()
            #select country
            select_server=Select(driver.find_element_by_id("af-region"))
            select_server.select_by_value(cn_value)

            #entering credentials
            if Credentials == 'Yes':
                driver.find_element_by_xpath("//a[@id='analyze-form-advanced-options-trigger']").click()
                user_field=driver.find_element_by_xpath("//input[@id='af-username']")
                user_field.click()
                user_field.send_keys(User)
                pswd_field=driver.find_element_by_xpath("//input[@id='af-password']")
                pswd_field.click()
                pswd_field.send_keys(Pswd)

            #Submit
            driver.find_element_by_xpath("//button[contains(text(),'Analyze')]").click()
            wait.until(EC.presence_of_element_located((By.XPATH,"//h1[contains(text(),'Latest Performance Report for:')]")))

            # # Saving screenshot
            # correction=page_url.replace("/","")
            # ss_name=correction.replace(":","")
            # # print(correction)
            # # print(ss_name)
            # driver.implicitly_wait(10)
            # ob=Screenshot_Clipping.Screenshot()
            # img_url=ob.full_Screenshot(
            #     driver,save_path=r'D:/OneDrive - CACTUS/Python/Sel_python/Pytest/Screenshots/GTmetrix',image_name="{}.png".format(ss_name))
            # print(img_url)
            # # driver.save_screenshot('D:/OneDrive - CACTUS/Python/Sel_python/Pytest/Screenshots/GTmetrix/{}.png'.format(ss_name))
            # time.sleep(5)

            #Recording page performance
            pageperf=driver.find_element_by_xpath(
                "(//span[@class='report-score-percent'])[1]").text
            print("Page performance is: "+pageperf)
            df1=pd.DataFrame({'Page performance':[pageperf]})
            df1.to_excel(writer, sheet_name='Data_01',index=False, header=None, startcol=5, startrow=row_count)
            writer.save()

            #Recording page grade
            page_grade = driver.find_element_by_xpath(
                "//i[contains(@class ,'sprite-grade-')]").get_attribute('class')
            Grade=page_grade.lstrip('sprite-grade-')
            print("Page speed grade is: " + Grade)
            df2 = pd.DataFrame({'Page grade': [Grade]})
            df2.to_excel(writer, sheet_name='Data_01', index=False, header=None, startcol=6, startrow=row_count)
            writer.save()

            # Recording first contentful paint load time
            first_paint_load = driver.find_element_by_xpath(
                "//span[@class='report-filmstrip-label report-filmstrip-timing-first-contentful-paint']").text
            first_content_load = first_paint_load.lstrip('First Contentful Paint: ')
            print("First Contentful Paint: "+first_content_load)
            df5=pd.DataFrame({'First content load time':[first_content_load]})
            df5.to_excel(writer, sheet_name='Data_01', index=False, header=None, startcol=7, startrow=row_count)
            writer.save()

            #Recording load time
            loaded_time=driver.find_element_by_xpath(
                "//div[@class='report-summary-loaded-text']/h4").text
            print("Fully loaded time is:"+loaded_time)
            df3=pd.DataFrame({'Load time':[loaded_time]})
            df3.to_excel(writer, sheet_name='Data_01',index=False, header=None, startcol=8, startrow=row_count)
            writer.save()

            #Recording page size
            page_size=driver.find_element_by_xpath(
                "(//h4[@class='report-summary-chart-title'])[1]").text
            total_page_size=page_size.lstrip('Total Page Size - ')
            print("Total page size is: "+total_page_size)
            df4=pd.DataFrame({'Page size':[total_page_size]})
            df4.to_excel(writer, sheet_name='Data_01', index=False, header=None, startcol=9, startrow=row_count)
            writer.save()

            #Additional data
            page_requests = driver.find_element_by_xpath(
                "(//h4[@class='report-summary-chart-title'])[2]").text
            total_page_requests=page_requests.lstrip('Total Page Requests - ')
            print("The total requests in page: " + total_page_requests)

            #incrementing cell positions
            row_count=row_count+1
            col_count=col_count+1

    # def test02_final_report(self, test_setup):
    #
    #     #GTmetrix login
    #     driver.get("https://gtmetrix.com/")
    #     driver.find_element_by_xpath("//a[@class='js-auth-widget-link'][contains(text(),'Log In')]").click()
    #     driver.find_element_by_name("email").send_keys("libin.thomas@cactusglobal.com")
    #     driver.find_element_by_name("password").send_keys("L!b!n20O4")
    #     driver.find_element_by_xpath("//button[contains(text(),'Log In')]").click()
    #     wait = WebDriverWait(driver, 300)
    #     wait.until(EC.presence_of_element_located((By.XPATH, "//h1[@class='page-heading']")))
    #
    #     driver.find_element_by_xpath(
    #         "//div[@class='header-content clear']//i[@class='sprite-gtmetrix sprite-display-block']").click()

        #Saving screenshot
        # time.sleep(2)
        # ele=driver.find_element_by_xpath("//a[@class='paginate_button next']")
        # actions=ActionChains(driver)
        # actions.move_to_element(ele).perform()
        # time.sleep(2)
        # driver.save_screenshot('D:/OneDrive - CACTUS/Python/Sel_python/Pytest/Screenshots/GTmetrix/Traversed pages.png')

