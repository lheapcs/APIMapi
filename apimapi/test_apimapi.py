import unittest
import fuzzing
import authentication
from argparse import Namespace

class TestApiMapi(unittest.TestCase):

    def test_wordlist(self):
        # Create wordlist with no wordlist arg
        args = Namespace(endpoint='https://jsonplaceholder.typicode.com/todos', extended=False, wordlist=None, output=None, output_json=None, bola_check=None, random=False, admin_check=False, authentication_basic=None, authentication_key=None, no_post=True, no_options=True)
        tested_wordlist = fuzzing.create_wordlist(args)
        self.assertEqual(tested_wordlist, ['access-token', 'account', 'accounts', 'admin', 'amount', 'api', 'api-docs', 'apidocs', 'balance', 'balances','bio', 'bios', 'category', 'channel', 
        'chart', 'circular', 'company', 'companies', 'content', 'contract', 'coordinate', 'credentials', 'creds', 'custom', 'customer', 'customers', 
        'details', 'dir', 'directory', 'dob', 'email', 'employee', 'event', 'favorite', 'feed', 'foo', 'form', 'github', 'gmail', 'group', 'history', 'hidden', 
        'image', 'info', 'item', 'job', 'link', 'links', 'location', 'locations', 'log', 'login', 'logins', 'logs', 'map', 'member', 'members', 
        'messages', 'money', 'my', 'name', 'names', 'news', 'option', 'options', 'pass', 'password', 'passwords', 'phone', 'picture', 'pin', 'post', 
        'prod', 'production', 'profile', 'profiles', 'publication', 'record', 'sale', 'sales', 'set', 'setting', 'settings', 'setup', 'site', 'swagger',
        'test', 'test1', 'theme', 'token', 'tokens', 'twitter', 'union', 'url', 'user', 'username', 'users', 'vendor', 'vendors', 'version', 'website', 
        'work'])

        # Create wordlist with fake file path arg
        args = Namespace(endpoint='https://jsonplaceholder.typicode.com/todos', extended=False, wordlist='/does/not/exist', output=None, output_json=None, bola_check=None, random=False, admin_check=False, authentication_basic=None, authentication_key=None, no_post=True, no_options=True)
        tested_wordlist = fuzzing.create_wordlist(args)
        self.assertEqual(tested_wordlist, ['access-token', 'account', 'accounts', 'admin', 'amount', 'api', 'api-docs', 'apidocs', 'balance', 'balances','bio', 'bios', 'category', 'channel', 
        'chart', 'circular', 'company', 'companies', 'content', 'contract', 'coordinate', 'credentials', 'creds', 'custom', 'customer', 'customers', 
        'details', 'dir', 'directory', 'dob', 'email', 'employee', 'event', 'favorite', 'feed', 'foo', 'form', 'github', 'gmail', 'group', 'history', 'hidden', 
        'image', 'info', 'item', 'job', 'link', 'links', 'location', 'locations', 'log', 'login', 'logins', 'logs', 'map', 'member', 'members', 
        'messages', 'money', 'my', 'name', 'names', 'news', 'option', 'options', 'pass', 'password', 'passwords', 'phone', 'picture', 'pin', 'post', 
        'prod', 'production', 'profile', 'profiles', 'publication', 'record', 'sale', 'sales', 'set', 'setting', 'settings', 'setup', 'site', 'swagger',
        'test', 'test1', 'theme', 'token', 'tokens', 'twitter', 'union', 'url', 'user', 'username', 'users', 'vendor', 'vendors', 'version', 'website', 
        'work'])

    def test_vfuzz(self):
        args = Namespace(endpoint='https://jsonplaceholder.typicode.com/todos', extended=False, wordlist=None, output=None, output_json=None, bola_check=None, random=False, admin_check=False, authentication_basic=None, authentication_key=None, no_post=True, no_options=True)
        fuzz_result = []
        fuzzing.v_fuzz('GET', args, fuzz_result, None, None)
        self.assertEqual(fuzz_result, [])

        args = Namespace(endpoint='https://jsonplaceholder.typicode.com/v1/todos', extended=False, wordlist=None, output=None, output_json=None, bola_check=None, random=False, admin_check=False, authentication_basic=None, authentication_key=None, no_post=True, no_options=True)
        fuzz_result = []
        fuzzing.v_fuzz('GET', args, fuzz_result, None, None)
        self.assertEqual(fuzz_result, [{'Endpoint': 'https://jsonplaceholder.typicode.com/v2/todos', 'Result': 404, 'Method': 'GET', 'Type': 'V Fuzz'}, {'Endpoint': 'https://jsonplaceholder.typicode.com/v3/todos', 'Result': 404, 'Method': 'GET', 'Type': 'V Fuzz'}, {'Endpoint': 'https://jsonplaceholder.typicode.com/v4/todos', 'Result': 404, 'Method': 'GET', 'Type': 'V Fuzz'}])

    def test_bola_fuzz(self):
        args = Namespace(endpoint='https://jsonplaceholder.typicode.com/todos', extended=False, wordlist=None, output=None, output_json=None, bola_check=5, random=False, admin_check=False, authentication_basic=None, authentication_key=None, no_post=True, no_options=True)
        fuzz_result = []
        fuzzing.bola_fuzz(args, fuzz_result, None, None)
        self.assertEqual(fuzz_result, [])

        args = Namespace(endpoint='https://jsonplaceholder.typicode.com/todos/1', extended=False, wordlist=None, output=None, output_json=None, bola_check=5, random=False, admin_check=False, authentication_basic=None, authentication_key=None, no_post=True, no_options=True)
        fuzz_result = []
        fuzzing.bola_fuzz(args, fuzz_result, None, None)
        self.assertEqual(fuzz_result, [{'Endpoint': 'https://jsonplaceholder.typicode.com/todos/2', 'Result': 200, 'Method': 'GET', 'Type': 'BOLA'}, {'Endpoint': 'https://jsonplaceholder.typicode.com/todos/3', 'Result': 200, 'Method': 'GET', 'Type': 'BOLA'}, {'Endpoint': 'https://jsonplaceholder.typicode.com/todos/4', 'Result': 200, 'Method': 'GET', 'Type': 'BOLA'}, {'Endpoint': 'https://jsonplaceholder.typicode.com/todos/5', 'Result': 200, 'Method': 'GET', 'Type': 'BOLA'}, {'Endpoint': 'https://jsonplaceholder.typicode.com/todos/6', 'Result': 200, 'Method': 'GET', 'Type': 'BOLA'}])

    def test_basic(self):
        args = Namespace(endpoint='https://jsonplaceholder.typicode.com/todos', extended=False, wordlist=None, output=None, output_json=None, bola_check=5, random=False, admin_check=False, authentication_basic=None, authentication_key=None, no_post=True, no_options=True)
        password = authentication.handle_basic(args)
        self.assertEqual(password, None)

        args = Namespace(endpoint='https://jsonplaceholder.typicode.com/todos', extended=False, wordlist=None, output=None, output_json=None, bola_check=5, random=False, admin_check=False, authentication_basic=True, authentication_key=None, no_post=True, no_options=True)
        password = authentication.handle_basic(args)
        self.assertEqual(password, 'y')

    def test_key(self):
        args = Namespace(endpoint='https://jsonplaceholder.typicode.com/todos', extended=False, wordlist=None, output=None, output_json=None, bola_check=5, random=False, admin_check=False, authentication_basic=None, authentication_key=None, no_post=True, no_options=True)
        key = authentication.handle_key(args)
        self.assertEqual(key, None)

        args = Namespace(endpoint='https://jsonplaceholder.typicode.com/todos', extended=False, wordlist=None, output=None, output_json=None, bola_check=5, random=False, admin_check=False, authentication_basic=None, authentication_key=True, no_post=True, no_options=True)
        key = authentication.handle_key(args)
        self.assertEqual(key, 'y')    
