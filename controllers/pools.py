from services.db.pools import get_pools, update_pool, delete_pool
from services.db.users import get_user, update_user
from services.apis.sports import event

from datetime import datetime
from enum import Enum
from controllers.winnings import fan_base_pool

class State(Enum):
    INACTIVE = 0
    OPEN = 1
    LOCKED = 2
    CLOSED = 3

def cashout(db, winners, sub_total, total):
    for winner in winners:
        user_percent = int(winner["wager"]) * 100 / sub_total
        user_cashout = user_percent * total / 100

        user = get_user(db=db, query={"username" : winner["username"]})
        balance = float(user["balance"]) + float(user_cashout)
        user = update_user(db=db, query={"username" : winner["username"]}, value={"$set" : {"balance" : "{:.2f}".format(balance)}})
        print(user)

def invalid_pool(db, pool, users):
    update_pool(db=db, query={"poolId" : pool["poolId"]}, value={"$set" : {"bet-fee" : 0}})
    update_pool(db=db, query={"poolId" : pool["poolId"]}, value={"$set" : {"cashout" : "None"}})

    for user in users:
        _user = get_user(db=db, query={"username" : user["username"]})
        balance = float(_user["balance"]) + float(user["wager"])
        user = update_user(db=db, query={"username" : user["username"]}, value={"$set" : {"balance" : "{:.2f}".format(balance)}})
        print(user)

def void_pool(db, pool, users):
    update_pool(db=db, query={"poolId" : pool["poolId"]}, value={"$set" : {"bet-fee" : 0}})
    update_pool(db=db, query={"poolId" : pool["poolId"]}, value={"$set" : {"cashout" : "None"}})

    for user in users:
        _user = get_user(db=db, query={"username" : user["username"]})
        balance = float(_user["balance"]) + float(user["wager"])
        user = update_user(db=db, query={"username" : user["username"]}, value={"$set" : {"balance" : "{:.2f}".format(balance)}})
        print(user)

def winnings(db, pool) -> str:
    winner = fan_base_pool(db=db, pool=pool)
    home_wager = sum([int(user["wager"]) for user in pool["home"]])
    away_wager = sum([int(user["wager"]) for user in pool["away"]])
    _total = home_wager + away_wager
    bet_percent = 5
    bet_fee = bet_percent * _total / 100
    total = _total - bet_fee

    update_pool(db=db, query={"poolId" : pool["poolId"]}, value={"$set" : {"bet-fee" : bet_fee}})
    update_pool(db=db, query={"poolId" : pool["poolId"]}, value={"$set" : {"cashout" : total}})

    if winner == "home":
        winners = pool["home"]
        update_pool(db=db, query={"poolId" : pool["poolId"]}, value={"$set" : {"winner" : "home"}})
        cashout(db=db, winners=winners, sub_total=home_wager, total=total)
    elif winner == "away":
        winners = pool["away"]
        update_pool(db=db, query={"poolId" : pool["poolId"]}, value={"$set" : {"winner" : "away"}})
        cashout(db=db, winners=winners, sub_total=away_wager, total=total)
    elif winner == "void":
        update_pool(db=db, query={"poolId" : pool["poolId"]}, value={"$set" : {"winner" : "None"}})
        void_pool(db=db, pool=pool, users=pool["home"])
        void_pool(db=db, pool=pool, users=pool["away"])

def pool_scheduler(db) -> str:
    print("Running the pool scheduler")
    pools = get_pools(db=db)

    date = datetime.now()
    time = f"{date.strftime('%Y')}{date.strftime('%m')}{date.strftime('%d')}{date.strftime('%H')}{date.strftime('%M')}{date.strftime('%S')}"
    print(time, "pool")

    for pool in pools:
        if pool["state"] == State.INACTIVE.value:
            if int(pool["event-start-time"]) <= int(time):
                _pool = update_pool(db=db, query={"poolId" : pool["poolId"]}, value={"$set" : {"state" : State.CLOSED.value}})
                print(_pool, "inactive")
        elif pool["state"] == State.OPEN.value:
            if int(pool["event-start-time"]) <= int(time):
                _pool = update_pool(db=db, query={"poolId" : pool["poolId"]}, value={"$set" : {"state" : State.LOCKED.value}})
                print(_pool, "open")
        elif pool["state"] == State.LOCKED.value:
            print(pool, "locked")
            if int(pool["event-end-time"]) <= int(time):
                count = pool["participant-count"]
                if count >= 2 and len(pool["home"]) >= 1 and len(pool["away"]) >= 1:
                    wins = winnings(db=db, pool=pool)
                    print(wins)

                    _pool = update_pool(db=db, query={"poolId" : pool["poolId"]}, value={"$set" : {"state" : State.CLOSED.value}})
                    print(_pool)
                else:
                    users = [*pool["home"], *pool["away"]]
                    print(users)
                    invalid_pool(db=db, pool=pool, users=users)

                    _pool = update_pool(db=db, query={"poolId" : pool["poolId"]}, value={"$set" : {"state" : State.CLOSED.value}})
                    print(_pool)

    return "Successful Pool Scheduling Session"