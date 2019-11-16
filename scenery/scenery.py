import urllib.request
from bs4 import BeautifulSoup


class MySpider:
    def spider(self, url):
        try:
            res = urllib.request.urlopen(url)
            html = res.read().decode()
            soup = BeautifulSoup(html, 'lxml')
            divs = soup.find("div", attrs={'class': 'sightlist'}).find_all("div", attrs={'class': 'sightshow'})
            for div in divs:
                dd = div.find("div", attrs={'class': 'sightdetail'})
                sName = dd.find("h4").find('a').text
                lis = dd.find('ul', attrs={'class': 'sightbase'}).find_all('li')
                sType = []
                if len(lis):
                    for link in lis[0].find_all('a'):
                        sType.append(link.text)
                sSource = []
                if len(lis) > 1:
                    for link in lis[1].find_all('a'):
                        sSource.append(link.text)
                if len(lis) > 2:
                    sLevel = lis[2].find('span').find('a').text
                    sTime = lis[2].find('a', recursive=False).text
                else:
                    sLevel = ''
                    sTime = ''
                lis = dd.find('ul', attrs={'class': 'sighthotel'}).find_all('li')
                sHotel = []
                for li in lis:
                    h = {}
                    h['name'] = li.find('a').text
                    h['price'] = li.find('span').text
                    sHotel.append(h)
                print(sName, sType, sSource, sLevel, sTime, sHotel)
        except Exception as e:
            print(e)

    def getPageCount(self):
        count = 0
        try:
            resp = urllib.request.urlopen("http://scenic.cthy.com/scenicSearch/0-0-201-0-0-1.html")
            html = resp.read().decode()
            soup = BeautifulSoup(html, "lxml")
            count = int(soup.find("ul", attrs={"id": "PagerList"}).find("li").find_all("span")[1].text)
        except Exception as err:
            print(err)
        return count


if __name__ == '__main__':
    s = MySpider()
    count = s.getPageCount()
    print("Total ", count, " pages")
    for p in range(1, count + 1):
        url = "http://scenic.cthy.com/scenicSearch/0-0-201-0-0-" + str(p) + ".html"
        print("Page ", p, " ", url)
        s.spider(url)
