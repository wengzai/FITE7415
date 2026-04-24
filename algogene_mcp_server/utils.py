import requests
from config import BASE_URL, ALGOGENE_USER, ALGOGENE_API_KEY

def _request(action, url, data=None):
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            'user':ALGOGENE_USER, 
            'api_key':ALGOGENE_API_KEY
        }
        if data:
            params.update(data)
        if action=="GET":
            r = requests.get(BASE_URL+url, headers=headers, params=params)
        else:
            r = requests.post(BASE_URL+url, headers=headers, json=params)
        res = r.json()
        status = r.status_code
    except Exception as e:
        status, res = 400, "Invalid request"
    return status, res


def _request_app(action, url, data=None):
    try:
        headers = {
            'Content-Type': 'application/json',
            'user':ALGOGENE_USER, 
            'api_key':ALGOGENE_API_KEY
        }
        params = {}
        if type(data)==dict:
            params = data
        if action=="GET":
            r = requests.get(BASE_URL+url, headers=headers, params=params)
        else:
            r = requests.post(BASE_URL+url, headers=headers, json=params)
        res = r.json()
        status = r.status_code
    except Exception as e:
        status, res = 400, "Invalid request"
    return status, res


def validate_api_credentials():
    return _request("GET", "/v1/session")

