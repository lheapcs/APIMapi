# APIMapi
API fuzzer final year project.

Map out an API based on a single endpoint to get a full picture of an API's attack surface.

# apimapi                                                       | run without any arguments, get ASCII art and small guide
# apimapi https://endpoint.co.uk                                | begin fuzz of endpoint with no authentication, with default wordlist
# apimapi https://endpoint.co.uk  -w /home/wordlists/thislist   | begin fuzz with specified wordlist
# apimapi https://endpoint.co.uk  -ab username:password         | begin fuzz with basic auth specified 
# apimapi https://endpoint.co.uk  -ak asldkhweuf                | begin fuzz with API key specified 
# apimapi https://endpoint.co.uk  -o /home/usr                  | begin fuzz and output result to specified location
# apimapi https://endpoint.co.uk  -d /home/usr                  | output to JSON file twith OpenAPI format