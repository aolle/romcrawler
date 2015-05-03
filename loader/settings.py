# Scrapy settings for romloader project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'loader'

SPIDER_MODULES = ['loader.spiders']
NEWSPIDER_MODULE = 'loader.spiders'
ITEM_PIPELINES = ['loader.pipelines.loaderpipeline']


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20130917 Firefox/17.0 Iceweasel/17.0.9'
CONCURRENT_REQUESTS_PER_DOMAIN = '20'
