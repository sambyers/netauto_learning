from dnac import DNAC
import json


with open('host.json', 'r') as f:
    host = json.loads(f.read())

dnac = DNAC(**host)
data = dnac.get_client_health()
print('')
for category in data['response'][0]['scoreDetail']:
    # Omit the top level dictionary in the response for ALL client types
    if category['scoreCategory']['value'] in ['WIRED', 'WIRELESS']:
        print(f"Client category: {category['scoreCategory']['value']}")
        print(f"Client count: {category['clientCount']}")
        for score in category['scoreList']:
            print(f"{score['scoreCategory']['value']}: {score['clientCount']}")
print('')