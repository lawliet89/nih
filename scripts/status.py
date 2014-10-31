import requests
import json
import time

def wait_until_idle():
    time.sleep(5)
    while get_status() != 'idle':
        print "Waiting for Jukebox to be idle..."

def get_status():
    try:
        return _request_status()['result']['status']
    except:
        return 'unknown'

def _request_status():
    url = "http://localhost:8888/rpc/jukebox/get_queue"
    headers = { 'content-type': 'application/json' }
    payload = {
        "method": "get_queue",
        "id": 0,
        "params": []
    }

    response = requests.post(url, 
        data=json.dumps(payload), headers=headers).json()
    return response

if __name__ == "__main__":
    print get_status()
