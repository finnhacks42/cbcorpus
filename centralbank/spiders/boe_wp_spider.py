import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BoeWpSpiderSpider(CrawlSpider):
    name = 'boe_wp_spider'
    allowed_domains = ['www.bankofengland.co.uk']
    start_urls = ['http://www.bankofengland.co.uk/sitemap/staff-working-paper']

    rules = (
        Rule(LinkExtractor(
            allow=(r'https:\/\/www.bankofengland.co.uk\/working-paper\/\d+\/(\w+|-)+')), 
            callback='parse_item', 
            follow=True
        ),
    )

    def parse_item(self, response):
        """Parse the response for a given working paper."""
        item = {}
        item['pubdate'] = response.xpath("//div[contains(@class,'published-date')]/text()").get()
        item['abstract'] = response.xpath("//div[contains(@class,'page-content')]/p[1]/text()").get()
        relative_pdf_url = response.xpath("//div[contains(@class,'page-content')]/p/a/@href").get()
        pdf_url = response.urljoin(relative_pdf_url)
        item['pdf_url'] = pdf_url
        item['file_urls'] = [pdf_url]
        return item
