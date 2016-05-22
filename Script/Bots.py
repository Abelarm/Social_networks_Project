import sys
from random import randint


def best_response(name, adv_value, slot_ctrs, history, query):
    
    step = len(history)
    
    if step == 0:
        return 0
    
    #Initialization
    for i in range(1,step+1):
        if query in history[step-i]:
            adv_slots=history[step-i][query]["adv_slots"]
            adv_bids=history[step-i][query]["adv_bids"]
            break
        if step-i == 0:
            return 0

    sort_bids=sorted(adv_bids.values(), reverse=True)
    sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)
    
    #Saving the index of slots assigned at the advertiser in the previous auction
    if name not in adv_slots.keys():
        last_slot=-1
    else:
        last_slot=sort_slots.index(adv_slots[name])
        
    utility = -1
    preferred_slot = -1
    payment = 0

    #The best response bot makes the following steps:
    #1) Evaluate for each slot, how much the advertiser would pay if
    #   - he changes his bid so that that slot is assigned to him
    #   - no other advertiser change the bid
    for i in range(len(sort_slots)):
        
        if i < last_slot: #If I take a slot better than the one previously assigned to me
            tmp_pay = sort_bids[i] #then, I must pay for that slot the bid of the advertiser at which that slot was previously assigned
            
        elif i == len(sort_bids) - 1: #If I take the last slot, I must pay 0
            tmp_pay = 0
            
        else: #If I take the slot as before or a worse one (but not the last)
            tmp_pay = sort_bids[i+1] #then, I must pay for that slot the bid of the next advertiser
        
    #2) Evaluate for each slot, which one gives to the advertiser the largest utility
        new_utility = slot_ctrs[sort_slots[i]]*(adv_value-tmp_pay)
        
        if new_utility > utility:
            utility = new_utility
            preferred_slot = i
            payment = tmp_pay
    
    #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
    #ultima slot
    if preferred_slot == -1:
        # TIE-BREAKING RULE: I choose the largest bid smaller than my value for which I lose
        return min(adv_value[query], sort_bids[len(sort_slots)])
    
    #prima slot
    if preferred_slot == 0:
        # TIE-BREAKING RULE: I choose the bid that is exactly in the middle between my own value and the next bid
        return float(adv_value[query]+payment)/2
    
    #TIE-BREAKING RULE: If I like slot j, I choose the bid b_i for which I am indifferent from taking j at computed price or taking j-1 at price b_i
    return (adv_value - float(slot_ctrs[sort_slots[preferred_slot]])/slot_ctrs[sort_slots[preferred_slot-1]] * (adv_value - payment))


def best_response_competitive(name, adv_value, slot_ctrs, history, query):
    
    step = len(history)
    
    if step == 0:
        return adv_value
    
    #Initialization
    for i in range(1,step+1):
        if query in history[step-i]:
            adv_slots=history[step-i][query]["adv_slots"]
            adv_bids=history[step-i][query]["adv_bids"]
            break
        if step-i == 0:
            return 0
    
    sort_bids=sorted(adv_bids.values(), reverse=True)
    sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)
    
    if name not in adv_slots.keys():
        last_slot=-1
    else:
        last_slot=sort_slots.index(adv_slots[name])
        
    utility = -1
    preferred_slot = -1
    payment = 0

    for i in range(len(sort_slots)):
        if i < last_slot: 
            tmp_pay = sort_bids[i] 
            
        elif i == len(sort_bids) - 1: 
            tmp_pay = 0
            
        else: 
            tmp_pay = sort_bids[i+1]
        
        new_utility = slot_ctrs[sort_slots[i]]*(adv_value-tmp_pay)
        
        if new_utility > utility:
            utility = new_utility
            preferred_slot = i
            payment = tmp_pay
    
    if preferred_slot == -1:
        return 0
    
    return max(utility, payment)


def best_response_altruistic(name, adv_value, slot_ctrs, history, query):
    
    step = len(history)

    if step == 0:
        return 0

    for i in range(1,step+1):
        if query in history[step-i]:
            adv_slots=history[step-i][query]["adv_slots"]
            adv_bids=history[step-i][query]["adv_bids"]
            break
        if step-i == 0:
            return 0

    sort_bids=sorted(adv_bids.values(), reverse=True)
    sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)


    if name not in adv_slots.keys():
        last_slot=-1
    else:
        last_slot=sort_slots.index(adv_slots[name])
        
    utility = -1
    preferred_slot = -1
    payment = 0

    for i in range(len(sort_slots)):
        
        if i < last_slot: 
            tmp_pay = sort_bids[i]
            
        elif i == len(sort_bids) - 1: 
            tmp_pay = 0
            
        else: 
            tmp_pay = sort_bids[i+1] 
        
        new_utility = slot_ctrs[sort_slots[i]]*(adv_value-tmp_pay)
        
        if new_utility > utility:
            utility = new_utility
            preferred_slot = i
            payment = tmp_pay
    
    if preferred_slot == -1:
        return 0
    
    return min(utility, payment)


def competitor(name, adv_value, slot_ctrs, history, query):
    
    step = len(history)
    
    if step == 0:
        return adv_value
    

    for i in range(1,step+1):
        if query in history[step-i]:
            adv_slots=history[step-i][query]["adv_slots"]
            adv_bids=history[step-i][query]["adv_bids"]
            break
        if step-i == 0:
            return 0

    sort_bids=sorted(adv_bids.values(), reverse=True)
    sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)
    
    return sort_bids[0] + 1


def budget_saving(name, adv_value, slot_ctrs, history, query):
    
    step = len(history)
    
    if step == 0:
        return 0
    
    for i in range(1,step+1):
        if query in history[step-i]:
            adv_slots=history[step-i][query]["adv_slots"]
            adv_bids=history[step-i][query]["adv_bids"]
            break
        if step-i == 0:
            return 0
    
    min_value = sys.float_info.max
    min_name = None
    for bid in adv_bids:
        if not bid in adv_slots and adv_bids[bid]<min_value:
            min_value = adv_bids[bid]
            min_name = bid

    return min(min_value,adv_value)


def random(name, adv_value, slot_ctrs, history):

    all_bids = []
    for i in range(len(history)):
        for b in history[i][query]["adv_bids"].values():
            all_bids.append(b)

    maxbidEVER= max(all_bids)

    return randint(0,maxbidEVER+1)


def competitor_budget(name, adv_value, budget, current_budget, slot_ctrs, history, query):

    if current_budget >= budget/2:
        return competitor(name, adv_value, slot_ctrs, history, query)
    else:
        return best_response(name, adv_value, slot_ctrs, query)


def preferential_competitor(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query)
    if adv_value > threshold:
        return competitor(name, adv_value, slot_ctrs, history, query)
    else:
        return budget_saving(name, adv_value, slot_ctrs, history, query)


def best_competitor_budget(name, adv_value, budget, current_budget, slot_ctrs, history, query):

    if current_budget >= budget/2:
        return best_competitor(name, adv_value, slot_ctrs, history, query)
    else:
        return best_response(name, adv_value, slot_ctrs, query)


def best_preferential_competitor(name, adv_value, threshold, budget, current_budget, slot_ctrs, history, query)
    if adv_value > threshold:
        return best_competitor(name, adv_value, slot_ctrs, history, query)
    else:
        return budget_saving(name, adv_value, slot_ctrs, history, query)















