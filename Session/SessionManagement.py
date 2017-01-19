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

def get_page_response(url, iteration=0):
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
            http_try = get_page_response('http://' + url, iteration=iteration+1)
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


def is_wordpress(response):
    """
    Uses multiple features of the response object that has been returned to
    check if a website has the features of being WordPress compatable.
 
    Parameters
    ----------
    response: response
        Some valid response object that has been received.
    
    Returns
    -------
    Bool
        If the response object looks like it is probably a WordPress site.

    """


    if isinstance(response, requests.Response) or response.status_code != 200:
        logging.error("Attempted to pass faulty response to is_wordpress")

    if "wp-content" in response.text:
        return True
    elif "wordpress" in response.text.lower():
        return True
    else:
        return False

def is_drupal(response):
    """
    Uses multiple features of the response object that has been returned to
    check if a website has the features of being WordPress compatable.
 
    Parameters
    ----------
    response: response
        Some valid response object that has been received.
    
    Returns
    -------
    Bool
        If the response object looks like it is probably a WordPress site.

    """

    if isinstance(response, requests.Response) or response.status_code != 200:
        logging.error("Attempted to pass faulty response to is_drupal")

    if "views" in response.text and "panels" in response.text and "CCK" in response.text:
        return True
    elif "drupal" in response.text.lower():
        return True
    else:
        return False

def get_page_metadata(response):
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

    if not isinstance(response, requests.Response):
        logging.debug("Passing of non-response to get_page_metadata: create_sandbox only takes Response object.")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Default values: Note that we will try to be error
    # resillient, but sometimes, especially in the case
    # of cdn_type this is not possible.
    title = "Untitled Page"
    description = "No Description"

    if is_wordpress(response):
        logging.debug(Fore.GREEN + "    This site is a WordPress site!" + Style.RESET_ALL)
        cdn_type = "Wordpress"
    elif is_drupal(response):
        logging.debug(Fore.GREEN + "    This site is a Drupal site!" + Style.RESET_ALL)
        cdn_type = "Drupal"
    else:
        logging.debug(Fore.RED + "    CDN deduction process failed." + Style.RESET_ALL)
        cdn_type = "No CDN / Unknown"

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
    response = get_page_response(url)

    # Invalid site.
    if response is None:
        return None

    # Metadata extraction
    logging.debug("Attempting deduction of CDN on site content...")
    sandbox_metadata = get_page_metadata(response)

    for key, value in sandbox_metadata.items():
        if value == None:
            logging.debug(Fore.RED + "    Error: We were not able to deduce this sites {}".format(key) + Style.RESET_ALL)
            return None

    return sandbox_metadata
