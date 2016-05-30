__author__ = 'worker'

import traceback, os
import url_manager, html_downloader, html_parser, html_outputer

class TumblrDownloader(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def download(self, accountName):
        next_link = "http://%s.tumblr.com/archive/" % accountName

        # collect all urls
        # each page contains one url link to next page
        pageCount = 0
        while not next_link is None:
            pageCount = pageCount + 1
            print "downloading page %d ..." % pageCount
            html_cont = self.downloader.downloadPage(next_link)
            new_urls, next_link = self.parser.parse(next_link, html_cont)

            if not new_urls is None:
                self.urls.add_new_urls(new_urls)

            # stop here for debug
            break;

        # Print all
        print "total %d pages, contains %d url" % (pageCount, self.urls.url_count())
        self.urls.print_all_urls()

        # download all to ./<accountName>/
        dir = "%s/%s" % (os.getcwd(), accountName)
        if not os.path.exists(dir):
            os.makedirs(dir)

        while self.downloader.has_new_url():
            url = self.urls.get_new_url();            
            if self.downloader.downloadImage(url, dir):
                print "+ %s" % url
            else:
                print "- %s" % url

        print "finished"

if __name__ == "__main__":
    # root_url = "http://wanimal1983.org/archives"
    obj_spider = TumblrDownloader()
    obj_spider.download("wanimal1983")
    