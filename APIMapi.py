# APIMapi.py v1

import argparse

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
                        epilog='For more information, find the readme at https://github.com/lheapcs/APIMapi')

    # Add arguments to the parser
    main_parser.add_argument('endpoint', nargs="?", help="enter an API endpoint to interact with.")
    main_parser.add_argument("-w", "--wordlist", help="specify the location of a wordlist to fuzz with.")
    main_parser.add_argument("-o", "--output", help="output the fuzz result to the specified location.")
    main_parser.add_argument("-j", "--output_json", help="output in OpenAPI JSON format to the specified location.")
    main_parser.add_argument("-ab", "--authentication_basic", help="authenticate API calls with provided basic details; format username:password.")
    main_parser.add_argument("-ak", "--authentication_key", help="authenticate API calls with provided API key.")

    user_args = main_parser.parse_args()

    if not user_args.endpoint:
        print(ascii + "\nusage: APIMapi [-h] [-w WORDLIST] [-o OUTPUT] [-j OUTPUT_JSON] [-ab AUTHENTICATION_BASIC] [-ak AUTHENTICATION_KEY] [endpoint]\n"
            + "\nRun APIMapi with an endpoint to begin fuzzing or with the -h option to receive the full help menu.\n")

def main():
    start_main_parser()
    

if __name__ == "__main__":
    main()


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