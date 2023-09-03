import logging

def get_stat(db, query : dict) -> dict:
    try:
        stat = db.collection["stats"].find_one(query)
    except TimeoutError:
        logging.error("Cannot get stat data to database, may be due to poor network connectivity")
    else:
        return stat

def set_stat(db, value : dict) -> dict:
    try:
        stat = db.collection["stats"].insert_one(value)
    except TimeoutError:
        logging.error("Cannot post stat data to database, may be due to poor network connectivity")
    else:
        return stat

def update_stat(db, query: dict, value: dict) -> dict:
    try:
        stat = db.collection["stats"].update_one(query, value)
    except TimeoutError:
        logging.error("Cannot update stat data to database, may be due to poor network connectivity")
    else:
        return stat
    
def delete_stat(db, query: dict) -> dict:
    try:
        stat = db.collection["stats"].delete_one(query)
    except TimeoutError:
        logging.error("Cannot delete stat data to database, may be due to poor network connectivity")
    else:
        return stat