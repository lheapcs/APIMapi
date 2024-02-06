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
    main_parser.add_argument("-ab", "--authentication_basic", help="authenticate API calls with provided basic details (supply just the username).")
    main_parser.add_argument("-ak", "--authentication_key", help="authenticate API calls with provided API key.")

    global user_args
    user_args = main_parser.parse_args()

# Run a get request with the specified arguments to ensure the known endpoint is working.
# This should only be called once due to user_pass.
def check_request():   
    try:
        if user_args.authentication_basic:
            global user_pass 
            user_pass = getpass()
            response = requests.get(user_args.endpoint, auth=(user_args.authentication_basic, user_pass))
        elif user_args.authentication_key:
            response = requests.get(user_args.endpoint, headers={'X-API-Key': user_args.authentication_key})
        else:
            response = requests.get(user_args.endpoint)
    except requests.exceptions.RequestException as err:
        print('Request to specified endpoint not successful; fuzz cannot begin. Request error:\n')
        raise SystemExit(err)
    return True

# Placeholder
def create_wordlist():
    # If no argument, this equals a default wordlist specified here.
    # If argument, find the wordlist in the folder specified.
    return 'THE wordlist' 

# Placeholder
def get_fuzz():
    print('GET fuzz. Got a wordlist: ' + wordlist)
    if user_args.authentication_basic:
        print('Can access user pass. Password: ' + user_pass)

# Placeholder
def post_fuzz():
    print('POST fuzz. Got a wordlist: ' + wordlist)

# Placeholder
def options_fuzz():
    print('OPTIONS fuzz. Got a wordlist: ' + wordlist)

     
# Placeholder    
def fuzz_handler(check_request):
    print('Starting fuzz')
    global wordlist
    wordlist = create_wordlist()
    get_fuzz()
    post_fuzz()
    options_fuzz()
    # Store the output if this argument is supplied. This will go to file at the end.
    # Whether the above is true or not, output each fuzz attempt to the console.

def main():
    start_main_parser()

    if not user_args.endpoint:
        print(ascii + "\nRun APIMapi with an endpoint to begin fuzzing or with the -h option to receive the full help menu.\n"
            + "\nusage: APIMapi [-h] [-w WORDLIST] [-o OUTPUT] [-j OUTPUT_JSON] [-ab AUTHENTICATION_BASIC] [-ak AUTHENTICATION_KEY] [endpoint]\n"
            )
    else:
        # Start a fuzz but only if the endpoint specified is not erroring
        fuzz_handler(check_request())
    

if __name__ == "__main__":
    main()