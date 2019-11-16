import re
import urllib.request


class MySpider:
    def match(self, t, s):
        m = re.search(r"<" + t, s)
        if m:
            a = m.start()
            m = re.search(r">", s[a:])
            if m:
                b = a + m.end()
                return {"start": a, "end": b}
        return None

    def spider(self, url):
        try:
            res = urllib.request.urlopen(url)
            data = res.read()
            html = data.decode()
            m = re.search(r'<div id="realRateInfo">', html)
            html = html[m.end():]
            m = re.search(r'</div>', html)
            html = html[:m.start()]
            i = 0
            while True:
                p = self.match("tr", html)
                q = self.match("/tr", html)
                if p and q:
                    i += 1
                    a = p['end']
                    b = q['start']
                    tds = html[a:b]
                    row = []
                    count = 0
                    while True:
                        m = self.match("td", tds)
                        n = self.match("/td", tds)
                        if m and n:
                            u = m['end']
                            v = n['start']
                            count += 1
                            if count <= 8:
                                row.append(tds[u:v].strip())
                            tds = tds[n['end']:]
                        else:
                            break
                    if i >= 2 and len(row) == 8:
                        currency = row[0]
                        TSP = row[3]
                        CSP = row[4]
                        TBP = row[5]
                        CBP = row[6]
                        time = row[7]
                        print(currency, TSP, CSP, TBP, CBP, time)
                    html = html[q['end']:]
                else:
                    break
        except Exception as e:
            print(e)


if __name__ == '__main__':
    s = MySpider()
    s.spider("http://fx.cmbchina.com/hq/")
