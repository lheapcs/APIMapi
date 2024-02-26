# APIMapi.py v1

import argparse
import requests
import re
from datetime import datetime
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
    main_parser.add_argument('endpoint', nargs="?", help="enter an API endpoint to interact with. The last word of the URL path will be tested. Numbers are currently ignored.")
    main_parser.add_argument("-w", "--wordlist", help="specify the location of a wordlist to fuzz with.")
    main_parser.add_argument("-o", "--output", help="output the fuzz result to the specified location.")
    main_parser.add_argument("-j", "--output_json", help="output in OpenAPI JSON format to the specified location.")
    main_parser.add_argument("-ab", "--authentication_basic", help="authenticate API calls with provided basic details (supply just the username).")
    main_parser.add_argument("-ak", "--authentication_key", help="authenticate API calls with provided API key.")

    global user_args
    user_args = main_parser.parse_args()

def status_check(code):
    if code == 200:
        print('Initial request successful.')
        return True
    else:
        print('\nInitial request to specified endpoint returning status code ' + str(code) + '.\nBe aware this may cause all fuzzing to fail. Continue?')
        continue_action = input('(y/n): ')
        if continue_action == 'y':
            return True
        else:
            raise SystemExit('Quitting application')

# Run a get request with the specified arguments to ensure the known endpoint is working.
# This should only be called once due to user_pass.
def check_request():   
    try:
        if user_args.authentication_basic:
            global user_pass 
            user_pass = getpass()
            response = requests.get(user_args.endpoint, auth=(user_args.authentication_basic, user_pass))
            return status_check(response.status_code)
        elif user_args.authentication_key:
            response = requests.get(user_args.endpoint, headers={'X-API-Key': user_args.authentication_key})
            return status_check(response.status_code)    
        else:
            response = requests.get(user_args.endpoint)
            return status_check(response.status_code)
    except requests.exceptions.RequestException as err:
        print('Endpoint specified is not in the correct format or does not exist. Request error:\n')
        raise SystemExit(err)

# Used in the actual fuzzing, GET calls based on the given endpoint.
def make_get_call(endpoint):
    try:
        if user_args.authentication_basic:
            response = requests.get(endpoint, auth=(user_args.authentication_basic, user_pass))
            print(str(response.status_code) + '  |  GET  |  ' + endpoint)
            fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code})
        elif user_args.authentication_key:
            response = requests.get(endpoint, headers={'X-API-Key': user_args.authentication_key})
            print(str(response.status_code) + '  |  GET  |  ' + endpoint)
            fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code}) 
        else:
            response = requests.get(endpoint)
            print(str(response.status_code) + '  |  GET  |  ' + endpoint)
            fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code})
    except requests.exceptions.RequestException as err:
        print(str(err) + '  |  ' + endpoint)
        fuzz_result.append({"Endpoint": endpoint, "Error": err})

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

def v_fuzz():
    # Define pattern of /v* where * is any number.
    pattern = r'(/v)(\d+)'
    match = re.search(pattern, user_args.endpoint) # Is this pattern present in the endpoint?
    
    if match:
        # Increment the v number of the URL
        def increment(match):
            version = int(match.group(2)) # Use .group to find the number part of the match defined in pattern (\d+)
            version += 1
            return match.group(1) + str(version)
        
        updated_endpoint = user_args.endpoint
        for _ in range(3):
            updated_endpoint = re.sub(pattern, increment, updated_endpoint) # Replace the number in the URL based on the increment function.
            make_get_call(updated_endpoint)

def get_fuzz():
    v_fuzz()

    pattern = re.compile(r'/([^/\d]+)(?:/\d+)?$')

    for word in wordlist:
        updated_endpoint = re.sub(pattern, '/' + word, user_args.endpoint)
        make_get_call(updated_endpoint)

# Placeholder
def post_fuzz():
    v_fuzz()
    print('POST fuzz. Got a wordlist. First word: ' + wordlist[0])

# Placeholder
def options_fuzz():
    v_fuzz()
    print('OPTIONS fuzz. Got a wordlist. First word: ' + wordlist[0])

     
# In progress  
def fuzz_handler(check_request):
    print('\nStarting fuzz at ' + str(datetime.now()) + '\n')
    global wordlist
    wordlist = create_wordlist()

    global fuzz_result
    fuzz_result = []

    get_fuzz()
    #post_fuzz()
    #options_fuzz()

    # Store the output if this argument is supplied. This will go to file at the end.

def main():
    start_main_parser()

    if not user_args.endpoint:
        print(ascii + "\nRun APIMapi with an endpoint to begin fuzzing or with the -h option to receive the full help menu.\n"
            + "\nusage: APIMapi [-h] [-w WORDLIST] [-o OUTPUT] [-j OUTPUT_JSON] [-ab AUTHENTICATION_BASIC] [-ak AUTHENTICATION_KEY] [endpoint]\n"
            )
    else:
        fuzz_handler(check_request())
    

if __name__ == "__main__":
    main()