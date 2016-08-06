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

import urllib2, cookielib, urllib
import lxml.html
from PIL import Image
from StringIO import StringIO
from pytesser.pytesser import image_to_string
from tmpmanager import tmanage
import requests
import os
import elementtree.ElementTree as ET

__author__ = "Angel Olle Blazquez"

class loaderpipeline(object):

    http_header = {
                "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20130917 Firefox/17.0 Iceweasel/17.0.9",
                "Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,text/png,*/*;q=0.5",
                "Accept-Language" : "en-us,en;q=0.5",
                "Accept-Charset" : "ISO-8859-1",
                "Content-type": "application/x-www-form-urlencoded",
                "Host" : "",
                "Referer" : ""
                }
    save_dir=None
    max_retries = 5  

    def parse_cfg(self):
        tree = ET.parse(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.', 'config.xml'))
        cfg = tree.getroot()
        self.save_dir = cfg.find('./local/save_dir').text
        self.http_header['Host']=cfg.find('./remote/ddomain').text
        self.max_retries= int(cfg.find('./local/max_retries').text)
        if cfg.find('./local/tmp').text == 'yes':
            self.tmp = True 
        else: self.tmp = False
        self.negative_responses = [resp.text for resp in cfg.findall('./remote/negative_responses/response')]


    def process_form(self,form,captcha):
        form.fields['code']=captcha.replace('\n','')
        return dict(form.fields)	
    
    def save_file(self, resp, platform, filename):
        self.save_dir = ''.join([self.save_dir, "/", platform])
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        with open(''.join([self.save_dir, "/", filename]),'w+') as f:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
        return filename

    def solve_captcha(self,img):
        imagename = img.split("/")[-1]
        req = urllib2.Request(img)
        img_file = Image.open(StringIO(urllib2.urlopen(req).read()))
        img_file.resize((116, 56), Image.NEAREST)
        if self.tmp:
            with tmanage() as t:  
                n = ''.join([t, "/code.tif"])
                img_file.save(n)
	        img_file = Image.open(n)
                s = image_to_string(img_file)
                img_file.close()
        else:
            output = StringIO()
            img_file.save(output,format="TIFF")
            s = image_to_string(Image.open(StringIO(output.getvalue())))
            output.close()
        s = s.replace(' ','')
        s = s.replace('.','')
        return s[:4]	


    def process_item(self, item, spider):
        self.parse_cfg()
        retries = 1
        while retries < self.max_retries:
		jar = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
		url = ''.join(["http://", item['url'].strip()])
		site = opener.open(url).read()
		dom = lxml.html.fromstring(site)
		imgurl = dom.xpath('//div[@id="codecheck"]/img/@src')[0]
		params = self.process_form(dom.forms[1], self.solve_captcha(imgurl))
		a,b= dom.forms[1].action.split('?')[1].split('=')
		c = {}
		c[a]=b	
		self.http_header['Refer'] = url
		resp = requests.post(dom.forms[1].action.split('?')[0], params=c ,data=params, headers=self.http_header, cookies=requests.utils.dict_from_cookiejar(jar),stream=True)
                if resp.text not in self.negative_responses:
                    print ''.join([ self.save_file(resp, str(item['platform']), str(params['filename']))," ... saved!" ])
                    break
                else: retries += 1
                

        if retries == self.max_retries: print ''.join(["Error: ", str(params['filename']), " not saved!"])

        return item






