# APIMapi.py v1

import argparse

#Create the parser and set its info
test_parser = argparse.ArgumentParser(prog='APIMapi',
                    description='Map out an API attack surface from an endpoint',
                    epilog='Text at the bottom of help') #Needs edit

#Add arguments to the parser
test_parser.add_argument('test1')
test_parser.add_argument("-t", "--test_flag", action="store_true", help="used to test if a flag works") #If the flag is provided, set to true.
args = test_parser.parse_args()

print(args.test1)

if args.test_flag:
    print("-t flag provided")