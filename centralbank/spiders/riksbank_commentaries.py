import scrapy


class RiksbankCommentariesSpider(scrapy.Spider):
    name = 'riksbank_commentaries'
    allowed_domains = ['www.riksbank.se']
    start_urls = ['https://www.riksbank.se/en-gb/press-and-published/publications/economic-commentaries/']

    def parse(self, response):
        """Parse the start_url"""
        papers = response.xpath("//div[@class='listing-block__body']/ul/li")
        for p in papers:
            paper_link = p.xpath('a/@href').get()
            item = {}
            item['pubdate'] = p.xpath('a/span[1]/text()').get()
            item['title'] = p.xpath('a/span[2]/text()').get()

            # direct link to pdf, no further url to follow
            # this is the case for most of their papers (except the most recent few)
            if paper_link.endswith(".pdf"): 
                pdf_url = response.urljoin(paper_link)
                item['pdf_url'] = pdf_url
                item['file_urls'] = [pdf_url]
                yield item

            # dont download data files
            elif paper_link.endswith('.xlxs'):
                continue 
            
            # link is to a seperate page
            else:
                yield response.follow(paper_link, callback = self.parse_paper, meta={'item':item})
            
    def parse_paper(self, response):
        """Parse info from the paper page and download the pdf."""
        item = response.meta['item']
        pdf_urls = response.xpath("//a[@class='report-page__download']/@href").getall()
        pdf_url = sorted(pdf_urls, key=lambda x: len(x))[0] # assume shortest url is correct one
        pdf_url = response.urljoin(pdf_url)
        item['pdf_url'] = pdf_url
        item['file_urls'] = [pdf_url]
        return item
