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
    def classification_iteration(var, response, word):
        if word.lower() in response.text.lower():
            return var + 1
        else:
            return var

    w = 0
    w = classification_iteration(w, response, 'wp-content')
    w = classification_iteration(w, response, 'wordpress')

    d = 0
    d = classification_iteration(w, response, 'views')
    d = classification_iteration(w, response, 'panels')
    d = classification_iteration(w, response, 'cck')
    d = classification_iteration(w, response, 'drupal')

    conflicts = False

    if w != 0 and d != 0 or w == 0 and d == 0:
        conflicts = True
        

    return {
        'classifactions': {
            'drupal_classification' : d,
            'wordpress_classification': w
        },

        'conflicts': conflicts
    }
