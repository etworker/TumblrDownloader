__author__ = 'worker'

import traceback, os, sys
import url_manager, html_downloader, html_parser, html_outputer

class TumblrDownloader(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def download(self, accountName):
        next_link = "http://%s.tumblr.com/archive/" % accountName

        print "start download %s in tumblr" % accountName

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
            # break;

        # Print all
        print "total %d pages, contains %d url" % (pageCount, self.urls.url_count())
        self.urls.print_all_urls()

        # download all to ./download/<accountName>/
        dir = "%s/download/%s" % (os.getcwd(), accountName)
        if not os.path.exists(dir):
            os.makedirs(dir)

        fileCount = 0
        totlaCount = self.urls.url_count()
        while self.urls.has_new_url():
            fileCount = fileCount + 1
            url = self.urls.get_new_url();

            # replace small image to big image
            url = url.replace("_250.", "_1280.")

            # download image
            if self.downloader.downloadImage(url, dir):
                print "+ %d/%d OK" % (fileCount, totlaCount)
            else:
                print "- %d/%d Failed, url = %s" % (fileCount, totlaCount, url)

        print "finished"

    def print_usage(self):
        print "Usage:\n"
        print "%s <accountName>\n" % sys.argv[0]
        print "e.g.\n"
        print "%s wanimal1983" % sys.argv[0]

if __name__ == "__main__":
    obj_spider = TumblrDownloader()

    if len(sys.argv) <= 1:
        obj_spider.print_usage()
    else:
        obj_spider.download(sys.argv[1])
    