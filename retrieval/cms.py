import requests
import logging
from colorama import Fore, Back, Style

def is_wordpress_site(response):
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


    if not isinstance(response, requests.Response) or response.status_code != 200:
        logging.error("Attempted to pass faulty response to is_wordpress_site")
        return False

    if "wp-content" in response.text:
        return True
    elif "wordpress" in response.text.lower():
        return True
    else:
        return False

def is_drupal_site(response):
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

    if not isinstance(response, requests.Response) or response.status_code != 200:
        logging.error("Attempted to pass faulty response to is_drupal_site")
        return False

    if "views" in response.text and "panels" in response.text and "CCK" in response.text:
        return True
    elif "drupal" in response.text.lower():
        return True
    else:
        return False

def build_cms_classifier(response):
    """
    Takes a response and builds a classifier for what CMS it may use. Currently
    it uses a substring based method, which may be fairly slow. Later on if neccessary
    this process could be done both iteratively to provide better performance and
    with APIs, either build by ourselves or possible public that give us guarenteed
    CMS attributes.
 
    Parameters
    ----------
    response: response
        Some valid response object that has been received.
    
    Returns
    -------
    Object
        The object with numerical data and conflicts regarding our responses
        structure.
    """


    def classification_iteration(var, response, word):
        """ Simple functional method to allow quick substring search. Could be faster. Meh. """
        return var + int(word.lower() in response.text.lower())

    def perform_classification(response, substring_list):
        classification_index = 0
        # Use functools!!
        for item in substring_list:
            classification_index = classification_iteration(w, response, item)
        return classification_index
            

    wordpress_classification = perform_classification(response, ['wp-content', 'wordpress'])
    drupal_classification = perform_classification(response, ['views', 'panels', 'cck', 'drupal'])

    classification_list = [
        wordpress_classification,
        drupal_classification
    ]

    conflicts = len(list(filter(lambda x: x != 0, classification_list))) <= 1

    return {
        'classifactions': {
            'drupal_classification' : d,
            'wordpress_classification': w
        },

        'conflicts': conflicts
    }
