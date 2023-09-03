from services.db.stats import get_stat, set_stat
from services.apis.sports import stats

def win_pool(stat):
    home = stat["Tr1"]
    away = stat["Tr2"]

    if int(home) > int(away):
        winner = "home"
    elif int(home) < int(away):
        winner = "away"
    elif int(home) == int(away):
        winner = "void"

    return winner

def fan_base_pool(db, pool) -> str:
    eventId = pool["eid"]
    stat = get_stat(db=db, query={"eid" : eventId})
    print(stat)

    if stat:
        winner = win_pool(stat=stat)
    else:
        stat = stats(eid=eventId)
        print(stat)

        winner = win_pool(stat=stat)

        _stat = set_stat(db=db, value=stat)
        print(_stat)
    
    return winner

def win_1x2(stat, booker, marquee, void):
    home = stat["Tr1"]
    away = stat["Tr2"]

    if int(home) > int(away):
        if booker == "1":
            winner = "booker"
        elif marquee == "1":
            winner = "marquee"
        elif void == "1":
            winner = "void"
    elif int(home) < int(away):
        if booker == "2":
            winner = "booker"
        elif marquee == "2":
            winner = "marquee"
        elif void == "2":
            winner = "void"
    elif int(home) == int(away):
        if booker == "X":
            winner = "booker"
        elif marquee == "X":
            winner = "marquee"
        elif void == "X":
            winner = "void"

    return winner

def _1x2(db, bet) -> str:
    booker = bet["bookers-bet"]
    marquee = bet["marquees-bet"]
    void = bet["void-bet"]

    eventId = bet["eid"]
    stat = get_stat(db=db, query={"eid" : eventId})
    print(stat)

    if stat:
        winner = win_1x2(stat=stat, booker=booker, marquee=marquee, void=void)
    else:
        stat = stats(eid=eventId)
        print(stat)

        winner = win_1x2(stat=stat, booker=booker, marquee=marquee, void=void)

        _stat = set_stat(db=db, value=stat)
        print(_stat)
    
    return winner

def win_gg_ng(stat, booker, marquee):
    home = stat["Tr1"]
    away = stat["Tr2"]

    if int(home) > 0 and int(away) > 0:
        if booker == "GG":
            winner = "booker"
        elif marquee == "GG":
            winner = "marquee"
    elif int(home) == 0 or int(away) == 0:
        if booker == "NG":
            winner = "booker"
        elif marquee == "NG":
            winner = "marquee"
        
    return winner

def gg_ng(db, bet) -> str:
    booker = bet["bookers-bet"]
    marquee = bet["marquees-bet"]

    eventId = bet["eid"]
    stat = get_stat(db=db, query={"eid" : eventId})
    print(stat)

    if stat:
        winner = win_gg_ng(stat=stat, booker=booker, marquee=marquee)
    else:
        stat = stats(eid=eventId)
        print(stat)

        winner = win_gg_ng(stat=stat, booker=booker, marquee=marquee)

        _stat = set_stat(db=db, value=stat)
        print(_stat)
    
    return winner

def win_over_under(stat, booker, marquee):
    home = stat["Tr1"]
    away = stat["Tr2"]
    sum = int(home) + int(away)
    winner = "None"

    if booker == "Over 0.5" and marquee == "Under 0.5":
        if sum >= 1:
            winner = "booker"
        elif sum == 0:
            winner = "marquee"
    elif booker == "Over 1.5" and marquee == "Under 1.5":
        if sum >= 2:
            winner = "booker"
        elif sum <= 1:
            winner = "marquee"
    elif booker == "Over 2.5" and marquee == "Under 2.5":
        if sum >= 3:
            winner = "booker"
        elif sum <= 2:
            winner = "marquee"
    elif booker == "Over 3.5" and marquee == "Under 3.5":
        if sum >= 4:
            winner = "booker"
        elif sum <= 3:
            winner = "marquee"
    elif booker == "Over 4.5" and marquee == "Under 4.5":
        if sum >= 5:
            winner = "booker"
        elif sum <= 4:
            winner = "marquee"
    elif booker == "Over 5.5" and marquee == "Under 5.5":
        if sum >= 6:
            winner = "booker"
        elif sum <= 5:
            winner = "marquee"
    elif booker == "Over 6.5" and marquee == "Under 6.5":
        if sum >= 7:
            winner = "booker"
        elif sum <= 6:
            winner = "marquee"
        
    return winner

def over_under(db, bet) -> str:
    booker = bet["bookers-bet"]
    marquee = bet["marquees-bet"]

    eventId = bet["eid"]
    stat = get_stat(db=db, query={"eid" : eventId})

    if stat:
        winner = win_over_under(stat=stat, booker=booker, marquee=marquee)
    else:
        stat = stats(eid=eventId)

        winner = win_over_under(stat=stat, booker=booker, marquee=marquee)

        _stat = set_stat(db=db, value=stat)
        print(_stat)
    
    return winner

def check(db, eventId) -> str:
    booker = "Over 6.5"
    marquee = "Under 6.5"

    stat = get_stat(db=db, query={"eid" : eventId})

    if stat:
        winner = win_over_under(stat=stat, booker=booker, marquee=marquee)
    else:
        stat = stats(eid=eventId)

        winner = win_over_under(stat=stat, booker=booker, marquee=marquee)

        _stat = set_stat(db=db, value=stat)
        print(_stat)
    
    return winner

def win_player_to_score(stat, player):
    incs_1 = stat["Incs"]["1"]
    incs_2 = stat["Incs"]["2"]
    incs = [*incs_1, *incs_2]

    for inc in incs:
        print(inc)
        if "Sc" in inc:
            if "Incs" in inc:
                fn = inc["Incs"][0]["Fn"]
                ln = inc["Incs"][0]["Ln"]
                print(fn, ln)

                if player == fn or player == ln:
                    winner = "booker"
                    break
                elif player != fn and player != ln:
                    winner = "marquee"
            else:
                fn = inc["Fn"]
                ln = inc["Ln"]
                print(fn, ln)

                if player == fn or player == ln:
                    winner = "booker"
                    break
                elif player != fn and player != ln:
                    winner = "marquee"
        else:
            continue

    return winner

def player_to_score(db, bet) -> str:
    player = bet["player"]

    eventId = bet["eid"]
    stat = get_stat(db=db, query={"eid" : eventId})
    print(stat)

    if stat:
        winner = win_player_to_score(stat=stat, player=player)
    else:
        stat = stats(eid=eventId)
        print(stat)

        winner = win_player_to_score(stat=stat, player=player)

        _stat = set_stat(db=db, value=stat)
        print(_stat)
    
    return winner

def win_correct_score(stat, score):
    home = stat["Tr1"]
    away = stat["Tr2"]
    [_home, _away] = score.split("-", 1)

    if int(home) == int(_home) and int(away) == int(_away):
        winner = "booker"
    elif int(home) != int(_home) or int(away) != int(_away):
        winner = "marquee"

    return winner

def correct_score(db, bet) -> str:
    score = bet["score"]

    eventId = bet["eid"]
    stat = get_stat(db=db, query={"eid" : eventId})
    print(stat)

    if stat:
        winner = win_correct_score(stat=stat, score=score)
    else:
        stat = stats(eid=eventId)
        print(stat)

        winner = win_correct_score(stat=stat, score=score)

        _stat = set_stat(db=db, value=stat)
        print(_stat)
    
    return winner

def win_exact_goals(stat, goals):
    home = stat["Tr1"]
    away = stat["Tr2"]
    sum = int(home) + int(away)

    if sum == int(goals):
        winner = "booker"
    elif sum != int(goals):
        winner = "marquee"

    return winner

def exact_goals(db, bet) -> str:
    goals = bet["goals"]

    eventId = bet["eid"]
    stat = get_stat(db=db, query={"eid" : eventId})
    print(stat)

    if stat:
        winner = win_exact_goals(stat=stat, goals=goals)
    else:
        stat = stats(eid=eventId)
        print(stat)

        winner = win_exact_goals(stat=stat, goals=goals)

        _stat = set_stat(db=db, value=stat)
        print(_stat)
    
    return winner

def win_1st_goal(stat, booker, marquee):
    incs_1 = stat["Incs"]["1"]
    incs_2 = stat["Incs"]["2"]
    incs = [*incs_1, *incs_2]
    winner = "None"

    for inc in incs:
        print(inc)
        if "Sc" in inc:
            goal = "home" if inc["Sc"][0] == 1 else "away"
            print(goal)
            if goal == "home":
                if booker == "1":
                    winner = "booker"
                elif marquee == "1":
                    winner = "marquee"
            elif goal == "away":
                if booker == "2":
                    winner = "booker"
                elif marquee == "2":
                    winner = "marquee"
            break
        else:
            continue

    return winner

def _1st_goal(db, bet) -> str:
    booker = bet["bookers-bet"]
    marquee = bet["marquees-bet"]

    eventId = bet["eid"]
    stat = get_stat(db=db, query={"eid" : eventId})
    print(stat)

    if stat:
        winner = win_1st_goal(stat=stat, booker=booker, marquee=marquee)
    else:
        stat = stats(eid=eventId)
        print(stat)

        winner = win_1st_goal(stat=stat, booker=booker, marquee=marquee)

        _stat = set_stat(db=db, value=stat)
        print(_stat)
    
    return winner

def win_odd_even(stat, booker, marquee):
    home = stat["Tr1"]
    away = stat["Tr2"]
    sum = int(home) + int(away)
    print(sum % 2)
    winner = "None"

    if sum % 2 == 1:
        if booker == "Odd":
            winner = "booker"
        elif marquee == "Odd":
            winner = "marquee"
    elif sum % 2 == 0:
        if booker == "Even":
            winner = "booker"
        elif marquee == "Even":
            winner = "marquee"

    return winner

def odd_even(db, bet) -> str:
    booker = bet["bookers-bet"]
    marquee = bet["marquees-bet"]

    eventId = bet["eid"]
    stat = get_stat(db=db, query={"eid" : eventId})
    print(stat)

    if stat:
        winner = win_odd_even(stat=stat, booker=booker, marquee=marquee)
    else:
        stat = stats(eid=eventId)
        print(stat)

        winner = win_odd_even(stat=stat, booker=booker, marquee=marquee)

        _stat = set_stat(db=db, value=stat)
        print(_stat)
    
    return winner