# APIMapi.py v1

import argparse

# Create the parser and set its info
main_parser = argparse.ArgumentParser(prog='APIMapi',
                    description='Map out an API\'s attack surface from a single endpoint.',
                    epilog='Text at the bottom of help') #Needs edit

# Add arguments to the parser
# apimapi                                                       | run without any arguments, get ASCII art and small guide
# apimapi https://endpoint.co.uk                                | begin fuzz of endpoint with no authentication, with default wordlist
# apimapi https://endpoint.co.uk  -w /home/wordlists/thislist   | begin fuzz with specified wordlist
# apimapi https://endpoint.co.uk  -ab username:password         | begin fuzz with basic auth specified 
# apimapi https://endpoint.co.uk  -ak asldkhweuf                | begin fuzz with API key specified 
# apimapi https://endpoint.co.uk  -o /home/usr                  | begin fuzz and output result to specified location
# apimapi https://endpoint.co.uk  -d /home/usr                  | output to JSON file twith OpenAPI format
main_parser.add_argument('Endpoint')
main_parser.add_argument("-w", "--wordlist", help="Specify the location of a wordlist to fuzz with.")
main_parser.add_argument("-o", "--output", help="Output the fuzz result to the specified location.")
main_parser.add_argument("-j", "--output_json", help="Create OpenAPI JSON based on the fuzz result to the specified location.")
main_parser.add_argument("-ab", "--authentication_basic", help="Authenticate API calls with provided basic details; format username:password.")
main_parser.add_argument("-ak", "--authentication_key", help="Authenticate API calls with provided API key.")


user_args = main_parser.parse_args()

# Set Namespace object from argparse to a dictionary with 'vars(user_args)'
# If we're on the endpoint arg, skip it with 'continue'
# If the arg exists in the Namespace, print its value
for arg in vars(user_args):
    if arg == 'Endpoint':
        continue
    if vars(user_args)[arg]:
        print(vars(user_args)[arg])