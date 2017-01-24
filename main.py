from argparse import ArgumentParser
from soft_retrieval.metadata_scraping import attempt_request, build_site_data
from colorama import Style

parser = ArgumentParser(description="Development framework for automating maintainence of small projects.")
parser.add_argument('--l', help='Load a user authenticated session.')
parser.add_argument('--d', help='Download and authenticate a session.')

args = parser.parse_args()

if (args.d != None):
    req = attempt_request(args.d)
    data = build_site_data(req)
    print("Data that was found: {}".format(data))
