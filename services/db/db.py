from pymongo import MongoClient
from bson.binary import UuidRepresentation

import logging

def connect_db(uri : str):
    try:
        client = MongoClient(uri, uuidRepresentation="standard")
        db = client["p2p-betting-dev"]
    except TimeoutError:
        logging.error("Cannot connect to database, may be due to poor network connectivity")
        connect_db(uri=uri)
    else:
        return db