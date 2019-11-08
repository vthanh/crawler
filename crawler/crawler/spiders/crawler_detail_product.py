import scrapy
from scrapy.selector import Selector
from crawler.items import ProductItem
import pandas as pd
import random
import base64

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


class CrawlerDetailProduct(scrapy.Spider):
    name = "crawler_detail_product"
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    allowed_domains = ["weedmaps.com"]
    _urls = "https://weedmaps.com"
    handle_httpstatus_list = [403]

    def process_request(self, url, callback, data, headers):
        # # Use the following lines if your proxy requires authentication
        # auth_creds = "lavanthanh.1995@gmail.com:Heocon123_1"
        # # setup basic authentication for the proxy
        # access_token = base64.encodestring(auth_creds)
        # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0',
        #            'proxy': 'http://x.botproxy.net:8080',
        #            'Proxy-Authorization': 'Basic ' + access_token}
        # print("headers: " + str(headers))
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        if callback:
            return scrapy.Request(url=url, callback=callback, cb_kwargs={'data': data}, headers=headers)
        return scrapy.Request(url=url, headers=headers)

    def get_text_from_string_tags(self, text):
        return text.split('>')[1].split('<')[0]

    def start_requests(self):
        list_data = []
        df = pd.DataFrame(pd.read_csv('product.csv', usecols=['ProductUrl', 'StoreUrl']))

        for index, rows in df.iterrows():
            list_data.append(rows.values)

        for data in list_data:
            url = data[0]
            user_agent = random.choice(user_agent_list)
            yield self.process_request(url=url, callback=self.parse, data=data, headers={'User-Agent': user_agent})
            # time.sleep(0.5)

    def parse(self, response, data):
        item = ProductItem()
        item['StoreUrl'] = data[1]
        item['ProductName'] = Selector(response).xpath('//*[@class="styled-components__ProductName-sc-1eacj5g-1 jAdqDv"]/text()').get()
        item['ProductType'] = Selector(response).xpath('//*[@class="styled-components__ProductMetadata-sc-1eacj5g-2 gSWiwN"]/text()').get()
        item['Price'] = ''
        for price in Selector(response).xpath('//*[@class="styled-components__Value-ssaqz4-3 cBQDki"]/text()'):
            item['Price'] = str(item['Price']) + ',' + price.get()
        item['ProductUrl'] = data[0]
        yield item