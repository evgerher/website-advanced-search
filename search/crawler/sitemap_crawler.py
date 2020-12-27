import scrapy
from scrapy.crawler import CrawlerProcess


class WebsiteSpider(scrapy.spiders.SitemapSpider):
  name = 'sitemap-crawler'
  download_delay = 1

  sitemap_urls = ['https://sallysbakingaddiction.com/sitemap_index.xml']
  sitemap_rules = [('', 'parse_article')]

  def parse_article(self, response):
    if 'sallysbakingaddiction.com' in response.url:
      self.logger.info('Parsed article: %s', response.url)
      yield {'url': response.url, 'content': response.text}


crawler = CrawlerProcess({
  'USER_AGENT': 'Mozilla/5.0',

  # save in file as CSV, JSON or XML
  'FEED_FORMAT': 'xml',  # csv, json, xml
  'FEED_URI': 'output.xml',
})
crawler.crawl(WebsiteSpider)
crawler.start()
