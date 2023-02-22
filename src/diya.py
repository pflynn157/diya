#!/usr/bin/python3
# Run with (from output): python3 -m  http.server 8000
import os
import sys
import shutil
from sys import argv
from http.server import HTTPServer, SimpleHTTPRequestHandler
from contextlib import contextmanager

from creator import new_website

# Make sure we can find the config file
sys.path.append(os.getcwd())

##
## Entry point for the website generator
##
def build_website(use_base = False):
    # Import what we need
    import config
    import processor
    
    # Verify the config module
    if not hasattr(config, "name"):
        print("Error: No website name specified.")
        exit(1)
    
    if not hasattr(config, "custom_links"):
        config.custom_links = list()
    
    if not hasattr(config, "output"):
        config.output = "./output"
    
    if not hasattr(config, "base"):
        config.base = "./base"
    
    if not hasattr(config, "pages"):
        config.pages = "./data/pages"
    
    if not hasattr(config, "posts"):
        config.posts = "./data/posts"
    
    # If the user wants to use the base files, import those
    if use_base:
        shutil.copytree("/usr/share/diya/base", "./base", dirs_exist_ok=True)
    
    # Run the generator
    processor.copy_raw_contents()
    processor.processor_main()

##
## Runs a simple web server for testing
##
@contextmanager
def run_server():
    import config
    print("Running web server for testing...")
    print("Press Ctrl-C to terminate.")
    print("")
    os.chdir(config.output)
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()
    
##
## Prints help and version information
##
def help():
    print("Diya Website Generator")
    print("")
    print("Valid options: diya [options]")
    print("\t-h, --help\t Print this message and exit.")
    print("\t-v, --version\t Print version information and exit.")
    print("\t-s, --serve\t Create a simple HTTP server for testing.")
    print("If no options are provided, the generator will run in the base directory.")
    print("")

def version():
    print("Diya Website Generator")
    print("Version 1.0.0")
    print("The Diya Generator was written by Patrick Flynn.")
    print("See <patrickflynn.xyz> for more information.")
    print("")
    
##
## Process command line arguments, and decide what to do
##
if len(argv) == 1:
    build_website()
    exit(0)

use_base = False

for i in range(1, len(argv)):
    arg = argv[i]
    if arg == "--help" or arg == "-h":
        help()
        exit()
    elif arg == "--version" or arg == "-v":
        version()
        exit()
    elif arg == "--serve" or arg == "-s":
        run_server()
        exit()
    elif arg == "--new" or arg == "-n":
        new_website()
        exit()
    elif arg == "--use-base" or arg == "-ub":
        use_base = True
    else:
        print("Invalid option: " + arg)
        exit(1)

build_website(use_base)

