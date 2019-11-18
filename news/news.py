from bs4 import BeautifulSoup
import urllib.request


class MySpider:
    def spider(self, url):
        try:
            print(url)
            res = urllib.request.urlopen(url)
            data = res.read()
            html = data.decode('gbk')
            root = BeautifulSoup(html, 'lxml')
            mdiv = root.find('div', attrs={'class': 'w1000 mt20 column_2 p9_con'})
            mdiv = mdiv.find_all('div', attrs={'class': 'headingNews qiehuan1_c'})[2]
            divs = mdiv.find_all('div', attrs={'class': 'hdNews clearfix'})
            for div in divs:
                title = div.find('h5').find('a').text
                brief = div.find('em').find('a').text
                href = div.find('em').find('a')['href']
                turl = urllib.request.urljoin(url, href)
                text = self.getText(turl)
                print(title, brief, text)
                print()
            links = mdiv.find('div', attrs={'class': 'page_n clearfix'}).find_all('a')
            if len(links):
                if links[-1].text == '下一页':
                    href = links[-1]['href']
                    url = urllib.request.urljoin(url, href)
                    self.spider(url)
        except Exception as e:
            print(e)

    def getText(self, url):
        text = ''
        try:
            res = urllib.request.urlopen(url)
            data = res.read()
            html = data.decode('gbk')
            root = BeautifulSoup(html, 'lxml')
            s = ""
            ps = root.find('div', attrs={'class': 'box_con', 'id': 'rwb_zw'}).find_all('p')
            for p in ps:
                # s += p.text
                s += p.decode_contents(formatter='html')
            text = s
        except Exception as e:
            print(e)
        return text


if __name__ == '__main__':
    url = "http://politics.people.com.cn"
    s = MySpider()
    s.spider(url)
