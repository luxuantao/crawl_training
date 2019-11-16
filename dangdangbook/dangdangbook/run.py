from scrapy import cmdline


cmdline.execute("scrapy crawl book -s LOG_ENABLED=False".split())