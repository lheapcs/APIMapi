## APIMapi
Map out an undocumented API based on a single endpoint to get a better picture of an API's attack surface.

## Usage

| Arguments        | Behaviour     |
|--------------|-----------|
| apimapi https://endpoint.co.uk | begin a fuzz of endpoint with no authentication using a default wordlist |
| apimapi https://endpoint.co.uk  -w /home/wordlists/thislist      | begin fuzz with specified wordlist |
| apimapi https://endpoint.co.uk  -ab username  | begin fuzz with basic authentication user specified |
| apimapi https://endpoint.co.uk  -ak asldkhweuf| begin fuzz with API key specified |
| apimapi https://endpoint.co.uk  -o /home/file.txt | begin fuzz and output result to specified location |
| apimapi https://endpoint.co.uk  -d /home/usr | begin fuzz and output result to OpenAPI JSON format |
| apimapi https://endpoint.co.uk -e | perform an extended fuzz where the wordlist is added to the end of the URL path rather than replacing |
| apimapi https://endpoint.co.uk  -np | carry out no POST requests in the fuzz |
| apimapi https://endpoint.co.uk  -no | carry out no OPTIONS requests in the fuzz |
| apimapi https://endpoint.co.uk -s | skip the main fuzz and only carry out extra tests. -b or -f should be used in conjunction with this |
| apimapi https://endpoint.co.uk -f admin | check endpoint for basic Broken Function Level Authorization. Specify the extra path to test (advised to check 'admin' as this is common)|
| apimapi https://endpoint.co.uk -b 10 | check endpoint for Broken Object Level Authorization (BOLA) on numbered resource. Specify the amount of objects to check |
| apimapi https://endpoint.co.uk -b 10 -r | the same BOLA check but intergers are randmonly generated rather than incremented |
