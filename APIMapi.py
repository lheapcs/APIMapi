# APIMapi.py v1

import argparse
import requests

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
    main_parser.add_argument("-ab", "--authentication_basic", help="authenticate API calls with provided basic details; format username:password.")
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
def test_endpoint(endpoint):
    # Need checks in here for specified options such as auth before carrying this out
    try:
        response = requests.get(endpoint)
    except requests.exceptions.RequestException as err:
        print('Request to specified endpoint not successful; fuzz cannot begin. Request error:\n')
        raise SystemExit(err)
    # response.json() will give the full response body
    # 'if response.status_code == 200:' not using this for now but may be handy in future
    return True

# Placeholder    
def begin_fuzz(request_test):
    if request_test:
        print('we\'re starting then')    

def main():
    start_main_parser()

    if not user_args.endpoint:
        print(ascii + "\nusage: APIMapi [-h] [-w WORDLIST] [-o OUTPUT] [-j OUTPUT_JSON] [-ab AUTHENTICATION_BASIC] [-ak AUTHENTICATION_KEY] [endpoint]\n"
            + "\nRun APIMapi with an endpoint to begin fuzzing or with the -h option to receive the full help menu.\n")
    else:
        # Start a fuzz but only if the endpoint specified is not erroring
        begin_fuzz(test_endpoint(user_args.endpoint)) 
    

if __name__ == "__main__":
    main()