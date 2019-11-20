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
        self.chrome.maximize_window()
        self.id = 0
        self.threads = []

    def download(self, fn, src):
        try:
            resp = urllib.request.urlopen(src)
            data = resp.read()
            f = open("images\\" + fn, "wb")
            f.write(data)
            f.close()
        except Exception as err:
            print(err)

    def spider(self, url):
        try:
            self.chrome.get(url)
            print(self.chrome.current_url)
            lis = self.chrome.find_elements_by_xpath("//ul[@class='sellListContent']//li[@class='clear LOGCLICKDATA']")
            for li in lis:
                try:
                    title = li.find_element_by_xpath(".//div[@class='title']//a").text
                    address = li.find_element_by_xpath(".//div[@class='address']").text
                    position = li.find_element_by_xpath(".//div[@class='positionInfo']").text
                    tag = li.find_element_by_xpath(".//div[@class='tag']").text
                    totalPrice = li.find_element_by_xpath(".//div[@class='priceInfo']//div[@class='totalPrice']").text
                    unitPrice = li.find_element_by_xpath(".//div[@class='priceInfo']//div[@class='unitPrice']").text
                    print(title, address, position, tag, totalPrice, unitPrice)
                    # 滚动
                    img = li.find_element_by_xpath(".//img[@class='lj-lazy']")
                    self.chrome.execute_script("arguments[0].scrollIntoView()", img)
                    time.sleep(0.1)
                    src = img.get_attribute("src")
                    src = urllib.request.urljoin(self.chrome.current_url, src)
                    self.id += 1
                    id = str(self.id)
                    while len(id) < 6:
                        id = '0' + id
                    p = src.rfind('.')
                    ext = src[p:]

                    t = threading.Thread(target=self.download, args=[id + ext, src])
                    t.start()
                    self.threads.append(t)
                except Exception as e:
                    print(e)
            if self.id >= 200:
                return
            div = self.chrome.find_element_by_xpath("//div[@class='contentBottom clear']//div[@class='page-box fr']")
            while True:
                links = div.find_elements_by_xpath(".//a")
                if len(links):
                    break
                time.sleep(1)
            link = links[-1]
            if link.text == '下一页':
                href = link.get_attribute("href")
                url = urllib.request.urljoin(self.chrome.current_url, href)
                self.spider(url)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    s = MySpider()
    s.spider("https://sz.lianjia.com/ershoufang/")
    for t in s.threads:
        t.join()
