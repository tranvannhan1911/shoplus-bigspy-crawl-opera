
import requests
import json


base_url = "http://127.0.0.1:8000/api"

def save_opera_shoplus(data):
    url = base_url+"/opera-shoplus-tiktok/"

    payload = json.dumps(data)
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response

def get_ads_id():
    url = base_url+"/ads_id/"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response