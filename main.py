from argparse import ArgumentParser
import os

import pytoml
import requests as r

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
    print("Creating new Wortex project.")
    project_name = input("Name of project? ")

    # TODO: All these tries and catches are because File IO
    # can be very, very impure.

    while os.path.exists(project_name):
        print("This folder already exists")
        project_name = input("New name of project? ")

    try:
        print("Creating project directory.")
        os.makedirs(project_name)
    except:
        print("An error occurred: {}".format(e))
        return 1

    try:
        print("Going into folder: {}".format("/" + project_name))
        os.chdir(project_name)
    except:
        return 2

    try:
        with open("Wortex.toml", "w+") as toml:
            print("Building out wortex.toml")

            toml.write("[package]\n")
            toml.write('name = "{}"\n'.format(project_name))
            # TODO: Create personal TOML file for authoring and github as well as password hashing/saving

            toml.write("\n")
            toml.write("[project]\n")
            toml.write('url = ""\n')
            toml.write("\n")
            toml.write("# Valid CMSes are Drupal, HTML, and WordPress\n")
            toml.write("# You must fill it out here in a text editor!\n")
            toml.write("\n")
            toml.write('cms = ""\n')
    except:
        return 3

    print("Success! Please go into the project directory and fill out the toml (Wortex.toml)")

@app_command("build", l=True)
def build():
    try:
        print("Attempting to open project toml...")
        with open("Wortex.toml") as toml:
            wortex_md = pytoml.loads(toml.read())
    except:
        print("Failed to open toml.")
        return 1

    project_md = wortex_md['project']
    bad_flag = False

    if project_md["url"] == '' or project_md["url"] is None:
        print("'url' in Wortex.toml must have url entered!")
        bad_flag = True
    elif project_md["cms"] == '' or project_md["cms"] is None:
        print("'cms' in Wortex.toml must has content management system entered (Wordpress, Drupal, or HTML)")
        bad_flag = True

    if bad_flag == True:
        print("An error occurred while parsing Wortex.toml: please read the error message and try again.")
    else:
        print("Wortex.toml parsed successfully: continuing to vertification process.")

    url = project_md["url"]
    cms = project_md["cms"]

    site_data = build_site_data(r.get(url))

    if site_data is None:
        print("Looks like this website is configured improperly or doesn't exist!")
        return 2

    if  cms.lower() == site_data['cms'].lower():
        print("Cms match!")
    else:
        print("Cms mismatch :-(. You entered: {}, we deduced: {}".format(cms, site_data['cms']))
