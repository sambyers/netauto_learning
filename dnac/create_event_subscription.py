from dnac import DNAC
import json


sub = [
    {
        "version": "1.0.0",
        "name": "my-demo-event-sub-high-io-swintf",
        "description": "Demo event sub created via intent api",
        "subscriptionEndpoints": [
            {
                "instanceId": "string",
                "subscriptionDetails": {
                    "name": "api endpoint",
                    "url": "YOUR API HERE",
                    "method": "POST",
                    "connectorType": "REST"
                }
            }
        ],
        "filter": { "eventIds": [ "NETWORK-DEVICES-3-208" ] }
    }
]

with open('host.json', 'r') as f:
    host = json.loads(f.read())

dnac = DNAC(**host)
data = dnac.create_event_subscriptions(sub)
print(json.dumps(data, indent=4))