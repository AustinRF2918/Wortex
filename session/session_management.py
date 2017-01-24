import re
import requests
from colorama import Fore, Back, Style
import logging
import sys
from retrieval import info
from bs4 import BeautifulSoup

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def attempt_request(url, iteration=0):
    """
    Takes a url and checks both it's validity as a string and if there
    is a domain behind the host. Returns a request object in the case
    that everything goes well, otherwise a None object is returned.
    
    Parameters
    ----------
    url: string
         The url that we are authenticating and attempting to
         get a request object from.
    
    iteration: number
         Level of recursion: We use recursion to do various fixes
         on user level problems with writing out the URL.
    
    Returns
    -------
    Option<Response, None>
        The cooresponding response object.
    """

    if not isinstance(url, str):
        logging.debug("Passing of non-string to attempt_request: attempt_request only takes string url.")
        return None

    if iteration > 5:
        logging.debug("Level of recursion exceeded: breaking request chain.")
        return None
        
    # URL String Validation
    logging.debug("Checking URL validity. Iteration: {}".format(iteration))

    if not regex.match(url):
        if 'http://' in url:
            if iteration == 0:
                logging.debug(Fore.RED + "    Error: {} is not a proper url.".format(url) + Style.RESET_ALL)
            return None
        else:
            http_try = attempt_request('http://' + url, iteration=iteration+1)
            if http_try == None:
                if iteration == 0:
                    logging.debug(Fore.RED + "    Error: {} is not a proper url.".format(url) + Style.RESET_ALL)
                return None
            else:
                return http_try
                
    else:
        logging.debug(Fore.GREEN + "    URL Good." + Style.RESET_ALL)

    # Check for existence
    logging.debug("Sending request to url.")

    try:
        request = requests.get(url)
    except:
        logging.debug(Fore.RED + "    Error: Request to {} failed.".format(url) + Style.RESET_ALL)
        return None

    if request.status_code == 200:
        logging.debug(Fore.GREEN + "    Got response!" + Style.RESET_ALL)
        return request
    else:
        logging.debug(Fore.RED + "    Error: {} is not a proper url.".format(url) + Style.RESET_ALL)
        return None


def build_site_data(response):
    """
    Takes a response and attempts to deduce metadata from it: May fail in
    certain cases in which case a None object is returned.
    
    Parameters
    ----------
    response: Response
         The Response object that we are pulling meta-data from.
    
    Returns
    -------
    Dictionary, None
        A new dictionary is returned in the case that everything
        went well: otherwise a None is returned and is to be
        handled by the caller.
    """


    logging.debug("Attempting to build site profile from Response object.")

    # Invalid site.
    if response is None or response.status_code != 200:
        return None

    # Metadata extraction
    logging.debug("Attempting deduction of CDN on site content...")
    metadata = info.fetch_page_metadata(response)

    for key, value in metadata.items():
        if value == None:
            logging.debug(Fore.RED + "    Error: We were not able to deduce this sites {}".format(key) + Style.RESET_ALL)
            return None

    return metadata
