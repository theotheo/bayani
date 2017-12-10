# coding=utf-8
import logging
import re

import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from w3lib.html import remove_tags, replace_tags

import coloredlogs

coloredlogs.install(level='DEBUG')

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'scrapy': {
            'level': 'DEBUG',
        },
    }
}

# logging.config.dictConfig(DEFAULT_LOGGING)



# %%
class Spider(CrawlSpider):
    name = "lyricshare"

    allowed_domains = ['lyricshare.net']
    
    # http://lyricshare.net/ru/Artists/ru-A.html
    rules = (
        Rule(LinkExtractor(allow=(r'ru/Artists/ru.*$'))),
        Rule(LinkExtractor(allow=(r'ru/[0-9a-z\-]+/$'))),
        Rule(LinkExtractor(allow=(r'ru/[0-9a-z\-]+/[0-9a-z\-]+.html$')), 
                                  callback='parse_lyric')
    )
#   custom_settings = {
        # 'LOGSTATS_INTERVAL': 15,
#        'EXTENSIONS': {
#            'scrapy.extensions.logstats.LogStats': 300
#        }
#    }
    
    start_urls = ['http://lyricshare.net/']

    def parse_lyric(self, response):
        item = {}
        item['url'] = response.url
        ## A little bit ugly
        item['meta'] = '---'.join(response.css('h1').xpath('.//text()').extract())
        item['text'] = '\n'.join(response.css('#textpesni').xpath('.//text()').extract())
        yield item
