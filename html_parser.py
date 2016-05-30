#coding=utf-8
__author__ = 'worker'

import urlparse
import re
from bs4 import BeautifulSoup

class HtmlParser(object):
    def _get_new_urls(self, page_url, soup):
        new_urls = set()

        # http://67.media.tumblr.com/52d4a44283cce631585ca4ff13ed4fa1/tumblr_o7yqogKV5m1r2xjmjo1_250.jpg
        links = soup.find_all("div", attrs={"class": "post_thumbnail_container has_imageurl"})
        for link in links:
            try:
                new_url = link["data-imageurl"]
                # print new_url
                new_urls.add(new_url)
            except:
                continue

        return new_urls

    def _get_next_link(self, page_url, soup):
        # /archive/?before_time=1460948524
        next_link = soup.find("a", href=re.compile(r"/archive/\?before_time=\d+"))
        next_full_link = None
        if not next_link is None:
            next_full_link = urlparse.urljoin(page_url, next_link["href"])
            # print "next_full_link=%s"%next_full_link
        
        return next_full_link

    def parse(self, page_url, html_cont):
        if (page_url is None ) or (html_cont is None):
            return

        soup = BeautifulSoup(html_cont, "html.parser", from_encoding="utf-8")
        new_urls = self._get_new_urls(page_url, soup)
        next_link = self._get_next_link(page_url, soup)

        return new_urls, next_link