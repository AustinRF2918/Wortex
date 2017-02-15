from argparse import ArgumentParser
from soft_retrieval.metadata_scraping import attempt_request, build_site_data
from soft_retrieval.content_scraping import run_tests
from colorama import Style

parser = ArgumentParser(description="Development framework for automating maintainence of small projects.")
parser.add_argument('--l', help='Load a user authenticated session.')
parser.add_argument('--d', help='Download and authenticate a session.')
parser.add_argument('command', help='Development test.')

cli_args = parser.parse_args()

def app_command(name, l=False):
    def commands_decorator(func):
        if cli_args.command != None and cli_args.command == name:
            func()
        elif l and cli_args.command == name[0]:
            func()
    return commands_decorator
            
@app_command("test", l=True)
def test_app():
    run_tests()

@app_command("new", l=True)
def new():
    run_tests()
