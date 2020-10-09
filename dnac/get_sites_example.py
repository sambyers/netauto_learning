from dnac import DNAC
import json
import requests



# Open our host info from a file
with open('host.json', 'r') as f:
    dnac = json.loads(f.read())

# Set a variable to the url for DNAC
base_url = dnac['host']

# Make a dictionary holding our http headers
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Glue our DNAC url and the path for authentication together
# https://developer.cisco.com/docs/dna-center/#!cisco-dna-1-3-3-x-api-api-authentication-authentication-api
auth_path = f'{base_url}/dna/system/api/v1/auth/token'

# Send the request to DNAC with our username and password. Turn off TLS validation
auth_resp = requests.post(auth_path, auth=(dnac['username'], dnac['password']), verify=False)

# Make a dictionary from the response HTTP body
auth_resp_dict = auth_resp.json()

# Extract the token from the dictionary
token = auth_resp_dict['Token']

# Make a dictionary to hold our authentication header
# https://developer.cisco.com/docs/dna-center/#!cisco-dna-1-3-3-x-api-api-authentication-authentication-api
auth_header = {'X-Auth-Token': token}

# Update our header dictionary with the token we got from DNAC
headers.update(auth_header)

# Glue our DNAC url and the path for authentication together
# https://developer.cisco.com/docs/dna-center/#!cisco-dna-1-3-3-x-api-api-sites-get-site
get_site_path = f'{base_url}/dna/intent/api/v1/site'

# Send the request to DNAC with our HTTP headers including our token. Turn off TLS validation
site_resp = requests.get(get_site_path, headers=headers, verify=False)

# Make a dictionary from the response HTTP body
site_resp_dict = site_resp.json()

# Access the value associated with the key 'response'
# The value in this case is a list
# Loop through each item in the list and print the value associated with the key 'name'
for item in site_resp_dict['response']:
    print(item['name'])