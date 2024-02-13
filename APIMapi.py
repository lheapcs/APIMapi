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

def create_wordlist():
    # Provide a built in wordlist if one not provided. This list is https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/api/objects-lowercase.txt
    if not user_args.wordlist:
        return ['access-token', 'account', 'accounts', 'admin', 'amount', 'balance', 'balances', 'bar', 'baz', 'bio', 'bios', 'category', 'channel', 
                'chart', 'circular', 'company', 'companies', 'content', 'contract', 'coordinate', 'credentials', 'creds', 'custom', 'customer', 'customers', 
                'details', 'dir', 'directory', 'dob', 'email', 'employee', 'event', 'favorite', 'feed', 'foo', 'form', 'github', 'gmail', 'group', 'history', 
                'image', 'info', 'item', 'job', 'link', 'links', 'location', 'locations', 'log', 'login', 'logins', 'logs', 'map', 'member', 'members', 
                'messages', 'money', 'my', 'name', 'names', 'news', 'option', 'options', 'pass', 'password', 'passwords', 'phone', 'picture', 'pin', 'post', 
                'prod', 'production', 'profile', 'profiles', 'publication', 'record', 'sale', 'sales', 'set', 'setting', 'settings', 'setup', 'site', 'swagger',
                'test', 'test1', 'theme', 'token', 'tokens', 'twitter', 'union', 'url', 'user', 'username', 'users', 'vendor', 'vendors', 'version', 'website', 
                'work']
    else:
        try:
            with open(user_args.wordlist, 'r') as imported_list:
                return(imported_list.read().splitlines())
        except:
            print('ERROR:\nWordlist not found.\n')

# Placeholder
def get_fuzz():
    print('GET fuzz. Got a wordlist. First word: ' + wordlist[0])
    if user_args.authentication_basic:
        print('Can access user pass. Password: ' + user_pass)

# Placeholder
def post_fuzz():
    print('POST fuzz. Got a wordlist. First word: ' + wordlist[0])

# Placeholder
def options_fuzz():
    print('OPTIONS fuzz. Got a wordlist. First word: ' + wordlist[0])

     
# In progress  
def fuzz_handler(check_request):
    print('Initial request successful.\nBegining fuzz:\n')
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