import scrapy
from scrapy.selector import Selector
from crawler.items import DispensaryItem

list_states = ['alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware', 'florida', 'georgia', 'hawaii', 'idaho' , 'illinois',
               'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi', 'missouri', 'montana', 'nebraska', 'new-hampshire',
               'new-jersey', 'new-mexico', 'new-york', 'north-carolina', 'north-dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania', 'rhode-island', 'sault-ste-marie', 'south-carolina', 'south-dakota', 'tennessee', 'texas', 'utah',
               'vermont', 'virginia', 'washington', 'washington-dc', 'west-virginia', 'wisconsin', 'wyoming']


class CrawlerSpider(scrapy.Spider):
    name = "crawler"
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    allowed_domains = ["weedmaps.com"]
    _urls = "https://weedmaps.com"

    def process_request(self, url, callback):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        if callback:
            return scrapy.Request(url=url, callback=callback, headers=headers)
        return scrapy.Request(url=url, headers=headers)

    def get_text_from_string_tags(self, text):
        return text.split('>')[1].split('<')[0]

    def start_requests(self):
        urls = [
            'https://weedmaps.com/dispensaries/in/united-states'
        ]
        for state in list_states:
            urls.append(str(urls[0]) + '/' + state)

        for url in urls:
            yield self.process_request(url=url, callback=self.parse)

    def parse(self, response):
        listings = Selector(response).xpath('//*[@class="region-subregions-tray__RegionLink-jf99ya-3 eGEnlj"]')
        item = DispensaryItem()
        print("len(listings): " + str(len(listings)))
        if len(listings) <= 0:
            dispensaries = Selector(response).xpath(
                '//*[@class="src__Box-sc-1sbtrzs-0 src__Flex-sc-1sbtrzs-1 styled-components__LinkWrap-sc-8si1dn-1 bNbtAW"]')
            for dispensary in dispensaries:
                item['State'] = str(Selector(response).xpath(
                    '//*[@class="map-title__TitleWrapper-sc-8szojn-0 juiolJ"]/text()').get()).replace(" in ", "")
                item['Listings'] = None
                item['DispensaryName'] = dispensary.xpath(
                    '//*[@class="styled-components__Name-sc-8si1dn-11 styled-components__NameOneLine-sc-8si1dn-12 fqPnyF"]/text()').get()
                item['StoreUrl'] = self._urls + dispensary.css('a::attr(href)').extract_first()
                yield item
        else:
            for listing in listings:
                listing_url = self._urls + listing.css('a::attr(href)').extract_first()
                item['ListingUrl'] = listing_url
                item['State'] = str(Selector(response).xpath(
                    '//*[@class="map-title__TitleWrapper-sc-8szojn-0 juiolJ"]/text()').get()).replace(" in ", "")
                item['Listings'] = str(self.get_text_from_string_tags(listing.get()))
                yield item
