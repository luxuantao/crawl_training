from selenium import webdriver
from selenium.webdriver.chrome .options import Options
import time


class MySpider:
    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.chrome = webdriver.Chrome(options=chrome_options)
        self.chrome.maximize_window()

    def spider(self):
        try:
            time.sleep(2)
            print(self.chrome.current_url)
            lis = self.chrome.find_element_by_id("list_con").find_elements_by_xpath(".//li[@class='job_item clearfix']")
            for li in lis:
                try:
                    company = li.find_element_by_xpath(".//div[@class='comp_name']//a").text
                except:
                    company = ""
                try:
                    address = li.find_element_by_xpath(".//span[@class='address']").text
                except:
                    address = ""
                try:
                    occupation = li.find_element_by_xpath(".//span[@class='name']").text
                except:
                    occupation = ""
                try:
                    salary = li.find_element_by_xpath(".//p[@class='job_salary']").text
                except:
                    salary = ""
                try:
                    require = li.find_element_by_xpath(".//p[@class='job_require']").text
                except:
                    require = ""
                print(company, address, occupation, salary, require)
            try:
                link = self.chrome.find_element_by_xpath("//div[@class='pagesout']//a[@class='next']")
                link.click()
                self.spider()
            except:
                pass
        except Exception as e:
            print(e)


if __name__ == '__main__':
    s = MySpider()
    s.chrome.get("https://sz.58.com/ruanjiangong/?PGTID=0d202408-0000- 4643-ad88-f906f70cbce9&ClickID=1")
    s.spider()
