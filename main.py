from argparse import ArgumentParser
import Session.SessionManagement as sm
from colorama import Style

parser = ArgumentParser(description="Development framework for automating maintainence of small projects.")
parser.add_argument('--l', help='Load a user authenticated session.')
parser.add_argument('--d', help='Download and authenticate a session.')

args = parser.parse_args()

if (args.d != None):
    sm.create_session(args.d)

# Reset potentially changed terminal colors.
print(Style.RESET_ALL)
