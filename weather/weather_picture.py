from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import urllib.request
import threading

start_url = "http://www.weather.com.cn/weather/101020100.shtml"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
count = 0
threads = []

def imageSpider(start_url):
    global threads
    global count
    try:
        urls = []
        req = urllib.request.Request(start_url, headers=headers)
        data = urllib.request.urlopen(req)
        data = data.read()
        dammit = UnicodeDammit(data, ['utf-8', 'gbk'])
        data = dammit.unicode_markup
        soup = BeautifulSoup(data, 'lxml')
        images = soup.select("img")
        for image in images:
            try:
                src = image["src"]
                url = urllib.request.urljoin(start_url, src)
                if url not in urls:
                    print(url)
                    count += 1
                    t = threading.Thread(target=download, args=(url, count))
                    t.setDaemon(False)
                    t.start()
                    threads.append(t)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

def download(url, count):
    try:
        if (url[len(url)-4] == '.'):
            ext = url[len(url)-4:]
        else:
            ext = ""
        req = urllib.request.Request(url, headers=headers)
        data = urllib.request.urlopen(req, timeout=100)
        data = data.read()
        fobj = open("images\\" + str(count) + ext, "wb")
        fobj.write(data)
        fobj.close()
        print("downloaded" + str(count) + ext)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    imageSpider(start_url)
    for t in threads:
        t.join()
    print("end")
