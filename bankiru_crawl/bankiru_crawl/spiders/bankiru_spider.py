import scrapy
from bankiru_crawl.items import BankiruCrawlItem
# from scrapy.shell import inspect_response


class bankiru_spider(scrapy.Spider):
    handle_httpstatus_list = [404]
    name = "bankiru_spider"
    allowed_domains = ['banki.ru']
    URL = "http://www.banki.ru/services/responses/bank/{}/?page="
    # header = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate',
    #          'Accept': '*/*', 'User-Agent': 'python-requests/2.12.4'}
    xpaths = {'review_text': ('div[@class="responses__item__message '
                              'markup-inside-small '
                              'markup-inside-small--bullet"]/text()'),
              'review_url': 'div/a[@itemprop="url"]/@href',
              'review_header': 'div/a[@itemprop="url"]/text()',
              'review_author_url': 'footer//a[@itemprop="author"]/@href',
              'review_author_name': 'footer//a[@itemprop="author"]/span[@itemprop="name"]/text()',
              'review_datetime': 'footer//time/@datetime',
              'review_rating': 'div//meta[@itemprop="ratingValue"]/@content',
              'bank_answer_datetime': 'div//time/@datetime',
              'bank_answer_text': 'div//div[@class="thread-item__text"]/text()'}
    check_404 = False

    def start_requests(self):
        page_number = int(self.start_page)
        while True:
            if self.check_404:
                break
            page_number += 1
            url = self.URL.format(self.bank_name)
            yield scrapy.Request(url=url + str(page_number), callback=self.parse)

    def parse(self, response):
        def extract_item(article, x_path):
            content = article.xpath(x_path).extract()
            item = content[0] if len(content) > 0 else "empty"
            return item
        # inspect_response(response, self)
        if response.status == 404:
            self.check_404 = True
        for article in response.xpath('//article'):
            item = BankiruCrawlItem()
            item['bank_name'] = self.bank_name
            item["review_text"] = " ".join(article.xpath(self.xpaths['review_text'])
                                           .extract())
            item["review_url"] = extract_item(article, self.xpaths['review_url'])
            item["review_header"] = extract_item(article, self.xpaths['review_header'])
            item["review_author_url"] = extract_item(article,
                                                     self.xpaths['review_author_url'])
            item["review_author_name"] = extract_item(article, self.xpaths['review_author_name'])
            item['review_datetime'] = extract_item(article, self.xpaths['review_datetime'])
            item['review_rating'] = extract_item(article, self.xpaths['review_rating'])
            item['bank_answer_datetime'] = extract_item(article,
                                                        self.xpaths['bank_answer_datetime'])
            item['bank_answer_text'] = " ".join(article.xpath(self.xpaths['bank_answer_text']).extract())
            if item['bank_answer_text'] != '':
                item['bank_answer_check'] = True
            else:
                item['bank_answer_check'] = False
            yield item
