import urllib.request
from bs4 import BeautifulSoup
import threading
import bs4
import random
import os


ua_list = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
           "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
           "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
           "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"]


class MySpider:
    def __init__(self):
        self.count = 0
        self.TS = []

    def download(self, ID, src):
        try:
            req = urllib.request.Request(url=src, headers={"User-Agent": random.choice(ua_list)})
            res = urllib.request.urlopen(req)
            data = res.read()
            f = open('download\\'+ID+'.jpg', 'wb')
            f.write(data)
            f.close()
        except Exception as e:
            print(e)

    def splitItems(self, p):
        res = []
        flag = True
        for c in p.children:
            if isinstance(c, bs4.element.NavigableString):
                t = c.string.replace("\n", "").strip()
                if t != "":
                    if flag:
                        pos = t.find("主演:")
                        director = t[:pos].replace("导演:", "")
                        actor = t[pos + 3:]
                        res.append(director.strip())
                        res.append(actor.strip())
                    else:
                        st = t.split("/")
                        for e in st:
                            res.append(e.strip())
                        break
            elif isinstance(c, bs4.element.Tag) and c.name == "br":
                flag = False
        return res

    def spider(self, url):
        try:
            print(url)
            req = urllib.request.Request(url=url, headers={"User-Agent": random.choice(ua_list)})
            res = urllib.request.urlopen(req)
            html = res.read().decode()
            soup = BeautifulSoup(html, 'lxml')
            # 获取所用的<li>
            lis = soup.find("div", attrs={"id": "content"}).find("ol", attrs={"class": "grid_view"}).find_all("li")
            for li in lis:
                # 爬取电影名称
                div = li.find("div", attrs={"class": "info"})
                hd = div.find("div", attrs={"class": "hd"})
                spans = hd.find_all("span", attrs={"class": "title"})
                mTitle = spans[0].text.replace("\n", "").strip() if len(spans) else ""
                mNative = spans[1].text.replace("\n", "").strip() if len(spans) > 1 else ""
                mNickname = hd.find("span", attrs={"class": "other"}).text.replace("\n","").strip()
                sdiv = li.find("div", attrs={"class": "star"})
                mPoint = sdiv.find("span", attrs={"class": "rating_num"}).text.replace("\n","").strip()
                mComment = sdiv.find_all("span")[1].text.replace("\n", "").strip()
                bd = div.find("div", attrs={"class": "bd"})
                p = bd.find("p")
                res = self.splitItems(p)
                mDirectors = res[0] if len(res) else ""
                mActors = res[1] if len(res) > 1 else ""
                mTime = res[2] if len(res) > 2 else ""
                mCountry = res[3] if len(res) > 3 else ""
                mType = res[4] if len(res) > 4 else ""
                print(mTitle, mNative, mNickname, mPoint, mComment, mDirectors, mActors, mTime, mCountry, mType)
                img = li.find("div", attrs={"class": "pic"}).find("img")
                src = urllib.request.urljoin(url, img["src"])
                self.count += 1
                ID = str(self.count)
                while len(ID) < 6:
                    ID = "0" + ID
                T = threading.Thread(target=self.download, args=[ID, src])
                T.setDaemon(False)
                T.start()
                self.TS.append(T)
            # 网页翻页
            div = soup.find("div", attrs={"class": "paginator"})
            link = div.find("span", attrs={"class": "next"}).find("a")
            if link:
                href = link["href"]
            url = urllib.request.urljoin(url, href)
            # 递归调用 spider
            self.spider(url)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    if not os.path.exists("download"):
        os.mkdir("download")
    s = MySpider()
    s.spider("https://movie.douban.com/top250")
    for T in s.TS:
        T.join()
