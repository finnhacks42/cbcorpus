import scrapy
import re


class BoeQbSpiderSpider(scrapy.Spider):
    name = 'boe_qb_spider'
    allowed_domains = ['www.bankofengland.co.uk']
    start_urls = ['https://www.bankofengland.co.uk/sitemap/quarterly-bulletin']

    def parse(self, response):

        # selector for each year in the section of the page below the Documents heading
        nodes = response.xpath("//h2[contains(text(),'Documents')]/following::li[contains(text(),'bulletin')]/ul/li")
        for n in nodes:
            label = ''.join(n.xpath("text()").getall()).strip()
            if re.match(r'\d{4}',label):
                year = int(label)
                if year > 2010:
                    urls = n.xpath("ul/li/a/@href").getall()
                    item = {}
                    item['year']=label
                    item['file_urls'] = [response.urljoin(link) for link in urls]
                    yield item
            
           
