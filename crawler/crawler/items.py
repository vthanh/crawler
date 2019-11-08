# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DispensaryItem(scrapy.Item):
    State = scrapy.Field()
    Type = scrapy.Field()
    Listings = scrapy.Field()
    ChildListings = scrapy.Field()
    DispensaryName = scrapy.Field()
    Address = scrapy.Field()
    Phone = scrapy.Field()
    Monday = scrapy.Field()
    Tuesday = scrapy.Field()
    Wednesday = scrapy.Field()
    Thursday = scrapy.Field()
    Friday = scrapy.Field()
    Saturday = scrapy.Field()
    Sunday = scrapy.Field()
    Email = scrapy.Field()
    Website = scrapy.Field()
    Instagram = scrapy.Field()
    Twitter = scrapy.Field()
    Facebook = scrapy.Field()
    Description = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    ListingUrl = scrapy.Field()
    ChildListingUrl = scrapy.Field()
    StoreUrl = scrapy.Field()


class ProductItem(scrapy.Item):
    StoreUrl = scrapy.Field()
    ProductName = scrapy.Field()
    ProductType = scrapy.Field()
    Price = scrapy.Field()
    ProductUrl = scrapy.Field()

