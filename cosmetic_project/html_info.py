import requests
import time
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROMEDRIVER = 'C:/Users/Rang/Desktop/chromedriver.exe'

class Crawl():

    def __init__(self, url):

        self.url = url
        self.html_request = self.get_html()
        self.html_selenium = self.sele_html()

    def get_html(self):

        headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}
        html = None
        
        for i in range(3):

            #proxies = proxy.reqProxy().get_proxies()

            try:
                res = requests.get(self.url, headers = headers, verify = False, timeout = 30)
                time.sleep(random.uniform(2,5))

                html = res.content.decode("utf-8", "replace")
            
            except Exception as ex:
                print(ex, self.url)            
                pass

            except ConnectionRefusedError as ex:
                print(ex)
                pass

            except:
                print("error")
                pass

            if html is not None:
                break    
            
        return html

    def sele_html(self):
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        
        driver = webdriver.Chrome(executable_path= CHROMEDRIVER, options=chrome_options)
        
        #driver.implicitly_wait(600)
        
        driver.get(self.url)
        
        try:
            element = WebDriverWait(driver, 80).until(EC.element_to_be_clickable((By.CLASS_NAME, 'fdb_lst_ul')))
            html = driver.page_source
            return html
        except:
            pass
        finally:
            driver.quit()
        