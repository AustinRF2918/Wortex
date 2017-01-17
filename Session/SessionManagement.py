import re
import requests
from colorama import Fore, Back, Style

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def authenticate_url(url):
    # URL String Validation
    print("Checking URL validity.")

    if not regex.match(url):
        print(Fore.RED + "    Error: {} is not a proper url.".format(url) + Style.RESET_ALL)
        return None
    else:
        print(Fore.GREEN + "    URL Good." + Style.RESET_ALL)

    # Check for existence
    print("Sending request to url.")

    request = requests.get(url)

    if request.status_code == 200:
        print(Fore.GREEN + "    Got response!" + Style.RESET_ALL)
        return request
    else:
        print(Fore.RED + "    Error: {} is not a proper url.".format(url) + Style.RESET_ALL)
        return None

def extract_metadata(response):
    def deduce_cdn(response):
        if "wp-content" in response.text:
            return "Wordpress"
        else:
            return "Unknown"

    cdn_type = deduce_cdn(response)

    return (cdn_type)
    

def create_session(url):
    print("Attempting to session creation for: {}".format(url))

    response = authenticate_url(url)

    if response is None:
        return None

    print("Attempting deduction of CDN on site content...")
    site_metadata = extract_metadata(response)

    if site_metadata == "Unknown":
        print(Fore.RED + "    Error: We were not able to deduce this sites type." + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "    We found that this site is a {} site. Is this correct? [Y/N]".format(site_metadata))
        
