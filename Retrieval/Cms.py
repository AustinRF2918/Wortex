import requests
import logging

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


    if isinstance(response, requests.Response) or response.status_code != 200:
        logging.error("Attempted to pass faulty response to is_wordpress")

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

    if isinstance(response, requests.Response) or response.status_code != 200:
        logging.error("Attempted to pass faulty response to is_drupal")

    if "views" in response.text and "panels" in response.text and "CCK" in response.text:
        return True
    elif "drupal" in response.text.lower():
        return True
    else:
        return False

