import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class RbaRdpsSpider(CrawlSpider):
    name = 'rba_rdps'
    allowed_domains = ['www.rba.gov.au']
    start_urls = [
        "https://www.rba.gov.au/publications/rdp/2001-2010.html",
        "https://www.rba.gov.au/publications/rdp/2011-2020.html",
        "https://www.rba.gov.au/publications/rdp/2021-2030.html"
    ]

    rules = (
        Rule(
            LinkExtractor(allow=(r'\/publications\/rdp\/\d{4}\/(\w+|-)+')),
            callback='parse_item', 
            follow=False
        ),
    )

    def parse_item(self, response):
        """Parse the response for a given RDP"""
        item = {}
        item['rdp_number'] = response.xpath("//h1[@class='page-title']/span/text()").get()
        item['abstract'] = response.xpath("//div[@class='rss-rdp-description']/p/text()").extract()
        item['pubdate'] = response.xpath("//div[@class='box-article-info']/p[2]/text()").get()
        item['authors'] = response.xpath("//div[@class='box-article-info']/p[@class='author']//text()").get()
        item['links'] = response.xpath("//div[@class='box-article-info']//a/@href").extract()

        file_urls = []
        for link in item['links']:
            if link.endswith(".pdf") and 'non-technical' not in link:
                absolute_url = response.urljoin(link)
                file_urls.append(absolute_url)
        item['file_urls'] = file_urls

        return item

       