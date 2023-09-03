import logging
import os
from time import perf_counter, sleep
from dotenv import load_dotenv
import schedule

from services.db.db import connect_db
from controllers.bets import bet_scheduler
from controllers.pools import pool_scheduler

logging.basicConfig(format="%(asctime)s - %(message)s")

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
db = connect_db(uri=MONGO_URI)

def job(db):
    start = perf_counter()
    bet = bet_scheduler(db=db)
    print(bet)
    pool = pool_scheduler(db=db)
    print(pool)
    finish = perf_counter()
    print(f"It took {finish-start} seconds(s) to finish")

schedule.every(2).minutes.do(job_func=job, db=db)

while True:
    schedule.run_pending()
    sleep(1)