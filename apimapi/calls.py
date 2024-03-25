import requests

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
def check_request(user_arguments, fuzz_result, user_pass, auth_header):   
    try:
        if user_arguments.authentication_basic:
            response = requests.get(user_arguments.endpoint, auth=(user_arguments.authentication_basic, user_pass))
            if fuzz_result is not None:
                fuzz_result.append({"Endpoint": user_arguments.endpoint, "Result": response.status_code, "Method": "GET"})
            return status_check(response.status_code)
        elif user_arguments.authentication_key:
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
def make_get_call(endpoint: str, type: str, user_arguments, fuzz_result, user_pass, auth_header) -> None:
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

def make_post_call(endpoint: str, user_arguments, fuzz_result, user_pass, auth_header)-> None:
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

def make_options_call(endpoint: str, user_arguments, fuzz_result, user_pass, auth_header)-> None:
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

if __name__ == "__main__":
    print('Functions only run as part of the main apimapi module.')