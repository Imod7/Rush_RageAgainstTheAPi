import requests

response = requests.get("https://api.navitia.io/v1/")
print(response.status_code)