from selenium import webdriver
import pytest
from selenium.webdriver.chrome.options import Options
from certifier import CertInfo
import pandas as pd
from openpyxl import load_workbook

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
        global url
        url=Page_Url[1]
        print(url)

        # url='www.impact.science'
        # return url


    def test_case02(self):
        import ssl, socket

        hostname = url
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.connect((hostname, 443))
            cert = s.getpeercert()

        subject = dict(x[0] for x in cert['subject'])
        issued_to = subject['commonName']
        print(issued_to)
        issuer = dict(x[0] for x in cert['issuer'])
        issued_by = issuer['commonName']
        print(issued_by)

        cert = CertInfo(url, 443)
        # print(cert)
        # cert.ca_certs()
        # print(cert.ca_certs())
        print(cert.expire('%b %d %H:%M:%S %Y %Z'))















