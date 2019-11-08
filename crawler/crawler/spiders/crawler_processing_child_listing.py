import scrapy
from scrapy.selector import Selector
from crawler.items import DispensaryItem
import pandas as pd


class CrawlerProcessingChildListing(scrapy.Spider):
    name = "crawler_processing_child_listing"
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
        df = pd.DataFrame(pd.read_csv('data.csv', usecols=['ListingUrl', 'Listings', 'State']))
        for index, rows in df.iterrows():
            list_data.append(rows.values)
        print("Leng list_data: " + str(len(list_data)))
        for data in list_data:
            url = data[0]
            yield self.process_request(url=url, callback=self.parse, data=data)

    def parse(self, response, data):
        print("data: " + str(data))
        list_listings = []
        try:
            list_listings = Selector(response).xpath('//*[@class="region-subregions-tray__RegionLink-jf99ya-3 eGEnlj"]')
        except:
            print("Not contain child lising")
        if len(list_listings) > 0:
            for listing in list_listings:
                item = DispensaryItem()
                url = self._urls + listing.css('a::attr(href)').extract_first()
                print("url list_data: " + str(url))
                item['State'] = data[2]
                item['ListingUrl'] = data[0]
                item['Listings'] = data[1]
                item['ChildListingUrl'] = url
                item['ChildListings'] = str(self.get_text_from_string_tags(listing.get()))
                yield item
        else:
            item = DispensaryItem()
            item['State'] = data[2]
            item['ListingUrl'] = data[0]
            item['Listings'] = data[1]
            item['ChildListingUrl'] = None
            yield item