import calls
import re
from datetime import datetime
from random import randint

# All fuzzing functionality.
def create_wordlist(user_arguments)-> list[str]:
    # Provide a built in wordlist if one not provided. This list is https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/api/objects-lowercase.txt
    default_wordlist = ['access-token', 'account', 'accounts', 'admin', 'amount', 'api', 'api-docs', 'apidocs', 'balance', 'balances','bio', 'bios', 'category', 'channel', 
        'chart', 'circular', 'company', 'companies', 'content', 'contract', 'coordinate', 'credentials', 'creds', 'custom', 'customer', 'customers', 
        'details', 'dir', 'directory', 'dob', 'email', 'employee', 'event', 'favorite', 'feed', 'foo', 'form', 'github', 'gmail', 'group', 'history', 'hidden', 
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
def v_fuzz(method: str, user_arguments, fuzz_result, user_pass, auth_header)-> None:
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
                'GET': lambda: calls.make_get_call(updated_endpoint, 'V Fuzz', user_arguments, fuzz_result, user_pass, auth_header),
                'POST': lambda: calls.make_post_call(updated_endpoint, user_arguments, fuzz_result, user_pass, auth_header),
                'OPTIONS': lambda: calls.make_options_call(updated_endpoint, user_arguments, fuzz_result, user_pass, auth_header)
            }
            switch.get(method, lambda: "Internal Error: Invalid HTTP Method")()

def bola_fuzz(user_arguments, fuzz_result, user_pass, auth_header)-> None:
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
            calls.make_get_call(updated_endpoint, 'BOLA', user_arguments, fuzz_result, user_pass, auth_header)
    
    else:
        print(f'No numbered object resource found in endpoint {user_arguments.endpoint}. Cannot complete BOLA check.')

def admin_fuzz(endpoint: str, user_arguments, fuzz_result, user_pass, auth_header)-> None:
    get_elements = endpoint.split('/')
    modified_urls = []

    for i in range(3, len(get_elements)):
        modified_url = '/'.join(get_elements[:i] + [user_arguments.admin_check] + get_elements[i:])
        modified_urls.append(modified_url)
    
    for url in modified_urls:
        calls.make_get_call(url, 'Admin', user_arguments, fuzz_result, user_pass, auth_header)

# Based on the method argument call the correct HTTP type.
def fuzz_sorter(method: str, user_arguments, wordlist: list[str], fuzz_result, user_pass, auth_header)-> None:
    
    def http_switch():
        switch = {
                    'GET': lambda: calls.make_get_call(updated_endpoint, 'Original', user_arguments, fuzz_result, user_pass, auth_header),
                    'POST': lambda: calls.make_post_call(updated_endpoint, user_arguments, fuzz_result, user_pass, auth_header),
                    'OPTIONS': lambda: calls.make_options_call(updated_endpoint, user_arguments, fuzz_result, user_pass, auth_header)
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
            
     
def fuzz_handler(check_request: bool, user_arguments, wordlist: list[str], fuzz_result, user_pass, auth_header)-> None:
    print(f'\nStarting fuzz at {str(datetime.now())}: \n')
    
    if user_arguments.skip is False: 
        v_fuzz('GET', user_arguments, fuzz_result, user_pass, auth_header)
        fuzz_sorter('GET', user_arguments, wordlist, fuzz_result, user_pass, auth_header)
    else:
        print("Main fuzz skipped.")

    if user_arguments.no_post is False:
        v_fuzz('POST', user_arguments, fuzz_result, user_pass, auth_header)
        calls.make_post_call(user_arguments.endpoint, user_arguments, fuzz_result, user_pass, auth_header) # See if the original endpoint takes a POST call first.
        fuzz_sorter('POST', user_arguments, wordlist, fuzz_result, user_pass, auth_header)

    if user_arguments.no_options is False:    
        v_fuzz('OPTIONS', user_arguments, fuzz_result, user_pass, auth_header)
        calls.make_options_call(user_arguments.endpoint, user_arguments, fuzz_result, user_pass, auth_header) # See if the original endpoint takes an OPTIONS call first.
        fuzz_sorter('OPTIONS', user_arguments, wordlist, fuzz_result, user_pass, auth_header)
    
    if user_arguments.bola_check:
        print('\nStarting BOLA check for original endpoint:\n')
        bola_fuzz(user_arguments, fuzz_result, user_pass, auth_header)

    if user_arguments.admin_check:
        print('\nStarting Broken Function Level Authorization check for original endpoint:\n')
        admin_fuzz(user_arguments.endpoint, user_arguments, fuzz_result, user_pass, auth_header)
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
                        admin_fuzz(result['Endpoint'], user_arguments, fuzz_result, user_pass, auth_header)

if __name__ == "__main__":
    print('Functions only run as part of the main apimapi module.')