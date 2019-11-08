import scrapy
from scrapy.selector import Selector
from crawler.items import DispensaryItem
import pandas as pd


class CrawlerDispensaries(scrapy.Spider):
    name = "crawler_dispensaries"
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    allowed_domains = ["weedmaps.com"]
    _urls = "https://weedmaps.com"

    handle_httpstatus_list = [403]

    def process_request(self, url, callback, data):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        if callback:
            return scrapy.Request(url=url, callback=callback, cb_kwargs={'data': data}, headers=headers)
        return scrapy.Request(url=url, headers=headers)

    def get_text_from_string_tags(self, text):
        return text.split('>')[1].split('<')[0]

    def start_requests(self):
        urls = []
        list_data = []
        df = pd.DataFrame(pd.read_csv('first_dispensaries.csv', usecols=['ListingUrl', 'Listings',
                                                                         'ChildListingUrl', 'ChildListings', 'State']))

        for index, rows in df.iterrows():
            print(rows.values[2])
            list_data.append(rows.values)

        print("Leng list_data: " + str(len(list_data)))
        for data in list_data:
            print("data: " + str(data))
            url = data[0]
            if len(data[2]) > 0 and data[2] != 'nan':
                url = data[2]
            print("url: " + str(url))
            yield self.process_request(url=url, callback=self.parse, data=data)

    def parse(self, response, data):
        dispensaries = Selector(response).xpath('//*[@class="src__Box-sc-1sbtrzs-0 src__Flex-sc-1sbtrzs-1 styled-components__LinkWrap-sc-8si1dn-1 bNbtAW"]')
        for dispensary in dispensaries:
            item = DispensaryItem()
            store_url = self._urls + dispensary.css('a::attr(href)').extract_first()
            print("store_url: " + str(store_url))
            item['StoreUrl'] = store_url
            item['State'] = data[4]
            item['ListingUrl'] = data[2]
            item['Listings'] = data[3]
            item['ChildListingUrl'] = data[0]
            item['ChildListings'] = data[1]
            yield item