import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class FedFedsSpider(CrawlSpider):
    name = 'fed_feds'
    allowed_domains = ['www.federalreserve.gov']
    start_urls = ['https://www.federalreserve.gov/econres/feds/all-years.htm']

    rules = (
        Rule(LinkExtractor(allow=r'https:\/\/www.federalreserve.gov\/econres\/feds\/20\d{2}.htm'), callback='parse_year', follow=False),
    )

    def parse_year(self, response):

        papers = response.xpath("//div[@class='col-xs-12 col-md-9 heading feds-note']")

        for p in papers:
            item = {}
            item['pubdate'] = p.xpath('div/time/@datetime').get()
            item['title'] = p.xpath('div/h5/a/text()').get()
            paper_link = p.xpath('div/h5/a/@href').get()
            item['paper_link'] = paper_link
            yield response.follow(paper_link, callback = self.parse_paper, meta={'item':item})

    def parse_paper(self, response):
        item = response.meta['item']
        headings = response.xpath("//p/strong")

        item['headings'] = headings.xpath('text()').getall()

          # try and pull out the abstract from the html
        for h in headings:
            text = h.xpath('text()').get()
            if text is not None:
                text = text.lower().strip()

            if re.match(r'abstract\S{0,2}',text): 
                item['abstract'] = h.xpath('../following-sibling::p/text()').get()
                

            elif re.match(r'pdf\S{0,2}',text):  
                pdf_url = h.xpath('../a/@href').get()
                pdf_url = response.urljoin(pdf_url)
                item['file_urls'] = [pdf_url]
                break # stop looking once we have found this

        return item
        
        


