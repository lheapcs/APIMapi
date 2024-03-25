from getpass import getpass

def handle_basic(user_arguments):
    if user_arguments.authentication_basic:
        return getpass()
    return None

def handle_key(user_arguments):
    if user_arguments.authentication_key:
        return input('\nEnter API key request header name:')
    return None

if __name__ == "__main__":
    print('Functions only run as part of the main apimapi module.')