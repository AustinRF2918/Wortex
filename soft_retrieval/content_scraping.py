import requests
from colorama import Fore, Back, Style
from html.parser import HTMLParser
import logging
import sys
import pandas as pd

if __name__ == '__main__':
    import metadata_scraping.attempt_request
else:
    from soft_retrieval.metadata_scraping import attempt_request

from bs4 import BeautifulSoup

# Goal: Place in (sub) strings and then be able to automatically
# pull classes of information from the document.

class HTMLCrawler(HTMLParser):
    def handle_starttag(self, tag, attrs):
        x = tag

    def handle_endtag(self, tag):
        y = tag

    def handle_data(self, data):
        print(type(data))
        if data.strip() != '':
            print("{}".format(data))
        
class SiteFrameGenerator:
    def __init__(self, url):
        req = requests.get(url)
        parser = HTMLCrawler()
        parser.feed(req.text)
        
def run_tests():
    def initialization():
        x = SiteFrameGenerator("http://andrewjacoblee.com")

    initialization()
