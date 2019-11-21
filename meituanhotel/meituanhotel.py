from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import urllib.request
import threading


class MySpider:
    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.chrome = webdriver.Chrome(options=chrome_options)
        # self.chrome.maximize_window()
        self.pageIndex = 0
        self.pageCount = 0
        self.threads = []

    def trimDigits(self, s):
        i = 0
        while i < len(s) and s[i] >= '0' and s[i] <= '9':
            i += 1
        return s[i:]

    def getExt(self, url):
        p = url.rfind(".")
        if p >= 0:
            ext = url[p:]
            p = ext.find("/")
            if p >= 0:
                ext = ext[:p]
        else:
            ext = ""
        return ext

    def download(self, url, fName):
        try:
            resp = urllib.request.urlopen(url)
            data = resp.read()
            f = open(fName, "wb")
            f.write(data)
            f.close()
            print("download " + fName)
        except Exception as err:
            print(err)

    def spider(self):
        try:
            self.pageIndex += 1
            print(self.pageIndex, "/", self.pageCount, "---", self.chrome.current_url)
            articles = self.chrome.find_element_by_id("list-view").find_elements_by_xpath(".//article")
            for article in articles:
                div = article.find_element_by_xpath(".//div[@class='info-wrapper']")
                hotel = div.find_element_by_xpath(".//h3[@class='poi-title-wrapper']//a").text
                hotel = self.trimDigits(hotel)
                address = div.find_element_by_xpath(".//div[@class='poi-address']").text
                address = address.replace('查看地图', '')
                grade = div.find_element_by_xpath(".//div[@class='poi-grade']").text
                src = article.find_element_by_xpath(".//div[@class='picture-wrapper']//img").get_attribute('src')
                src = urllib.request.urljoin(self.chrome.current_url, src)
                ext = self.getExt(src)
                try:
                    print(hotel, address, grade)
                    t = threading.Thread(target=self.download, args=[src, hotel + ext])
                    t.start()
                    self.threads.append(t)
                except Exception as e:
                    print(e)
            if self.pageIndex < self.pageCount:
                try:
                    link = self.chrome.find_element_by_xpath("//div[@class='paginator-wrapper']//ul[@class='paginator']//li[@class=' next']")
                    link.click()
                    time.sleep(1)
                    self.spider()
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    s = MySpider()
    try:
        url = "https://hotel.meituan.com/"
        s.chrome.get(url)
        div = s.chrome.find_element_by_xpath("//div[@class='search-header']")
        city = div.find_element_by_xpath(".//label[@class='city-box']//input")
        city.click()
        city.clear()
        city.send_keys("武汉")
        city.click()
        # 设置入住日期
        s.chrome.execute_script("document.querySelector(\"div[class='search-header'] div[class='dp-container checkin'] input[class='dp-input']\").value='2019-11-12';")
        # 设置退房日期
        s.chrome.execute_script("document.querySelector(\"div[class='search-header'] div[class='dp-container checkout'] input[class='dp-input']\").value='2019-11-16';")
        search = div.find_element_by_xpath(".//input[@class='search-btn']")
        search.click()
        time.sleep(1)
        links = s.chrome.find_elements_by_xpath("//div[@class='paginator-wrapper']//ul[@class='paginator']//li[@class='page-link']")
        link = links[-1]
        s.pageCount = int(link.find_element_by_xpath(".//a").text)
        print("Total ", s.pageCount)
        s.spider()
        for t in s.threads:
            t.join()
    except Exception as err:
        print(err)
