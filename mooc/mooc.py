from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class MOOCSpider:
    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.chrome = webdriver.Chrome(options=chrome_options)
        self.chrome.maximize_window()

    def spider(self):
        try:
            time.sleep(5)
            print(self.chrome.current_url)
            mdiv = self.chrome.find_element_by_id('j-courseCardListBox')
            divs = mdiv.find_elements_by_xpath(".//div[@data-action='课程点击']")
            for div in divs:
                course = div.find_element_by_xpath(".//span[@class=' u-course-name f-thide']").text
                d = div.find_element_by_xpath(".//div[@class='t2 f-fc3 f-nowrp f-f0']")
                links = d.find_elements_by_xpath(".//a")
                college = links[0].text
                if len(links) >= 2:
                    teacher = links[1].text
                else:
                    teacher = ""
                team = teacher
                try:
                    team += d.find_elements_by_xpath(".//span").text
                except:
                    pass
                count = div.find_element_by_xpath(".//span[@class='hot']").text
                process = div.find_element_by_xpath(".//span[@class='txt']").text
                brief = div.find_element_by_xpath(".//span[@class='p5 brief f-ib f-f0 f-cb']").text
                print(course, college, count, process, brief)
            link = self.chrome.find_element_by_xpath("//ul[@class='ux-pager']//li[@class='ux-pager_btn ux-pager_btn__next']//a")
            if link.get_attribute("class") == "th-bk-main-gh":
                print(link.text)
                link.click()
                self.spider()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    s = MOOCSpider()
    key = 'python'
    url = "https://www.icourse163.org/search.htm?search=" + key + '#'
    try:
        s.chrome.get(url)
        s.spider()
    except Exception as e:
        print(e)
