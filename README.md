# APIMapi
Fuzz an undocumented API endpoint to map out hidden endpoints and get a better picture of an API's attack surface. APIMapi also includes some basic tests to find possible OWASP Top 10 vulnerabilities based solely on the endpoint.

## Table of contents

  * [Parameters](#parameters)
  * [Example Usage](#example-usage)
     * [Basic use](#basic-use)
     * [Fuzz with BOLA](#fuzz-with-bola)
     * [Rate limit test](#rate-limit-test)
  * [License](#license)

## Setup
To run APIMapi: 
- Download the project files.
- Run the `apimapi.py` file with Python in your terminal. I.e. `{PathToPython} {PathToAPIMapi.py} endpoint arguments`
- Specify an endpoint with arguments and run.

You may need to install the `requests` library if there are any errors saying the module can't be found. To do this run:
`python -m pip install requests` in your terminal of choice.

### Test
To run a basic test of APIMapi to ensure it is working, specify the endpoint `https://jsonplaceholder.typicode.com/todos`, and use the test wordlist with the argument `-w {YourPathToFile}/test_worlist.txt` where the path to the file is to the test wordlist found in the project folder.

You should see some 200 results in here of live endpoints in the test API.

## Parameters
Below is a table of possible commands that can be used with APIMapi. These can be used together and this is explored further in the [Example Usage](#example-usage) section of this README.

| Arguments        | Behaviour     |
|--------------|-----------|
| apimapi https://endpoint.co.uk | begin a fuzz of endpoint with no authentication using a default wordlist |
| apimapi https://endpoint.co.uk  -w /home/wordlists/thislist      | begin fuzz with specified wordlist (a default wordlist is used if none specified) |
| apimapi https://endpoint.co.uk  -ab username  | begin fuzz with basic authentication user specified |
| apimapi https://endpoint.co.uk  -ak asldkhweuf| begin fuzz with API key specified |
| apimapi https://endpoint.co.uk  -ab username -at  | test any found endpoint with no authentication to see if it potentially has broken authentication. Usable in conjunction with -ab or -ak |
| apimapi https://endpoint.co.uk  -o /home/file.txt | begin fuzz and output result to specified location |
| apimapi https://endpoint.co.uk  -j /home/usr | begin fuzz and output result to OpenAPI JSON format |
| apimapi https://endpoint.co.uk -e | perform an extended fuzz where the wordlist is added to the end of the URL path rather than replacing |
| apimapi https://endpoint.co.uk  -np | carry out no POST requests in the fuzz |
| apimapi https://endpoint.co.uk  -no | carry out no OPTIONS requests in the fuzz |
| apimapi https://endpoint.co.uk -s | skip the main fuzz and only carry out extra tests. -b or -f should be used in conjunction with this |
| apimapi https://endpoint.co.uk  -l 100 | check API for a rate limit by specifying how many requests to make in quick succession to the originally specified endpoint |
| apimapi https://endpoint.co.uk -f admin | check endpoint for basic Broken Function Level Authorization. Specify the extra path to test (advised to check 'admin' as this is common)|
| apimapi https://endpoint.co.uk -b 10 | check endpoint for Broken Object Level Authorization (BOLA) on numbered resource. Specify the amount of objects to check |
| apimapi https://endpoint.co.uk -b 10 -r | the same BOLA check but integers are randomly generated rather than incremented |

## Example Usage
### Basic Use
To complete a normal endpoint fuzz against an endpoint using a specified wordlist and basic authentication, and then output the result to a text file, run:
```console
foo@bar:~$ apimapi https://endpoint.co.uk  -w /home/wordlists/thislist -ab my_username -o /home/filelocation
```
### Fuzz with BOLA
To complete a BOLA check on a numbered resource in an endpoint using a random set of numbers, without first completing the main fuzz seen above, and output this to a file, use:
```console
foo@bar:~$ apimapi https://endpoint.co.uk/123  -s -b 100 -r -o /home/filelocation
```
### Rate Limit Test
To check if your target endpoint has a rate limit, skipping the main fuzz, run:
```console
foo@bar:~$ apimapi https://endpoint.co.uk  -s -l 10000
```

## License
[MIT](LICENSE.txt) - Lewis Heap - 2024