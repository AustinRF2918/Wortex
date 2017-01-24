import requests
from colorama import Fore, Back, Style
import logging
import sys
from retrieval import info
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

def test(req):
    site_text = extract_text(req)
    other = associate_with(site_text['a'], req, 'class')
    print(other)
