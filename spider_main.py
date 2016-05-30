__author__ = 'worker'

import traceback
from TumblrDownloader import url_manager, html_downloader, html_parser, html_outputer

class TDMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def download(self, accountName):
        next_link = "http://%s.tumblr.com/archive/" % accountName

        # Collect all urls
        while not next_link is None:
            html_cont = self.downloader.downloadPage(next_link)
            new_urls, next_link = self.parser.parse(next_link, html_cont)

            if not new_urls is None:
                self.urls.add_new_urls(new_urls)

        # Print all
        self.urls.print_all_urls()

if __name__ == "__main__":
    # root_url = "http://wanimal1983.org/archive/filter-by/photo"
    obj_spider = TDMain()
    obj_spider.download("wanimal1983")