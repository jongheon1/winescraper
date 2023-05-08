from scrapy import Spider
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from wineScraper.items import WineItem

import logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)

class WinespiderSpider(Spider):
    name = "winespider"
    allowed_domains = ["www.shinsegae-lnb.com"]
    start_urls = ["https://www.shinsegae-lnb.com/html/product/wine.html"]
    
    def __init__(self):
        self.driver = Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def parse(self, response):
        # start the selenium script
        self.driver.get(response.url)
        
        page_selector = '.pageArea a'
        self.wait = WebDriverWait(self.driver, 10)
        pages = self.driver.find_elements(By.CSS_SELECTOR, page_selector)
        
        while True:
            time.sleep(1)

            for i in range(1, 6):
                pages = self.driver.find_elements(By.CSS_SELECTOR, page_selector)
                pages[i].click()
                
                time.sleep(1)

                css_selector = '.productList a'
                
                wine_pods = self.driver.find_elements(By.CSS_SELECTOR, css_selector)

                for wine_pod in wine_pods:
                    wine_pod.click()

                    wine_item = WineItem()

                    wine_name_ko = self.driver.find_element(By.CSS_SELECTOR, '.productInner h3').text
                    wine_name_en = self.driver.find_element(By.CSS_SELECTOR, '.productInner .nameEng').text

                    wine_img = self.driver.find_element(By.CSS_SELECTOR, '.productInner.img img')
                    wine_img = wine_img.get_attribute('src')

                    wine_details = []
                    details = self.driver.find_elements(By.CSS_SELECTOR, 'table tr')
                    for detail in details:
                        category = detail.find_element(By.CSS_SELECTOR, 'th').text
                        content = detail.find_element(By.CSS_SELECTOR, 'td').text
                        wine_details.append([category, content])

                    wine_dang = self.driver.find_elements(By.CSS_SELECTOR, '.features dd')[0]
                    wine_san = self.driver.find_elements(By.CSS_SELECTOR, '.features dd')[1]
                    wine_body = self.driver.find_elements(By.CSS_SELECTOR, '.features dd')[2]

                    childs = wine_dang.find_elements(By.CSS_SELECTOR, 'span')
                    wine_dang = 0
                    
                    for child in childs:
                        if child.get_attribute('class') == "on":
                            wine_dang = child.text

                    childs = wine_san.find_elements(By.CSS_SELECTOR, 'span')
                    wine_san = 0
                    for child in childs:
                        if child.get_attribute('class') == "on":
                            wine_san = child.text

                    childs = wine_body.find_elements(By.CSS_SELECTOR, 'span')
                    wine_body = 0
                    for child in childs:
                        if child.get_attribute('class') == "on":
                            wine_body = child.text

                    wine_awards = []
                    awards = self.driver.find_elements(By.CSS_SELECTOR, '.awards2 p')
                    for award in awards:
                        wine_awards.append(award.text)

                    wine_info = self.driver.find_element(By.CSS_SELECTOR, '.textDes').text
                    
                    
                    wine_item['name_ko'] = wine_name_ko
                    wine_item['name_en'] = wine_name_en
                    wine_item['img'] = wine_img
                    wine_item['details'] = wine_details
                    wine_item['sugar'] = wine_dang
                    wine_item['acidaty'] = wine_san
                    wine_item['body'] = wine_body
                    wine_item['awards'] = wine_awards
                    wine_item['info'] = wine_info
                    
                    yield wine_item
                    
                    self.driver.back()

            pages = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, page_selector)))
            if pages[6].get_attribute('onclick') == 'return false;' :
                break
            else :
                pages[6].click()

    def closed(self, reason):
        self.driver.quit()