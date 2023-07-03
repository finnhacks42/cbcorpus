import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from pathlib import Path
import hashlib


class RbaBulletinSpiderSpider(CrawlSpider):
    name = 'rba_bulletin_spider'
    allowed_domains = ['rba.gov.au']
    start_urls = ['https://www.rba.gov.au/publications/bulletin']

    rules = (
        Rule(LinkExtractor(
            allow=(r'https:\/\/www.rba.gov.au\/publications\/bulletin\/20[1-2]{1}\d')),
            callback='parse_item', 
            follow = True,
        ),
    )

    def parse_item(self, response):        
        
        abstract = response.xpath("//div[@id='content']//div[@class='box-abstract']//p//text()").getall()
        pubdate = response.xpath("//div[@id='content']//time//@datetime").get()
        pubtitle = response.xpath("//span[@class='publication-name']/text()").get()


        references = response.xpath("//div[@id='content']//div[@id='bibliography']//p")
        if references is None or len(references) == 0:
            references = response.xpath("//div[@id='content']//div[@id='references']//p")

        references = [r.xpath('text()').getall() for r in references]

        if len(references) > 0 or len(abstract) > 0:
            item = {}
            item['pubdate'] = pubdate
            item['pubtitle'] = pubtitle
            item['abstract'] = abstract
            item['references'] = references
            item['url'] = response.url
            item['html_doc'] = response.body
            return item
        
        # else:
        #     links = response.xpath('//h2[text()="Contents"]/following-sibling::h3[text()="Articles"]/following-sibling::ul[1]/li/div[@class="title"]//a/@href').getall()
        #     for l in links:
        #         yield response.follow(l, callback = self.parse_item)
            

#'https:\/\/www.bankofengland.co.uk\/working-paper\/\d+\/(\w+|-)+')), 