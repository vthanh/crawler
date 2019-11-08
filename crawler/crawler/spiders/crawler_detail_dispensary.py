import scrapy
from scrapy.selector import Selector
from crawler.items import DispensaryItem
import pandas as pd
import time


class CrawlerDetailDispensary(scrapy.Spider):
    name = "crawler_detail_dispensary"
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
        df = pd.DataFrame(pd.read_csv('dispensaries.csv', usecols=['ListingUrl', 'Listings', 'ChildListingUrl',
                                                                   'ChildListings', 'State', 'StoreUrl']))

        for index, rows in df.iterrows():
            list_data.append(rows.values)

        print("Leng list_data: " + str(len(list_data)))
        for data in list_data:
            print("data: " + str(data))
            url = data[5] + '/about'
            yield self.process_request(url=url, callback=self.parse, data=data)
            # time.sleep(0.5)

    def parse(self, response, data):
        item = DispensaryItem()
        # item['State'] = str(Selector(response).xpath(
        #     '//*[@class="map-title__TitleWrapper-sc-8szojn-0 juiolJ"]/text()').get()).replace(" in ", "")
        item['StoreUrl'] = response.request.url
        item['ListingUrl'] = response.request.url
        item['DispensaryName'] = Selector(response).xpath(
            '//*[@class="styled-components__Name-soafp9-0 cWmvtr"]/text()').get()
        item['Type'] = Selector(response).xpath(
            '//*[@class="styled-components__Capitalize-soafp9-10 gihoQE"]/text()').get()
        item['Address'] = Selector(response).xpath(
            '//*[@class="styled-components__AddressRow-sc-1k0lbjf-2 dwPNra"]/text()').get()
        list_working_time = Selector(response).xpath(
            '//*[@class="src__Box-sc-1sbtrzs-0 open-hours__Range-xpgk3n-7 fCOJPV"]/text()')
        for working_time in list_working_time:
            if list_working_time.index(working_time) == 0:
                item['Monday'] = working_time.get()
            elif list_working_time.index(working_time) == 1:
                item['Tuesday'] = working_time.get()
            elif list_working_time.index(working_time) == 2:
                item['Wednesday'] = working_time.get()
            elif list_working_time.index(working_time) == 3:
                item['Thursday'] = working_time.get()
            elif list_working_time.index(working_time) == 4:
                item['Friday'] = working_time.get()
            elif list_working_time.index(working_time) == 5:
                item['Saturday'] = working_time.get()
            elif list_working_time.index(working_time) == 6:
                item['Sunday'] = working_time.get()
        item['Phone'] = Selector(response).xpath('//a[contains(@href, "tel:")]/text()').get()
        item['Email'] = Selector(response).xpath('//a[contains(@href, "mailto:")]/text()').get()
        # item['Website'] = Selector(response).xpath('//a[contains(@href, "mailto:")]/text()').get()
        item['Instagram'] = Selector(response).xpath('//a[contains(@href, "https://www.instagram.com")]/text()').get()
        item['Twitter'] = Selector(response).xpath('//a[contains(@href, "https://twitter.com")]/text()').get()
        item['Facebook'] = Selector(response).xpath('//a[contains(@href, "https://www.facebook.com")]/text()').get()
        item['StoreUrl'] = data[5]
        item['State'] = data[4]
        item['ListingUrl'] = data[2]
        item['Listings'] = data[3]
        item['ChildListingUrl'] = data[0]
        item['ChildListings'] = data[1]
        # item['Address'] = Selector(response).xpath(
        #     '//*[@class="styled-components__Capitalize-soafp9-10 gihoQE"]/text()').get()  # styled-components__AddressRow-sc-1k0lbjf-2 dwPNra
        # item['Address'] = Selector(response).xpath(
        #     '//*[@class="styled-components__Capitalize-soafp9-10 gihoQE"]/text()').get()  # styled-components__AddressRow-sc-1k0lbjf-2 dwPNra
        # item['Address'] = Selector(response).xpath(
        #     '//*[@class="styled-components__Capitalize-soafp9-10 gihoQE"]/text()').get()  # styled-components__AddressRow-sc-1k0lbjf-2 dwPNra
        # item['Address'] = Selector(response).xpath(
        #     '//*[@class="styled-components__Capitalize-soafp9-10 gihoQE"]/text()').get()  # styled-components__AddressRow-sc-1k0lbjf-2 dwPNra
        yield item