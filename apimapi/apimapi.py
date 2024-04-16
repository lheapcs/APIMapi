import argparse
import results
import fuzzing
import calls
import authentication

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
    main_parser.add_argument("-s", "--skip", action='store_true', help="skip the main fuzz and only complete other specified checks. -b or -f should be specified if using this option.")
    main_parser.add_argument("-w", "--wordlist", help="specify the location of a wordlist to fuzz with.")
    main_parser.add_argument("-o", "--output", help="output the fuzz result to the specified location (For example '/Documents/fuzz_output.txt').")
    main_parser.add_argument("-j", "--output_json", help="output in OpenAPI JSON format to the specified location.")
    main_parser.add_argument("-b", "--bola_check", type=int, help="test endpoint for Broken Object Level Authorization (BOLA) on numbered resource. Specify the amount of objects to check.")
    main_parser.add_argument("-r", "--random", action='store_true', help="use in conjunction with -b to check objects randomly rather than incrementally. Numbers will be within the range from 0 to 9999.")
    main_parser.add_argument("-f", "--admin_check", help="test endpoint for basic Broken Function Level Authorization. Specify the extra path to test (advised to check 'admin' as this is common).")
    main_parser.add_argument("-l", "--rate_limit_check", type=int, help="test endpoint for a possible unrestricted resource consumption vulnerability. Specify the number of calls to make, which will be multiplied by ten.")     
    main_parser.add_argument("-ab", "--authentication_basic", help="authenticate API calls with provided basic details. Supply just the username.")
    main_parser.add_argument("-ak", "--authentication_key", help="authenticate API calls with provided API key.")
    main_parser.add_argument("-at", "--authentication_check", action='store_true', help="test for potential broken authentication on found endpoints. All endpoints will be called with no authentication to see if they allow access. Should only be used in conjunction with -ab or -ak.")
    main_parser.add_argument("-np", "--no_post", action='store_true', help="if this flag is supplied the tests will not send POST requests.")
    main_parser.add_argument("-no", "--no_options", action='store_true', help="if this flag is supplied the tests will not send OPTIONS requests.")

    user_args = main_parser.parse_args()
    if user_args.endpoint:
        user_args.endpoint = user_args.endpoint.strip('/') # Remove trailing forward slash to clean URL

    return user_args

def main():
    user_arguments = start_main_parser()
    if not user_arguments.endpoint:
        raise SystemExit(f'{ascii}\nRun APIMapi with an endpoint to begin fuzzing or with the -h option to receive the full help menu.\n\nusage: APIMapi [-h] [-e] [-s] [-w WORDLIST] [-o OUTPUT] [-j OUTPUT_JSON] [-b BOLA_CHECK] [-r] [-f ADMIN_CHECK] [-l RATE_LIMIT_CHECK] [-ab AUTHENTICATION_BASIC] [-ak AUTHENTICATION_KEY] [-at] [-np] [-no] [endpoint]\n')
    
    fuzz_result = results.init_fuzz_result(user_arguments)
    wordlist = fuzzing.create_wordlist(user_arguments)

    user_pass = authentication.handle_basic(user_arguments)
    auth_header = authentication.handle_key(user_arguments) 

    fuzzing.fuzz_handler(calls.check_request(user_arguments, fuzz_result, user_pass, auth_header), user_arguments, wordlist, fuzz_result, user_pass, auth_header)
    
    if user_arguments.output:
        results.text_output_handler(user_arguments, fuzz_result)

    if user_arguments.output_json:
        results.json_output_handler(user_arguments, fuzz_result)
    
if __name__ == "__main__":
    main()