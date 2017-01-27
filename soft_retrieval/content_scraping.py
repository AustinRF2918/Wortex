import requests
from colorama import Fore, Back, Style
import logging
import sys
import pandas as pd

from retrieval import info
from soft_retrieval.metadata_scraping import attempt_request

from bs4 import BeautifulSoup

# Goal: Place in (sub) strings and then be able to automatically
# pull classes of information from the document.

TAG_LIST = ['p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'li', 'span']

def clean_string(string):
    return string.strip()
    
def extract_tags(tag, response):
    if isinstance(response, requests.models.Response):
        page_soup = BeautifulSoup(response.text, 'html.parser')
    elif isinstance(response, BeautifulSoup):
        page_soup = response
    else:
        raise TypeError('response is not a requests.models.Response object or BeautifulSoup object..')

    return sum(list(
        map(lambda x: x.findAll(text=True), page_soup.findAll(tag)), ), [])
    
def extract_text(response):
    if not isinstance(response, requests.models.Response):
        raise TypeError('response is not a requests.models.Response object..')

    page_soup = BeautifulSoup(response.text, 'html.parser')

    extracted_tags = dict(
        zip(TAG_LIST, list(
            map(lambda x: list(list(
                filter(lambda y: y != '',
                       map(clean_string, extract_tags(x, page_soup))))), TAG_LIST))))

    return extracted_tags

def associate_with(substrings, response, item):
    if not isinstance(substrings, list):
       if isinstance(substrings, str):
           substrings = [substrings]
       else:
           raise TypeError('substrings is not a list or string.')

    if isinstance(response, requests.models.Response):
        page_soup = BeautifulSoup(response.text, 'html.parser')
    elif isinstance(response, BeautifulSoup):
        page_soup = response
    else:
        raise TypeError('response is not a requests.models.Response object or BeautifulSoup object..')

    return extracted_tags

def estimate_substrings(substrings, response):
    if not isinstance(substrings, list):
        if isinstance(substrings, str):
            substrings = [substrings]
        else:
            raise TypeError('substrings is not a list or string.')

    if not isinstance(response, requests.models.Response):
        raise TypeError('response is not a requests.models.Response object..')

    empties = list(filter(lambda x: len(x) < 4, substrings))

    if len(empties) != 0:
        raise ValueError('Substring lengths passed to fetch_substring_nodes must be greater than 4!')

class CFrameGenerator:
    def __init__(self, url, recursive=False):
        if not isinstance(url, str):
            raise TypeError("url in ContentFrame.__init__(url, ...)  must be of type str.")

        self.url = url

        if recursive is False:
            self.url_content = [attempt_request(self.url)]

        if self.url_content is None:
            raise ValueError("The URL you entered could not be deduced.")

    def __call__(self, class_name="", tags=TAG_LIST, additional_tags=[]):
        if not isinstance(class_name, str):
            raise TypeError("class_name in ContentFrame.__call__(class_name ...)  must be of type str.")

        tags_searched = tags

        for item in additional_tags:
            tags_searched.append(item)

        frame_data = []

        for page in self.url_content:
            soup = BeautifulSoup(page.text, "html.parser")

            class_nodes = []

            for item in tags_searched:
                if class_name != "":
                    class_nodes.append((item, soup.select(class_name + " " + item)))
                else:
                    class_nodes.append((item, soup.select(item)))

            for node in class_nodes:
                for j in node[1]:
                    if j.text.strip() != '':
                        frame_data.append({
                            'tag': node[0],
                            'text': j.text.strip()
                        })

        df = pd.DataFrame(frame_data)
        df.drop_duplicates()
        return df

    def page_classes(self, stag=None):
        other = set()

        for page in self.url_content:
            soup = BeautifulSoup(page.text, "html.parser")
            for tag in soup.find_all():
                try:
                    for item in tag['class']:
                        if tag != None:
                            if tag.tag == stag:
                                other.add(item)
                        else:
                            other.add(item)
                                
                except:
                    pass

        return pd.Series(list(other))

def test():
    c = CFrameGenerator("http://youtube.com")
    df = c(".feed-message");
    print(df)
