from services.db.bets import get_bets, update_bet, delete_bet
from services.db.users import get_user, update_user
from services.apis.sports import event

from datetime import datetime
from enum import Enum

from controllers.winnings import _1x2, gg_ng, over_under, _1st_goal, odd_even, correct_score, player_to_score, exact_goals

class State(Enum):
    INACTIVE = 0
    OPEN = 1
    LOCKED = 2
    CLOSED = 3

def void_bet(db, bet, booker, marquee, bookers_wager, marquees_wager):
    _booker = get_user(db=db, query={"username" : booker})
    balance = _booker["balance"]
    bookers_balance = float(balance) + float(bookers_wager)
    user = update_user(db=db, query={"username" : booker}, value={"$set" : {"balance" : "{:.2f}".format(bookers_balance)}})
    print(user)

    _marquee = get_user(db=db, query={"username" : marquee})
    _balance = _marquee["balance"]
    marquees_balance = float(_balance) + float(marquees_wager)
    user = update_user(db=db, query={"username" : booker}, value={"$set" : {"balance" : "{:.2f}".format(marquees_balance)}})
    print(user)

    update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"bet-fee" : 0}})
    update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"cashout" : "None"}})

def cashout(db, bet, username, wager):
    bet_percent = 5
    bet_fee = bet_percent * wager / 100
    net_profit = wager - bet_fee

    update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"bet-fee" : bet_fee}})
    update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"cashout" : net_profit}})

    user = get_user(db=db, query={"username" : username})
    balance = float(user["balance"]) + float(net_profit)

    user = update_user(db=db, query={"username" : username}, value={"$set" : {"balance" : "{:.2f}".format(balance)}})
    print(user)

def winnings(db, bet) -> str:
    booker = bet["booker"]
    marquee = bet["marquee"]
    bookers_wager = int(bet["bookers-wager"])
    marquees_wager = int(bet["marquees-wager"])
    total = bookers_wager + marquees_wager

    if bet["category"] == "1X2":
        winner = _1x2(db=db, bet=bet)
        if winner == "booker":
            update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"winner" : booker}})
            cashout(db=db, bet=bet, username=booker, wager=total)
        elif winner == "marquee":
            update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"winner" : marquee}})
            cashout(db=db, bet=bet, username=marquee, wager=total)
        elif winner == "void":
            update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"winner" : "None"}})
            void_bet(db=db, bet=bet, booker=booker, marquee=marquee, bookers_wager=bookers_wager, marquees_wager=marquees_wager)
    elif bet["category"] == "GG/NG":
        winner = gg_ng(db=db, bet=bet)
        if winner == "booker":
            update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"winner" : booker}})
            cashout(db=db, bet=bet, username=booker, wager=total)
        elif winner == "marquee":
            update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"winner" : marquee}})
            cashout(db=db, bet=bet, username=marquee, wager=total)
    elif bet["category"] == "Over/Under":
        winner = over_under(db=db, bet=bet)
        if winner == "booker":
            update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"winner" : booker}})
            cashout(db=db, bet=bet, username=booker, wager=total)
        elif winner == "marquee":
            update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"winner" : marquee}})
            cashout(db=db, bet=bet, username=marquee, wager=total)
    elif bet["category"] == "Player to Score":
        winner = player_to_score(db=db, bet=bet)
        if winner == "booker":
            update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"winner" : booker}})
            cashout(db=db, bet=bet, username=booker, wager=total)
        elif winner == "marquee":
            update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"winner" : marquee}})
            cashout(db=db, bet=bet, username=marquee, wager=total)
    elif bet["category"] == "Correct score":
        winner = correct_score(db=db, bet=bet)
        if winner == "booker":
            update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"winner" : booker}})
            cashout(db=db, bet=bet, username=booker, wager=total)
        elif winner == "marquee":
            update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"winner" : marquee}})
            cashout(db=db, bet=bet, username=marquee, wager=total)
    elif bet["category"] == "Exact Goals":
        winner = exact_goals(db=db, bet=bet)
        if winner == "booker":
            update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"winner" : booker}})
            cashout(db=db, bet=bet, username=booker, wager=total)
        elif winner == "marquee":
            update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"winner" : marquee}})
            cashout(db=db, bet=bet, username=marquee, wager=total)
    elif bet["category"] == "1st Goal":
        winner = _1st_goal(db=db, bet=bet)
        if winner == "booker":
            update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"winner" : booker}})
            cashout(db=db, bet=bet, username=booker, wager=total)
        elif winner == "marquee":
            update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"winner" : marquee}})
            cashout(db=db, bet=bet, username=marquee, wager=total)
    elif bet["category"] == "Odd/Even":
        winner = odd_even(db=db, bet=bet)
        if winner == "booker":
            update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"winner" : booker}})
            cashout(db=db, bet=bet, username=booker, wager=total)
        elif winner == "marquee":
            update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"winner" : marquee}})
            cashout(db=db, bet=bet, username=marquee, wager=total)

def bet_scheduler(db) -> str:
    print("Running the bet sheduler")
    bets = get_bets(db=db)

    date = datetime.now()
    time = f"{date.strftime('%Y')}{date.strftime('%m')}{date.strftime('%d')}{date.strftime('%H')}{date.strftime('%M')}{date.strftime('%S')}"
    print(time, "bet")

    for bet in bets:
        if bet["state"] == State.INACTIVE.value:
            print(bet, "inactive")
            if int(bet["event-start-time"]) <= int(time):
                _bet = update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"state" : State.CLOSED.value}})
                print(_bet)
        elif bet["state"] == State.OPEN.value:
            print(bet, "open")
            if int(bet["event-end-time"]) <= int(time):
                _bet = update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"state" : State.LOCKED.value}})
                print(_bet)
        elif bet["state"] == State.LOCKED.value:
            print(bet, "locked")
            if int(bet["event-end-time"]) <= int(time):
                if "marquee" in bet:
                    wins = winnings(db=db, bet=bet)
                    print(wins)

                    _bet = update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"state" : State.CLOSED.value}})
                    print(_bet)
                else:
                    username = bet["booker"]
                    user = get_user(db=db, query={"username" : username})
                    balance = user["balance"]
                    bookers_balance = float(balance) + float(bet["bookers-wager"])
                    user = update_user(db=db, query={"username" : username}, value={"$set" : {"balance" : "{:.2f}".format(bookers_balance)}})
                    print(user)

                    _bet = update_bet(db=db, query={"betId" : bet["betId"]}, value={"$set" : {"state" : State.CLOSED.value}})
                    print(_bet)

    return "Successful Bet Scheduling Session"