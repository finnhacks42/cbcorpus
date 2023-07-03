import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class FedsNotesSpider(CrawlSpider):
    name = 'feds_notes'
    allowed_domains = ['www.federalreserve.gov']
    start_urls = [
        'https://www.federalreserve.gov/econres/notes/feds-notes/2022-index.htm',
        'https://www.federalreserve.gov/econres/notes/feds-notes/all-years.htm'
    ]
    #    'https://www.federalreserve.gov/econres/notes/feds-notes/all-years.htm']
    #'https:\/\/www.federalreserve.gov\/econres\/notes\/feds-notes\/\d{4}-index.htm'
    #https://www.federalreserve.gov/econres/notes/feds-notes/2019-index.htm
    rules = (
        Rule(LinkExtractor(allow=r'https:\/\/www.federalreserve.gov\/econres\/notes\/feds-notes\/\d{4}-index.htm'), callback='parse_year', follow=False),
    )

    def parse_year(self, response):

        papers = response.xpath("//div[@class='col-xs-12 col-md-9 heading feds-note']")

        for p in papers:
            item = {}
            item['pubdate'] = p.xpath('div/time/@datetime').get()
            item['title'] = p.xpath('div/h5/a/text()').get()
            item['summary'] = p.xpath('div/p[1]/text()').get()
            item['doi'] = p.xpath('div/p[2]/text()').get()
            paper_link = p.xpath('div/h5/a/@href').get()
            yield response.follow(paper_link, callback = self.parse_paper, meta={'item':item})
            

    def parse_paper(self, response):
        item = response.meta['item']
        item['html_doc'] = response.body
        section_headings = response.xpath("//p/strong")

        # try and pull out the references from the html
        for h in section_headings:
            text = h.xpath('text()').get()
            if text is not None:
                text = text.lower()
            if text in ['references','bibliography']:
                clean_refs = []
                references = h.xpath('../following-sibling::p')
                for r in references:
                    ref = {} 
                    ref['auth_title'] = r.xpath('./text()').get()
                    ref['journal'] = r.xpath('./em/text()').get()
                    clean_refs.append(ref)
                item['references'] = clean_refs

        return item
        
