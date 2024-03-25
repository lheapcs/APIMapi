import re
import json

def init_fuzz_result(user_arguments):
    if user_arguments.output or user_arguments.output_json or user_arguments.admin_check:
        return []
    return None

# Output fuzz result to text.
def text_output_handler(user_arguments, fuzz_result)-> None:
    formatted_result = []

    sorted_data = sorted(fuzz_result, key=lambda x: x['Result']) # Put in order so 200 results show first.

    for result in sorted_data:
        formatted_string = f"{result['Result']}: {result['Method']} : {result['Endpoint']}\n"
        formatted_result.append(formatted_string)

    result_string = ''.join(formatted_result)

    try:
        with open(user_arguments.output, 'w') as result_output:
            result_output.write(result_string)
        print(f"\nFile output successfully to {user_arguments.output}")    
    except Exception as e:
        print(f"\n{e}")

# Output fuzz result to JSON in OpenAPI format.
def json_output_handler(user_arguments, fuzz_result)-> None:
    filtered_data = [entry for entry in fuzz_result if 200 <= entry['Result'] <= 300] #Only keep results in the 200 response range.

    # Create start of OpenAPI structure
    json_string = {}
    json_string['openapi'] = '3.0.1'
    json_string['info'] = {'title': input('\nEnter tested API\'s name: '), 'version': 'v1'}
    json_string['servers'] = [{'url': re.sub(r'/([^/\d]+)(?:/\d+)?$', '', user_arguments.endpoint)}]
    json_string['paths'] = {}

    # Finish OpenAPI based on 200 results.
    for result in filtered_data:
        pattern = re.compile(r'/([^/\d]+)(?:/\d+)?$')
        keyword = re.search(pattern, result['Endpoint']).group(1)

        try: 
            json_string['paths'][f'/{keyword}']
        except: 
            json_string['paths'][f'/{keyword}'] = {f"{result['Method'].lower()}" : {'tags': [f'{keyword}'], 'responses': {f"{result['Result']}": {'description': 'Success'}}}}   
        else:
            json_string['paths'][f'/{keyword}'][f"{result['Method'].lower()}"] = {'tags': [f'{keyword}'], 'responses': {f"{result['Result']}": {'description': 'Success'}}}

    # Write to file.
    try:
        with open(user_arguments.output_json, 'w') as result_output:
            json.dump(json_string, result_output)
        print(f"\nJSON file output successfully to {user_arguments.output_json}")    
    except Exception as e:
        print(f"\n{e}")


if __name__ == "__main__":
    print('Functions only run as part of the main apimapi module.')