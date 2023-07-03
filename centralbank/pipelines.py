# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pathlib import Path
import hashlib



class CentralbankPipeline:
    def process_item(self, item, spider):
        return item


class HTMLSnippetPipeline:
    """Pipeline for saving a section of html from a page to a file."""

    def __init__(self, files_store):
        self.datapath = Path(files_store)/'html'
        ## todo create subdirectory for html if not exits

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            files_store=crawler.settings.get('FILES_STORE'),
        )

    def open_spider(self, spider):
        folder = (self.datapath/spider.name).mkdir(parents=True, exist_ok=True)

    def process_item(self, item, spider):
        
        # check for html_subset
        if 'html_doc' in item:
            snip = item.pop('html_doc')
            filehash = hashlib.md5(snip).hexdigest()
            filepath = self.datapath/spider.name/f"{filehash}.html"
            with open(filepath,'wb') as f:
                f.write(snip)
            item['html_path'] = str(filepath)

        return item