import requests
import json

# Constants
APPLICATION_ID = 'YourApplicationID'
API_KEY = 'YourAPIKey'
SOURCE_INDEX_NAME = 'YourSourceIndexName'
SOURCE_MODEL_NAME = 'YourSourceModelName'
TARGET_INDEX_NAME = 'YourTargetIndexName'
TARGET_MODEL_NAME = 'YourTargetModelName'

def clean_rule(rule):
    # Print the original rule
    print("Original rule:", json.dumps(rule, indent=4))
    
    # Removing unnecessary fields
    rule.pop('_metadata', None)
    rule.pop('_highlightResult', None)
    
    # Print the cleaned rule
    print("Cleaned rule:", json.dumps(rule, indent=4))
    return rule

def list_recommend_rules():
    url = f"https://{APPLICATION_ID}.algolia.net/1/indexes/{SOURCE_INDEX_NAME}/{SOURCE_MODEL_NAME}/recommend/rules/search"
    headers = {
        'X-Algolia-API-Key': API_KEY,
        'X-Algolia-Application-Id': APPLICATION_ID,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps({}))
    
    # Print the response from listing rules
    print("List rules response:", json.dumps(response.json(), indent=4))
    return response.json()

def push_recommend_rules(rules):
    url = f"https://{APPLICATION_ID}.algolia.net/1/indexes/{TARGET_INDEX_NAME}/{TARGET_MODEL_NAME}/recommend/rules/batch"
    headers = {
        'X-Algolia-API-Key': API_KEY,
        'X-Algolia-Application-Id': APPLICATION_ID,
        'Content-Type': 'application/json'
    }
    # Extracting rules directly into an array
    clean_rules = [clean_rule(rule) for rule in rules.get('hits', [])]
    payload = json.dumps(clean_rules)  # Sending the array directly without wrapping in a 'rules' object

    # Print the final payload being sent
    print("Final payload being sent:", payload)
    
    response = requests.post(url, headers=headers, data=payload)
    
    # Print the response from pushing rules
    print("Push rules response:", json.dumps(response.json(), indent=4))
    return response.json()

# Retrieve rules from source
rules = list_recommend_rules()

# Push rules to target
result = push_recommend_rules(rules)
print("Final result:", json.dumps(result, indent=4))
