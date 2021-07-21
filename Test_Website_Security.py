from selenium import webdriver
import pytest
from selenium.webdriver.chrome.options import Options
from certifier import CertInfo
import pandas as pd
from openpyxl import load_workbook
import ssl, socket

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

        #initiating file reader
        file=r"D:/OneDrive - CACTUS/Python/Sel_python/Pytest/Data files/SSL_scan_data.xlsx"
        global df, Page_Url
        df = pd.read_excel(file, sheet_name='Data_01')
        Page_Url = df['URL']

        #initializing file writer
        global writer
        writer=pd.ExcelWriter(file,engine='openpyxl')
        writer.book=load_workbook(file)
        writer.sheets=dict((ws.title, ws)for ws in writer.book.worksheets)

        yield
        self.driver.close()
        self.driver.quit()
        print("Test Completed")

    def test_case01(self, test_setup):
        total_url_count=len(Page_Url)
        print("Total urls in the sheet are: "+str(total_url_count))
        row_count=1

        for url in Page_Url:
            print(url)

            hostname = url
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
                s.connect((hostname, 443))
                cert = s.getpeercert()

            subject = dict(x[0] for x in cert['subject'])
            issued_to = subject['commonName']
            print(issued_to)
            df1=pd.DataFrame({'Issued to':[issued_to]})
            df1.to_excel(writer,sheet_name='Data_01', index=False, header=None, startrow=row_count, startcol=1)
            writer.save()

            issuer = dict(x[0] for x in cert['issuer'])
            issued_by = issuer['commonName']
            print(issued_by)
            df2=pd.DataFrame({'Issued by':[issued_by]})
            df2.to_excel(writer, sheet_name='Data_01', index=False, header=None, startrow=row_count, startcol=2)
            writer.save()

            cert = CertInfo(url, 443)
            expiry_date=cert.expire('%b %d %H:%M:%S %Y %Z')
            print(expiry_date)
            df3 = pd.DataFrame({'Expiry': [expiry_date]})
            df3.to_excel(writer, sheet_name='Data_01', index=False, header=None, startrow=row_count, startcol=3)
            writer.save()

            row_count+=1


    def test_case02(self, test_setup):
        row_count=1
        for url in Page_Url:
            webpage="http://"
            webpage+=url
            self.driver.get(webpage)
            page_name=self.driver.current_url
            print(type(page_name))
            print(page_name)
            if (page_name.find('https:')!=-1):
                message="Https secured"
                print(message)
                df4=pd.DataFrame({'Https Status':[message]})
                df4.to_excel(writer, sheet_name='Data_01', index=False, header=None, startrow=row_count, startcol=4)
                writer.save()
            else:
                message = "No https/no auto-redirect to https"
                print(message)
                df5 = pd.DataFrame({'Https Status': [message]})
                df5.to_excel(writer, sheet_name='Data_01', index=False, header=None, startrow=row_count, startcol=4)
                writer.save()
            row_count+=1

















