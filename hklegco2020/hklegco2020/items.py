# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Hklegco2020Item(scrapy.Item):
    table_type_e = scrapy.Field()
    table_type_c = scrapy.Field()
    table_code = scrapy.Field()
    district_c = scrapy.Field()
    district_e = scrapy.Field()
    nominee_count = scrapy.Field()
    name_c = scrapy.Field()
    name_e = scrapy.Field()
    alias_c = scrapy.Field()
    alias_e = scrapy.Field()
    gender_c = scrapy.Field()
    gender_e = scrapy.Field()
    occupation_c = scrapy.Field()
    occupation_e = scrapy.Field()
    affiliation_c = scrapy.Field()
    affiliation_e = scrapy.Field()
    date_of_nomination = scrapy.Field()

