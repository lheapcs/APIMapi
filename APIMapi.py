# APIMapi.py v1

import argparse
import requests
import re
import json
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
    main_parser.add_argument("-e", "--extended", action='store_true', help="carry out an extended fuzz where the wordlist is added to the end of the URL path rather than replacing.")
    main_parser.add_argument("-w", "--wordlist", help="specify the location of a wordlist to fuzz with.")
    main_parser.add_argument("-o", "--output", help="output the fuzz result to the specified location (For example '/Documents/fuzz_output.txt').")
    main_parser.add_argument("-j", "--output_json", help="output in OpenAPI JSON format to the specified location.")
    main_parser.add_argument("-ab", "--authentication_basic", help="authenticate API calls with provided basic details (supply just the username).")
    main_parser.add_argument("-ak", "--authentication_key", help="authenticate API calls with provided API key.")
    main_parser.add_argument("-np", "--no_post", action='store_true', help="if this flag is supplied the tests will not send POST requests.")
    main_parser.add_argument("-no", "--no_options", action='store_true', help="if this flag is supplied the tests will not send OPTIONS requests.")

    global user_args
    user_args = main_parser.parse_args()
    if user_args.endpoint:
        user_args.endpoint = user_args.endpoint.strip('/') # Remove trailing forward slash to clean URL

def status_check(code):
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
def check_request():
    if user_args.output or user_args.output_json:
        global fuzz_result
        fuzz_result = []   
    try:
        if user_args.authentication_basic:
            global user_pass 
            user_pass = getpass()
            response = requests.get(user_args.endpoint, auth=(user_args.authentication_basic, user_pass))
            try:
                fuzz_result
            except:
                pass
            else:
                fuzz_result.append({"Endpoint": user_args.endpoint, "Result": response.status_code, "Method": "GET"})
            return status_check(response.status_code)
        elif user_args.authentication_key:
            global auth_header
            auth_header = input('\nEnter API key request header name:')
            response = requests.get(user_args.endpoint, headers={auth_header: user_args.authentication_key})
            try:
                fuzz_result
            except:
                pass
            else:
                fuzz_result.append({"Endpoint": user_args.endpoint, "Result": response.status_code, "Method": "GET"})
            return status_check(response.status_code)    
        else:
            response = requests.get(user_args.endpoint)
            try:
                fuzz_result
            except:
                pass
            else:
                fuzz_result.append({"Endpoint": user_args.endpoint, "Result": response.status_code, "Method": "GET"})
            return status_check(response.status_code)
    except requests.exceptions.RequestException as err:
        print('Endpoint specified is not in the correct format or does not exist. Request error:\n')
        raise SystemExit(err)

# Used in the actual fuzzing, GET calls based on the given endpoint.
def make_get_call(endpoint):
    try:
        if user_args.authentication_basic:
            response = requests.get(endpoint, auth=(user_args.authentication_basic, user_pass))
            print(f'{str(response.status_code)}  |  GET      |  {endpoint}')
            try:
                fuzz_result
            except:
                pass
            else:
                fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "GET"})
        elif user_args.authentication_key:
            response = requests.get(endpoint, headers={auth_header: user_args.authentication_key})
            print(f'{str(response.status_code)}  |  GET      |  {endpoint}')
            try:
                fuzz_result
            except:
                pass
            else:
                fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "GET"}) 
        else:
            response = requests.get(endpoint)
            print(f'{str(response.status_code)}  |  GET      |  {endpoint}')
            try:
                fuzz_result
            except:
                pass
            else:
                fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "GET"})
    except requests.exceptions.RequestException as err:
        print(f'{str(err)}  |  GET      |  {endpoint}')
        try:
            fuzz_result
        except:
            pass
        else:
            fuzz_result.append({"Endpoint": endpoint, "Error": err, "Method": "GET"})

def make_post_call(endpoint):
    post_body = {"userId": 1, "title": "Test", "firstName": "User"} # Change this is the request body of the known endpoint is known.
    try:
        if user_args.authentication_basic:
            response = requests.post(endpoint, json=post_body, auth=(user_args.authentication_basic, user_pass))
            print(f'{str(response.status_code)}  |  POST     |  {endpoint}')
            try:
                fuzz_result
            except:
                pass
            else:
                fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "POST"})
        elif user_args.authentication_key:
            response = requests.post(endpoint, json=post_body, headers={auth_header: user_args.authentication_key})
            print(f'{str(response.status_code)}  |  POST     |  {endpoint}')
            try:
                fuzz_result
            except:
                pass
            else:
                fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "POST"}) 
        else:
            response = requests.post(endpoint, json=post_body)
            print(f'{str(response.status_code)}  |  POST     |  {endpoint}')
            try:
                fuzz_result
            except:
                pass
            else:
                fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "POST"})
    except requests.exceptions.RequestException as err:
        print(f'{str(err)}  |  POST     |  {endpoint}')
        try:
            fuzz_result
        except:
            pass
        else:
            fuzz_result.append({"Endpoint": endpoint, "Error": err, "Method": "POST"})

def make_options_call(endpoint):
    try:
        if user_args.authentication_basic:
            response = requests.options(endpoint, auth=(user_args.authentication_basic, user_pass))
            print(f'{str(response.status_code)}  |  OPTIONS  |  {endpoint}')
            try:
                fuzz_result
            except:
                pass
            else:
                fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "OPTIONS"})
        elif user_args.authentication_key:
            response = requests.options(endpoint, headers={auth_header: user_args.authentication_key})
            print(f'{str(response.status_code)}  |  OPTIONS  |  {endpoint}')
            try:
                fuzz_result
            except:
                pass
            else:
                fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "OPTIONS"}) 
        else:
            response = requests.options(endpoint)
            print(f'{str(response.status_code)}  |  OPTIONS  |  {endpoint}')
            try:
                fuzz_result
            except:
                pass
            else:
                fuzz_result.append({"Endpoint": endpoint, "Result": response.status_code, "Method": "OPTIONS"})
    except requests.exceptions.RequestException as err:
        print(f'{str(err)}  |  OPTIONS  |  {endpoint}')
        try:
            fuzz_result
        except:
            pass
        else:
            fuzz_result.append({"Endpoint": endpoint, "Error": err, "Method": "OPTIONS"})

def create_wordlist():
    # Provide a built in wordlist if one not provided. This list is https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/api/objects-lowercase.txt
    default_wordlist = ['access-token', 'account', 'accounts', 'admin', 'amount', 'balance', 'balances', 'bar', 'baz', 'bio', 'bios', 'category', 'channel', 
        'chart', 'circular', 'company', 'companies', 'content', 'contract', 'coordinate', 'credentials', 'creds', 'custom', 'customer', 'customers', 
        'details', 'dir', 'directory', 'dob', 'email', 'employee', 'event', 'favorite', 'feed', 'foo', 'form', 'github', 'gmail', 'group', 'history', 
        'image', 'info', 'item', 'job', 'link', 'links', 'location', 'locations', 'log', 'login', 'logins', 'logs', 'map', 'member', 'members', 
        'messages', 'money', 'my', 'name', 'names', 'news', 'option', 'options', 'pass', 'password', 'passwords', 'phone', 'picture', 'pin', 'post', 
        'prod', 'production', 'profile', 'profiles', 'publication', 'record', 'sale', 'sales', 'set', 'setting', 'settings', 'setup', 'site', 'swagger',
        'test', 'test1', 'theme', 'token', 'tokens', 'twitter', 'union', 'url', 'user', 'username', 'users', 'vendor', 'vendors', 'version', 'website', 
        'work']
    if not user_args.wordlist:
        return default_wordlist
    else:
        try:
            with open(user_args.wordlist, 'r') as imported_list:
                return(imported_list.read().splitlines())
        except:
            print('ERROR:\nWordlist not found. Using default.\n')
            return default_wordlist

# If endpoint has a version in it, fuzz other version numbers.
def v_fuzz(method):
    # Define pattern of /v* where * is any number.
    pattern = r'(/v)(\d+)'
    match = re.search(pattern, user_args.endpoint) # Confirm if pattern in endpoint.
    
    if match:
        # Increment the v number of the URL
        def increment(match):
            version = int(match.group(2))
            version += 1
            return match.group(1) + str(version)
        
        updated_endpoint = user_args.endpoint
        for _ in range(3):
            updated_endpoint = re.sub(pattern, increment, updated_endpoint) # Replace the number in the URL based on the increment function.
            switch = {
                'GET': lambda: make_get_call(updated_endpoint),
                'POST': lambda: make_post_call(updated_endpoint),
                'OPTIONS': lambda: make_options_call(updated_endpoint)
            }
            switch.get(method, lambda: "Internal Error: Invalid HTTP Method")()

# Based on the method argument call the correct HTTP type.
def fuzz_sorter(method):
    
    def http_switch():
        switch = {
                    'GET': lambda: make_get_call(updated_endpoint),
                    'POST': lambda: make_post_call(updated_endpoint),
                    'OPTIONS': lambda: make_options_call(updated_endpoint)
                }
        switch.get(method, lambda: "Internal Error: Invalid HTTP Method")()

    pattern = re.compile(r'/([^/\d]+)(?:/\d+)?$')
    for word in wordlist:
        updated_endpoint = re.sub(pattern, f'/{word}', user_args.endpoint)
        http_switch()

    if user_args.extended:
        for word in wordlist:
            updated_endpoint = f'{user_args.endpoint}/{word}'
            http_switch()
            
     
def fuzz_handler(check_request):
    print(f'\nStarting fuzz at {str(datetime.now())} \n')
    global wordlist
    wordlist = create_wordlist()

    v_fuzz('GET')
    fuzz_sorter('GET')

    if user_args.no_post == False:
        v_fuzz('POST')
        make_post_call(user_args.endpoint) # See if the original endpoint takes a POST call first.
        fuzz_sorter('POST')

    if user_args.no_options == False:    
        v_fuzz('OPTIONS')
        make_options_call(user_args.endpoint) # See if the original endpoint takes an OPTIONS call first.
        fuzz_sorter('OPTIONS')

def text_output_handler():
    formatted_result = []

    sorted_data = sorted(fuzz_result, key=lambda x: x['Result']) # Put in order so 200 results show first.

    for result in sorted_data:
        formatted_string = f"{result['Result']}: {result['Method']} : {result['Endpoint']}\n"
        formatted_result.append(formatted_string)

    result_string = ''.join(formatted_result)

    try:
        with open(user_args.output, 'w') as result_output:
            result_output.write(result_string)
        print(f"\nFile output successfully to {user_args.output}")    
    except:
        print("\nError creating file.")

def json_output_handler():
    filtered_data = [entry for entry in fuzz_result if 200 <= entry['Result'] <= 300] #Only keep results in the 200 response range.

    # Create start of OpenAPI structure
    json_string = {}
    json_string['openapi'] = '3.0.1'
    json_string['info'] = {'title': input('\nEnter tested API\'s name: '), 'version': 'v1'}
    json_string['servers'] = [{'url': re.sub(r'/[^/]+$', '', user_args.endpoint)}]
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
        with open(user_args.output_json, 'w') as result_output:
            json.dump(json_string, result_output)
        print(f"\nJSON file output successfully to {user_args.output_json}")    
    except:
        print("\nError creating file.")

def main():
    start_main_parser()

    if not user_args.endpoint:
        print(ascii + "\nRun APIMapi with an endpoint to begin fuzzing or with the -h option to receive the full help menu.\n"
            + "\nusage: APIMapi [-h] [-e] [-w WORDLIST] [-o OUTPUT] [-j OUTPUT_JSON] [-ab AUTHENTICATION_BASIC] [-ak AUTHENTICATION_KEY] [-np NO_POST] [-no NO_OPTIONS] [endpoint]\n"
            )
    else:
        fuzz_handler(check_request())
    
    if user_args.output:
        text_output_handler()

    if user_args.output_json:
        json_output_handler()
    
if __name__ == "__main__":
    main()