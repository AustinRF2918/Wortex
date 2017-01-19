from bs4 import BeautifulSoup
from Retrieval import Cms
import requests
import logging
from colorama import Fore, Back, Style

def fetch_page_metadata(response):
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

    page = BeautifulSoup(response.text, "html.parser")

    # Default values: Note that we will try to be error
    # resillient, but sometimes, especially in the case
    # of cdn_type this is not possible.
    title = "Untitled Page"
    description = "No Description"

    if Cms.is_wordpress_site(response):
        logging.debug(Fore.GREEN + "    This site is a WordPress site!" + Style.RESET_ALL)
        cms_type = "Wordpress"
    elif Cms.is_drupal_site(response):
        logging.debug(Fore.GREEN + "    This site is a Drupal site!" + Style.RESET_ALL)
        cms_type = "Drupal"
    else:
        logging.debug(Fore.RED + "    CDN deduction process failed." + Style.RESET_ALL)
        cms_type = "No CMS / Unknown"

    if page.title.text is not None:
        title = page.title.text.strip()

    for desc in page.findAll(attrs={"name": "description"}):
        # A page should never have more than one description,
        # and even if it does, this works: shows the developer
        # that what he has done is probably wrong.
        description = desc['content'].strip()
        
    return {
        'cms': cms_type,
        'title': title,
        'description': description
    }

