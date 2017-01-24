from argparse import ArgumentParser
import session.session_management as sm
from colorama import Style

parser = ArgumentParser(description="Development framework for automating maintainence of small projects.")
parser.add_argument('--l', help='Load a user authenticated session.')
parser.add_argument('--d', help='Download and authenticate a session.')

args = parser.parse_args()

if (args.d != None):
    req = sm.attempt_request(args.d)
    data = sm.build_site_data(req)
    print(data)
