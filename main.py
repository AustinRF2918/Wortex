from argparse import ArgumentParser
from colorama import Style
import Session.SessionManagement as sm

parser = ArgumentParser(description="Development framework for automating maintainence of small projects.")
parser.add_argument('--l', help='Load a user authenticated session.')
parser.add_argument('--d', help='Download and authenticate a session.')

args = parser.parse_args()

if (args.d != None):
    print(sm.create_sandbox(args.d))
