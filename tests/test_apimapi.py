import unittest
from argparse import Namespace

class TestApiMapi(unittest.TestCase):
    
    def test_vfuzz(self):
        args = Namespace(endpoint='https://jsonplaceholder.typicode.com/todos', extended=False, wordlist=None, output=None, output_json=None, bola_check=None, random=False, admin_check=False, authentication_basic=None, authentication_key=None, no_post=True, no_options=True)
        # Need to call vfuzz here with an endpoint.
        # First of all, code needs a refactor to remove the global user args.
        pass

    def test_wordlist(self):
        # Create wordlist with no wordlist arg
        args = Namespace(endpoint='https://jsonplaceholder.typicode.com/todos', extended=False, wordlist=None, output=None, output_json=None, bola_check=None, random=False, admin_check=False, authentication_basic=None, authentication_key=None, no_post=True, no_options=True)
        #tested_wordlist = apimapi.create_wordlist(args)
        #self.assertEqual(tested_wordlist, ['access-token', 'account', 'accounts', 'admin', 'amount', 'balance', 'balances', 'bar', 'baz', 'bio', 'bios', 'category', 'channel', 'chart', 'circular', 'company', 'companies', 'content', 'contract', 'coordinate', 'credentials', 'creds', 'custom', 'customer', 'customers', 'details', 'dir', 'directory', 'dob', 'email', 'employee', 'event', 'favorite', 'feed', 'foo', 'form', 'github', 'gmail', 'group', 'history', 'image', 'info', 'item', 'job', 'link', 'links', 'location', 'locations', 'log', 'login', 'logins', 'logs', 'map', 'member', 'members', 'messages', 'money', 'my', 'name', 'names', 'news', 'option', 'options', 'pass', 'password', 'passwords', 'phone', 'picture', 'pin', 'post', 'prod', 'production', 'profile', 'profiles', 'publication', 'record', 'sale', 'sales', 'set', 'setting', 'settings', 'setup', 'site', 'swagger', 'test', 'test1', 'theme', 'token', 'tokens', 'twitter', 'union', 'url', 'user', 'username', 'users', 'vendor', 'vendors', 'version', 'website', 'work'])

        # Create wordlist with fake file path arg
        args = Namespace(endpoint='https://jsonplaceholder.typicode.com/todos', extended=False, wordlist='/does/not/exist', output=None, output_json=None, bola_check=None, random=False, admin_check=False, authentication_basic=None, authentication_key=None, no_post=True, no_options=True)
        #tested_wordlist = apimapi.create_wordlist(args)
        #self.assertEqual(tested_wordlist, ['access-token', 'account', 'accounts', 'admin', 'amount', 'balance', 'balances', 'bar', 'baz', 'bio', 'bios', 'category', 'channel', 'chart', 'circular', 'company', 'companies', 'content', 'contract', 'coordinate', 'credentials', 'creds', 'custom', 'customer', 'customers', 'details', 'dir', 'directory', 'dob', 'email', 'employee', 'event', 'favorite', 'feed', 'foo', 'form', 'github', 'gmail', 'group', 'history', 'image', 'info', 'item', 'job', 'link', 'links', 'location', 'locations', 'log', 'login', 'logins', 'logs', 'map', 'member', 'members', 'messages', 'money', 'my', 'name', 'names', 'news', 'option', 'options', 'pass', 'password', 'passwords', 'phone', 'picture', 'pin', 'post', 'prod', 'production', 'profile', 'profiles', 'publication', 'record', 'sale', 'sales', 'set', 'setting', 'settings', 'setup', 'site', 'swagger', 'test', 'test1', 'theme', 'token', 'tokens', 'twitter', 'union', 'url', 'user', 'username', 'users', 'vendor', 'vendors', 'version', 'website', 'work'])