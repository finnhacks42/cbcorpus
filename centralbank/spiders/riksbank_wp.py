import scrapy


class RiksbankWpSpider(scrapy.Spider):
    name = 'riksbank_wp'
    allowed_domains = ['www.riksbank.se']
    start_urls = [
        'https://www.riksbank.se/en-gb/press-and-published/publications/working-paper-series/',
        'https://www.riksbank.se/en-gb/press-and-published/publications/staff-memos/'
        ]

    def parse(self, response):
        """Parse the start url"""
        
        papers = response.xpath("//div[@class='listing-block__body']/ul/li")
        for p in papers:
            paper_link = p.xpath('a/@href').get()
            item = {}
            item['pubdate'] = p.xpath('a/span[1]/text()').get()
            item['title'] = p.xpath('a//span[@class="header--file__title"]/text()').get()

            if paper_link.endswith(".pdf") or p.xpath('a/@target').get():
                if not paper_link.endswith(".xlxs"): 
                    pdf_url = response.urljoin(paper_link)
                    item['pdf_url'] = pdf_url
                    item['file_urls'] = [pdf_url]
                    yield item
            
            else:
                if not paper_link.endswith(".xlxs"):
                    yield response.follow(paper_link, callback = self.parse_paper, meta={'item':item})
            
    def parse_paper(self, response):
        item = response.meta['item']
        pdf_urls = response.xpath("//span[contains(text(),'Download PDF')]/../../a/@href").getall()
        pdf_url = sorted(pdf_urls, key=lambda x: len(x))[0] # assume shortest url is correct one (mostly they are just dups)
        pdf_url = response.urljoin(pdf_url)
        item['pdf_url'] = pdf_url
        item['file_urls'] = [pdf_url]
        return item
        

            
            
