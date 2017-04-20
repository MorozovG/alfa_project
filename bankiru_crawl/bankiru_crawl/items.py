# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BankiruCrawlItem(scrapy.Item):
    review_header = scrapy.Field()
    review_text = scrapy.Field()
    review_datetime = scrapy.Field()
    review_rating = scrapy.Field()
    review_url = scrapy.Field()
    review_author_name = scrapy.Field()
    review_author_url = scrapy.Field()
    bank_answer_check = scrapy.Field()
    bank_answer_text = scrapy.Field()
    bank_answer_datetime = scrapy.Field()
    bank_name = scrapy.Field()


class BankiruCrawlItemCat(scrapy.Item):
    review_url = scrapy.Field()
    review_category = scrapy.Field()
    bank_name = scrapy.Field()
