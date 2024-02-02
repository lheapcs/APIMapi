# APIMapi.py v1

import argparse
import requests
from getpass import getpass

ascii = """
█████╗ ██████╗ ██╗███╗   ███╗ █████╗ ██████╗ ██╗
██╔══██╗██╔══██╗██║████╗ ████║██╔══██╗██╔══██╗██║
███████║██████╔╝██║██╔████╔██║███████║██████╔╝██║
██╔══██║██╔═══╝ ██║██║╚██╔╝██║██╔══██║██╔═══╝ ██║
██║  ██║██║     ██║██║ ╚═╝ ██║██║  ██║██║     ██║
╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
"""
def start_main_parser():
    # Create the parser and set its info
    main_parser = argparse.ArgumentParser(prog='APIMapi',
                        description=  ascii +'\nMap out an API\'s attack surface from a single endpoint.',
                        formatter_class=argparse.RawDescriptionHelpFormatter,
                        epilog='For more information about using APIMapi, find the readme at https://github.com/lheapcs/APIMapi')

    # Add arguments to the parser
    main_parser.add_argument('endpoint', nargs="?", help="enter an API endpoint to interact with.")
    main_parser.add_argument("-w", "--wordlist", help="specify the location of a wordlist to fuzz with.")
    main_parser.add_argument("-o", "--output", help="output the fuzz result to the specified location.")
    main_parser.add_argument("-j", "--output_json", help="output in OpenAPI JSON format to the specified location.")
    main_parser.add_argument("-ab", "--authentication_basic", help="authenticate API calls with provided basic details; supply just the username here.")
    main_parser.add_argument("-ak", "--authentication_key", help="authenticate API calls with provided API key.")

    global user_args
    user_args = main_parser.parse_args()

    # Below is an example to help with interacting with arguments
    # Set Namespace object from argparse to a dictionary with 'vars(user_args)'
    # If we're on the endpoint arg, skip it with 'continue'
    # If the arg exists in the Namespace, print its value
    #
    #for arg in vars(user_args):
    #   if arg == 'endpoint':
    #        continue
    #    if vars(user_args)[arg]:
    #        print(vars(user_args)[arg])

# Needs refining further
# Function to log any error codes in the final result
def log_error_response(status_code):
    print(status_code)

# Needs refining further
def get_request(endpoint):
    if endpoint == 'check':
        current_endpoint = user_args.endpoint
    else:
        current_endpoint = endpoint
    
    try:
        if user_args.authentication_basic:
            global user_pass 
            user_pass == getpass() # Need a check somewhere to see if this already exists
            response = requests.get(current_endpoint, auth=(user_args.authentication_basic, user_pass))
        elif user_args.authentication_key:
            response = requests.get(current_endpoint, headers={'X-APi-Key': user_args.authentication_key})
        else:
            response = requests.get(current_endpoint)
    except requests.exceptions.RequestException as err:
        if endpoint == 'check':
            print('Request to specified endpoint not successful; fuzz cannot begin. Request error:\n')
            raise SystemExit(err)
        else:
            # Broken here, cannot access status code because this is an unsuccessful call
            log_error_response(response.status_code)
            return False
    return True

# Placeholder    
def begin_fuzz(request_test):
    if request_test:
        get_request('https://false') # Test to call without it being a check
        print('we\'re starting then')    

def main():
    start_main_parser()

    if not user_args.endpoint:
        print(ascii + "\nusage: APIMapi [-h] [-w WORDLIST] [-o OUTPUT] [-j OUTPUT_JSON] [-ab AUTHENTICATION_BASIC] [-ak AUTHENTICATION_KEY] [endpoint]\n"
            + "\nRun APIMapi with an endpoint to begin fuzzing or with the -h option to receive the full help menu.\n")
    else:
        # Start a fuzz but only if the endpoint specified is not erroring
        begin_fuzz(get_request('check')) # Specify check so we know it's not a get call for the fuzz
    

if __name__ == "__main__":
    main()