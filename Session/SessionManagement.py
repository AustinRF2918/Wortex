import re
import requests
from colorama import Fore, Back, Style
import logging
import sys
from bs4 import BeautifulSoup

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

    if not isinstance(response, requests.Response):
        logging.debug("Passing of non-response to extract_page_metadata: create_sandbox only takes Response object.")
        return None

    """
    Takes a response object and attempts to extract various pieces
    of meta-data from it.

    Parameters
    ----------
    response: response
        Some valid response object that has been received.
    
    Returns
    -------
    Option<String, None>
        The CDN type of the website or potentially none.


    """

    soup = BeautifulSoup(response.text, "html.parser")

    # Default values: Note that we will try to be error
    # resillient, but sometimes, especially in the case
    # of cdn_type this is not possible.
    cdn_type = None
    title = "Untitled Page"
    description = "No Description"

    if "wp-content" in response.text:
        logging.debug(Fore.GREEN + "    This site is a WordPress site!" + Style.RESET_ALL)
        cdn_type = "Wordpress"

    if soup.title.text is not None:
        title = soup.title.text.strip()

    for desc in soup.findAll(attrs={"name": "description"}):
        # A page should never have more than one description,
        # and even if it does, this works: shows the developer
        # that what he has done is probably wrong.
        description = desc['content'].strip()
        
    return {
        'CDN': cdn_type,
        'Title': title,
        'Description': description
    }

def create_sandbox(url):
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

    if not isinstance(url, str):
        logging.debug("Passing of non-string to create_sandbox: create_sandbox only takes string url.")
        return None

    logging.debug("Attempting to session creation for: {}".format(url))

    # Check validity of URL and create request.
    response = get_page_request(url)

    # Invalid site.
    if response is None:
        return None

    # Metadata extraction
    logging.debug("Attempting deduction of CDN on site content...")
    sandbox_metadata = extract_page_metadata(response)

    for key, value in sandbox_metadata.items():
        if value == None:
            logging.debug(Fore.RED + "    Error: We were not able to deduce this sites {}".format(key) + Style.RESET_ALL)
            return None

    return sandbox_metadata
