"""    This file is part of rom-crawler.

    rom-crawler is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    rom-crawler is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with rom-crawler.  If not, see <http://www.gnu.org/licenses/>.
"""

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from loader.items import RomItem 
import os
import elementtree.ElementTree as ET

__author__ = "Angel Olle Blazquez"

class NSpider(BaseSpider):
        tree = ET.parse(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../', 'config.xml'))
        cfg = tree.getroot()
        name = cfg.find('./local/name').text

        allowed_domains = [domain.text for domain in cfg.findall('./remote/domain')]
        start_urls = [url.text for url in cfg.findall('./remote/start_url')]
       
	def parse(self, response):
		hxs = HtmlXPathSelector(response)  
		platform = hxs.select('//div[@id="heading"]/h1/text()').extract()
                games = hxs.select("//div[@class='listings']/table/tr/td/a/text()").extract()
                urls = hxs.select('//div[@class="listings"]/table/tr/td/a/@href').extract()
                urls = [self.allowed_domains[0]+i.replace("rs","dd/rls") for i in urls]
		items = []
		for i,e in enumerate(games):
			item = RomItem()
			item['platform'] = platform
			item['title'] = e
			item['url'] = urls[i]
			items.append(item)
		return items
