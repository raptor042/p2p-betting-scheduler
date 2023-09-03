import requests
import logging

def event(date, league_id, eid):
    try:
        response = requests.get(f"http://localhost:3030/event/{date}/{league_id}/{eid}")
    except:
        logging.error("Unable to send request to payment gateway")
    else:
        print(response.json())
        return response.json()

def fixtures(date):
    try:
        response = requests.get(f"http://localhost:3030/fixtures/{date}")
    except:
        logging.error("Unable to send request to payment gateway")
    else:
        print(response.json())
        return response.json()
    
def stats(eid):
    try:
        response = requests.get(f"http://localhost:3030/stats/{eid}")
    except:
        logging.error("Unable to send request to payment gateway")
    else:
        print(response.json())
        return response.json()