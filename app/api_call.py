import requests

API_URL = "http://127.0.0.1:8000/query"

query = "SELECT CallID, summary FROM calls LIMIT 5"

response = requests.get(API_URL, params={"q": query})

if response.status_code == 200:
    data = response.json()
    print("Results:")
    print(data)
else:
    print("Error:", response.text)