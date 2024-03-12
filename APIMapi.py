# APIMapi.py v1

import argparse
import requests
import re
import json
from datetime import datetime
from getpass import getpass
from random import randint

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
                        description=  f'{ascii}\nMap out an API\'s attack surface from a single endpoint.',
                        formatter_class=argparse.RawDescriptionHelpFormatter,
                        epilog='For more information about using APIMapi, find the readme at https://github.com/lheapcs/APIMapi')

    # Add arguments to the parser
    main_parser.add_argument('endpoint', nargs="?", help="enter an API endpoint to interact with. The last word of the URL path will be tested.")
    main_parser.add_argument("-e", "--extended", action='store_true', help="carry out an extended fuzz where the wordlist is added to the end of the URL path rather than replacing.")
    main_parser.add_argument("-w", "--wordlist", help="specify the location of a wordlist to fuzz with.")
    main_parser.add_argument("-o", "--output", help="output the fuzz result to the specified location (For example '/Documents/fuzz_output.txt').")
    main_parser.add_argument("-j", "--output_json", help="output in OpenAPI JSON format to the specified location.")
    main_parser.add_argument("-b", "--bola_check", type=int, help="check endpoint for Broken Object Level Authorization (BOLA) on numbered resource. Specify the amount of objects to check.")
    main_parser.add_argument("-r", "--random", action='store_true', help="use in conjunction with -b to check objects randomly rather than incrementally. Numbers will be within the range from 0 to 9999.")
    main_parser.add_argument("-f", "--admin_check", help="check endpoint for basic Broken Function Level Authorization. Specify the extra path to test (advised to check 'admin' as this is common).")    
    main_parser.add_argument("-ab", "--authentication_basic", help="authenticate API calls with provided basic details. Supply just the username.")
    main_parser.add_argument("-ak", "--authentication_key", help="authenticate API calls with provided API key.")
    main_parser.add_argument("-np", "--no_post", action='store_true', help="if this flag is supplied the tests will not send POST requests.")
    main_parser.add_argument("-no", "--no_options", action='store_true', help="if this flag is supplied the tests will not send OPTIONS requests.")

    user_args = main_parser.parse_args()
    if user_args.endpoint:
        user_args.endpoint = user_args.endpoint.strip('/') # Remove trailing forward slash to clean URL

    return user_args

def init_fuzz_result(user_arguments):
    if user_arguments.output or user_arguments.output_json or user_arguments.admin_check:
        return []
    return None

def status_check(code: int) -> bool:
    if code in range(200, 300):
        print('Initial request successful.')
        return True
    else:
        print(f'\nInitial request to specified endpoint returning status code {str(code)}.\nBe aware this may cause all fuzzing to fail. Continue?')
        continue_action = input('(y/n): ')
        if continue_action == 'y':
            return True
        else:
            raise SystemExit('Quitting application')

# Run a get request with the specified arguments to ensure the known endpoint is working.
# This should only be called once due to user_pass.
def check_request(user_arguments, fuzz_result):   
    try:
        if user_arguments.authentication_basic:
            global user_pass 
            user_pass = getpass()
            response = requests.get(user_arguments.endpoint, auth=(user_arguments.authentication_basic, user_pass))
            if fuzz_result is not None:
                fuzz_result.append({"Endpoint": user_arguments.endpoint, "Result": response.status_code, "Method": "GET"})
            return status_check(response.status_code)
        elif user_arguments.authentication_key:
            global auth_header
            auth_header = input('\nEnter API key request header name:')
            response = requests.get(user_arguments.endpoint, headers={auth_header: user_arguments.authentication_key})
            if fuzz_result is not None:
                fuzz_result.append({"Endpoint": user_arguments.endpoint, "Result": response.status_code, "Method": "GET"})
            return status_check(response.status_code)    
        else:
            response = requests.get(user_arguments.endpoint)
            if fuzz_result is not None:
                fuzz_result.append({"Endpoint": user_arguments.endpoint, "Result": response.status_code, "Method": "GET"})
            return status_check(response.status_code)
    except requests.exceptions.RequestException as err:
        print('Endpoint specified is not in the correct format or does not exist. Request error:\n')
        raise SystemExit(err)

# Used in the actual fuzzing, GET calls based on the given endpoint.
def make_get_call(endpoint: str, type: str, user_arguments, fuzz_result) -> None:
    try:
        if user_arguments.authentication_basic:
            response = requests.get(endpoint, auth=(user_arguments.authentication_basic, user_pass))
            print(f'{str(response.status_code)}  |  GET      |  {endpoint}')
            if fuzz_result is not None:
                fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "GET", "Type": type})
        elif user_arguments.authentication_key:
            response = requests.get(endpoint, headers={auth_header: user_arguments.authentication_key})
            print(f'{str(response.status_code)}  |  GET      |  {endpoint}')
            if fuzz_result is not None:
                fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "GET", "Type": type}) 
        else:
            response = requests.get(endpoint)
            print(f'{str(response.status_code)}  |  GET      |  {endpoint}')
            if fuzz_result is not None:
                fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "GET", "Type": type})
    except requests.exceptions.RequestException as err:
        print(f'{str(err)}  |  GET      |  {endpoint}')
        if fuzz_result is not None:
                fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "GET", "Type": type})

def make_post_call(endpoint: str, user_arguments, fuzz_result)-> None:
    post_body = {"userId": 1, "title": "Test", "firstName": "User"} # Change this is the request body of the known endpoint is known.
    try:
        if user_arguments.authentication_basic:
            response = requests.post(endpoint, json=post_body, auth=(user_arguments.authentication_basic, user_pass))
            print(f'{str(response.status_code)}  |  POST     |  {endpoint}')
            if fuzz_result is not None:
                fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "POST"})
        elif user_arguments.authentication_key:
            response = requests.post(endpoint, json=post_body, headers={auth_header: user_arguments.authentication_key})
            print(f'{str(response.status_code)}  |  POST     |  {endpoint}')
            if fuzz_result is not None:
                fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "POST"})
        else:
            response = requests.post(endpoint, json=post_body)
            print(f'{str(response.status_code)}  |  POST     |  {endpoint}')
            if fuzz_result is not None:
                fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "POST"})
    except requests.exceptions.RequestException as err:
        print(f'{str(err)}  |  POST     |  {endpoint}')
        if fuzz_result is not None:
            fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "POST"})

def make_options_call(endpoint: str, user_arguments, fuzz_result)-> None:
    try:
        if user_arguments.authentication_basic:
            response = requests.options(endpoint, auth=(user_arguments.authentication_basic, user_pass))
            print(f'{str(response.status_code)}  |  OPTIONS  |  {endpoint}')
            if fuzz_result is not None:
                fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "OPTIONS"})
        elif user_arguments.authentication_key:
            response = requests.options(endpoint, headers={auth_header: user_arguments.authentication_key})
            print(f'{str(response.status_code)}  |  OPTIONS  |  {endpoint}')
            if fuzz_result is not None:
                fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "OPTIONS"})
        else:
            response = requests.options(endpoint)
            print(f'{str(response.status_code)}  |  OPTIONS  |  {endpoint}')
            if fuzz_result is not None:
                fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "OPTIONS"})
    except requests.exceptions.RequestException as err:
        print(f'{str(err)}  |  OPTIONS  |  {endpoint}')
        if fuzz_result is not None:
            fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "OPTIONS"})

def create_wordlist(user_arguments)-> list[str]:
    # Provide a built in wordlist if one not provided. This list is https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/api/objects-lowercase.txt
    default_wordlist = ['access-token', 'account', 'accounts', 'admin', 'amount', 'balance', 'balances', 'bar', 'baz', 'bio', 'bios', 'category', 'channel', 
        'chart', 'circular', 'company', 'companies', 'content', 'contract', 'coordinate', 'credentials', 'creds', 'custom', 'customer', 'customers', 
        'details', 'dir', 'directory', 'dob', 'email', 'employee', 'event', 'favorite', 'feed', 'foo', 'form', 'github', 'gmail', 'group', 'history', 
        'image', 'info', 'item', 'job', 'link', 'links', 'location', 'locations', 'log', 'login', 'logins', 'logs', 'map', 'member', 'members', 
        'messages', 'money', 'my', 'name', 'names', 'news', 'option', 'options', 'pass', 'password', 'passwords', 'phone', 'picture', 'pin', 'post', 
        'prod', 'production', 'profile', 'profiles', 'publication', 'record', 'sale', 'sales', 'set', 'setting', 'settings', 'setup', 'site', 'swagger',
        'test', 'test1', 'theme', 'token', 'tokens', 'twitter', 'union', 'url', 'user', 'username', 'users', 'vendor', 'vendors', 'version', 'website', 
        'work']
    if not user_arguments.wordlist:
        return default_wordlist
    else:
        try:
            with open(user_arguments.wordlist, 'r') as imported_list:
                return(imported_list.read().splitlines())
        except Exception as e:
            print(f'\n{e}\nUsing default wordlist.\n')
            return default_wordlist

# If endpoint has a version in it, fuzz other version numbers.
def v_fuzz(method: str, user_arguments, fuzz_result)-> None:
    # Define pattern of /v* where * is any number.
    pattern = r'(/v)(\d+)'
    match = re.search(pattern, user_arguments.endpoint) # Confirm if pattern in endpoint.
    
    if match:
        # Increment the v number of the URL
        def increment(match):
            version = int(match.group(2))
            version += 1
            return match.group(1) + str(version)
        
        updated_endpoint = user_arguments.endpoint
        for _ in range(3):
            updated_endpoint = re.sub(pattern, increment, updated_endpoint) # Replace the number in the URL based on the increment function.
            switch = {
                'GET': lambda: make_get_call(updated_endpoint, 'V Fuzz', user_arguments, fuzz_result),
                'POST': lambda: make_post_call(updated_endpoint, user_arguments, fuzz_result),
                'OPTIONS': lambda: make_options_call(updated_endpoint, user_arguments, fuzz_result)
            }
            switch.get(method, lambda: "Internal Error: Invalid HTTP Method")()

def bola_fuzz(user_arguments, fuzz_result)-> None:
    # Define pattern of any numbers in between slashes, ignoring letters.
    pattern = r'(?<=/)\d+(?![a-zA-Z])'
    match = re.search(pattern, user_arguments.endpoint)

    if match:
        def generate_number(match):
            version = int(match.group(0))
            if user_arguments.random:
                new_number = randint(0, 9999)
                while new_number in used_numbers: # Used to not repeat random numbers.
                    new_number = randint(0, 9999)
                used_numbers.add(new_number)
                version = new_number
            else:    
                version += 1
            return str(version)
        
        updated_endpoint = user_arguments.endpoint
        if user_arguments.random:
            used_numbers = set()

        for _ in range(user_arguments.bola_check):
            updated_endpoint = re.sub(pattern, generate_number, updated_endpoint)
            make_get_call(updated_endpoint, 'BOLA', user_arguments, fuzz_result)
    
    else:
        print(f'No numbered object resource found in endpoint {user_arguments.endpoint}. Cannot complete BOLA check.')

def admin_fuzz(endpoint: str, user_arguments, fuzz_result)-> None:
    get_elements = endpoint.split('/')
    modified_urls = []

    for i in range(3, len(get_elements)):
        modified_url = '/'.join(get_elements[:i] + [user_arguments.admin_check] + get_elements[i:])
        modified_urls.append(modified_url)
    
    for url in modified_urls:
        make_get_call(url, 'Admin', user_arguments, fuzz_result)

# Based on the method argument call the correct HTTP type.
def fuzz_sorter(method: str, user_arguments, wordlist: list[str], fuzz_result)-> None:
    
    def http_switch():
        switch = {
                    'GET': lambda: make_get_call(updated_endpoint, 'Original', user_arguments, fuzz_result),
                    'POST': lambda: make_post_call(updated_endpoint, user_arguments, fuzz_result),
                    'OPTIONS': lambda: make_options_call(updated_endpoint, user_arguments, fuzz_result)
                }
        switch.get(method, lambda: "Internal Error: Invalid HTTP Method")()

    pattern = re.compile(r'/([^/\d]+)(?:/\d+)?$')
    for word in wordlist:
        updated_endpoint = re.sub(pattern, f'/{word}', user_arguments.endpoint)
        http_switch()

    if user_arguments.extended:
        for word in wordlist:
            updated_endpoint = f'{user_arguments.endpoint}/{word}'
            http_switch()
            
     
def fuzz_handler(check_request: bool, user_arguments, wordlist: list[str], fuzz_result)-> None:
    print(f'\nStarting fuzz at {str(datetime.now())}: \n')
    
    v_fuzz('GET', user_arguments, fuzz_result)
    fuzz_sorter('GET', user_arguments, wordlist, fuzz_result)

    if user_arguments.no_post is False:
        v_fuzz('POST', user_arguments, fuzz_result)
        make_post_call(user_arguments.endpoint, user_arguments, fuzz_result) # See if the original endpoint takes a POST call first.
        fuzz_sorter('POST', user_arguments, wordlist, fuzz_result)

    if user_arguments.no_options is False:    
        v_fuzz('OPTIONS', user_arguments, fuzz_result)
        make_options_call(user_arguments.endpoint, user_arguments, fuzz_result) # See if the original endpoint takes an OPTIONS call first.
        fuzz_sorter('OPTIONS', user_arguments, wordlist, fuzz_result)
    
    if user_arguments.bola_check:
        print('\nStarting BOLA check for original endpoint:\n')
        bola_fuzz(user_arguments, fuzz_result)

    if user_arguments.admin_check:
        print('\nStarting Broken Function Level Authorization check for original endpoint:\n')
        admin_fuzz(user_arguments.endpoint, user_arguments, fuzz_result)
        print(f'\nAttempt the same test on all successful results from the original fuzz?\n')
        continue_action = input('(y/n): ')
        if continue_action == 'y':
            for result in fuzz_result:
                try:
                    result['Type']
                except:
                    pass
                else:
                    if result['Type'] == 'Original':
                        admin_fuzz(result['Endpoint'], user_arguments, fuzz_result)

# Output fuzz result to text.
def text_output_handler(user_arguments, fuzz_result)-> None:
    formatted_result = []

    sorted_data = sorted(fuzz_result, key=lambda x: x['Result']) # Put in order so 200 results show first.

    for result in sorted_data:
        formatted_string = f"{result['Result']}: {result['Method']} : {result['Endpoint']}\n"
        formatted_result.append(formatted_string)

    result_string = ''.join(formatted_result)

    try:
        with open(user_arguments.output, 'w') as result_output:
            result_output.write(result_string)
        print(f"\nFile output successfully to {user_arguments.output}")    
    except Exception as e:
        print(f"\n{e}")

# Output fuzz result to JSON in OpenAPI format.
def json_output_handler(user_arguments, fuzz_result)-> None:
    filtered_data = [entry for entry in fuzz_result if 200 <= entry['Result'] <= 300] #Only keep results in the 200 response range.

    # Create start of OpenAPI structure
    json_string = {}
    json_string['openapi'] = '3.0.1'
    json_string['info'] = {'title': input('\nEnter tested API\'s name: '), 'version': 'v1'}
    json_string['servers'] = [{'url': re.sub(r'/[^/]+$', '', user_arguments.endpoint)}]
    json_string['paths'] = {}

    # Finish OpenAPI based on 200 results.
    for result in filtered_data:
        pattern = re.compile(r'/([^/\d]+)(?:/\d+)?$')
        keyword = re.search(pattern, result['Endpoint']).group(1)

        try: 
            json_string['paths'][f'/{keyword}']
        except: 
            json_string['paths'][f'/{keyword}'] = {f"{result['Method'].lower()}" : {'tags': [f'{keyword}'], 'responses': {f"{result['Result']}": {'description': 'Success'}}}}   
        else:
            json_string['paths'][f'/{keyword}'][f"{result['Method'].lower()}"] = {'tags': [f'{keyword}'], 'responses': {f"{result['Result']}": {'description': 'Success'}}}

    # Write to file.
    try:
        with open(user_arguments.output_json, 'w') as result_output:
            json.dump(json_string, result_output)
        print(f"\nJSON file output successfully to {user_arguments.output_json}")    
    except Exception as e:
        print(f"\n{e}")

def main():
    user_arguments = start_main_parser()
    fuzz_result = init_fuzz_result(user_arguments)

    if not user_arguments.endpoint:
        raise SystemExit(f'{ascii}\nRun APIMapi with an endpoint to begin fuzzing or with the -h option to receive the full help menu.\n\nusage: APIMapi [-h] [-e] [-w WORDLIST] [-o OUTPUT] [-j OUTPUT_JSON] [-b BOLA_CHECK] [-r] [-f] [-ab AUTHENTICATION_BASIC] [-ak AUTHENTICATION_KEY] [-np NO_POST] [-no NO_OPTIONS] [endpoint]\n')
    else:
        wordlist = create_wordlist(user_arguments)
        fuzz_handler(check_request(user_arguments, fuzz_result), user_arguments, wordlist, fuzz_result)
    
    if user_arguments.output:
        text_output_handler(user_arguments, fuzz_result)

    if user_arguments.output_json:
        json_output_handler(user_arguments, fuzz_result)
    
if __name__ == "__main__":
    main()