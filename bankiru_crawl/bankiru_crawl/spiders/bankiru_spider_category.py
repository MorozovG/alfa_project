import scrapy
from bankiru_crawl.items import BankiruCrawlItemCat
# from scrapy.shell import inspect_response


class bankiru_spider(scrapy.Spider):
    handle_httpstatus_list = [404]
    name = "bankiru_spider_category"
    allowed_domains = ['banki.ru']
    URL = "http://www.banki.ru/services/responses/bank/{}/product/{}/?page="
    categories_check_404 = {'autocredits': False, 'deposits': False,
                            'debitcards': False, 'businessdeposits': False,
                            'remote': False, 'hypothec': False,
                            'creditcards': False, 'businesscredits': False,
                            'leasing': False, 'corporate': False,
                            'credits': False, 'restructing': False}

    def start_requests(self):
        for category in self.categories_check_404.keys():
            page_number = 0
            while not self.categories_check_404[category]:
                page_number += 1
                url = self.URL.format(self.bank_name, category)
                yield scrapy.Request(url=url + str(page_number),
                                     callback=self.parse,
                                     meta={'category': category})

    def parse(self, response):
        def extract_item(article, x_path):
            content = article.xpath(x_path).extract()
            item = content[0] if len(content) > 0 else "empty"
            return item
        # inspect_response(response, self)
        if response.status == 404:
            self.categories_check_404[response.meta['category']] = True
        x_path = 'div/a[@itemprop="url"]/@href'
        for article in response.xpath('//article'):
            item = BankiruCrawlItemCat()
            item['bank_name'] = self.bank_name
            item["review_url"] = extract_item(article, x_path)
            item['review_category'] = response.meta['category']
            yield item
