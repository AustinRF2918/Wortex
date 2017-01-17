import re
import requests
from colorama import Fore, Back, Style
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def get_page_request(url):
    """
    Takes a url and checks both it's validity as a string and if there
    is a domain behind the host. Returns a request object in the case
    that everything goes well, otherwise a None object is returned.
    
    Parameters
    ----------
    url: string
         The url that we are authenticating and attempting to
         get a request object from.
    
    Returns
    -------
    request
        The cooresponding request object.

    """

    # URL String Validation
    logging.debug("Checking URL validity.")

    if not regex.match(url):
        logging.debug(Fore.RED + "    Error: {} is not a proper url.".format(url) + Style.RESET_ALL)
        return None
    else:
        logging.debug(Fore.GREEN + "    URL Good." + Style.RESET_ALL)

    # Check for existence
    logging.debug("Sending request to url.")

    request = requests.get(url)

    if request.status_code == 200:
        logging.debug(Fore.GREEN + "    Got response!" + Style.RESET_ALL)
        return request
    else:
        logging.debug(Fore.RED + "    Error: {} is not a proper url.".format(url) + Style.RESET_ALL)
        return None

def extract_page_metadata(response):
    """
    Takes a response object and attempts to extract various pieces
    of meta-data from it.

    Parameters
    ----------
    response: response
        Some valid response object that has been received.
    
    Returns
    -------
    string
        The CDN type of the website.

    """

    if "wp-content" in response.text:
        return "Wordpress"
    else:
        return "Unknown"

    return (cdn_type)
    

def create_sandbox(url, **kwargs):
    """
    Takes a url an attempts to create a sandbox from it: May fail in
    the case an unknown CDN is used, the URL is malformed, or other
    user specific reasons.
    
    Parameters
    ----------
    url: string
         The url that we are attempting to make a sandbox out of.
    
    debug_mode: bool (Optional)
         If we wish to display progress information.
    
    Returns
    -------
    Sandbox, None
        A new sandbox is returned in the case that everything
        went well: otherwise a None is returned and is to be
        handled by the caller.
    """


    logging.debug("Attempting to session creation for: {}".format(url))

    # Check validity of URL and create request.
    response = get_page_request(url)

    # Invalid site.
    if response is None:
        return None

    logging.debug("Attempting deduction of CDN on site content...")

    site_metadata = extract_page_metadata(response)

    if site_metadata == "Unknown":
        logging.debug(Fore.RED + "    Error: We were not able to deduce this sites type." + Style.RESET_ALL)
    else:
        logging.debug(Fore.GREEN + "    We found that this site is a {} site. Is this correct? [Y/N]".format(site_metadata))
        
