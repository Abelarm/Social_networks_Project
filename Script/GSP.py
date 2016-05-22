#!/usr/bin/python
import sys
from random import randint

#Implements a GSP auction
def gsp(slot_ctrs, adv_bids):
    
    #Sort advertisers names in decreasing order of their bids
    sort_advs=sorted(adv_bids.keys(), key=adv_bids.__getitem__, reverse=True)
    #Sort slots names in decreasing order of their clickthrough rates
    sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)
    
    #It will contain for each advertiser the name of the slot assigned to him
    adv_slots=dict()
    #It will contain for each advertiser the payment assigned to him
    adv_pays = dict()
    
    for i in range(min(len(sort_advs),len(sort_slots))):
        adv_slots[sort_advs[i]]=sort_slots[i] #The i-th advertiser takes the i-th slot
        if i == len(sort_advs) - 1: #If it is the last advertiser, the payment is 0
            adv_pays[sort_advs[i]]=0
        else: # Else the payment is the slot of the next advertiser
            adv_pays[sort_advs[i]]=adv_bids[sort_advs[i+1]]
    
    return adv_slots, adv_pays

#We implement a possible bot for an advertiser in a repeated GSP auction
#The bot of an advertiser is a program that, given the history of what occurred in previous auctions, suggest a bid for the next auction.
#Specifically, a bot takes in input
#- the name of the advertiser (it allows to use the same bot for multiple advertisers)
#- the value of the advertiser (it is necessary for evaluating the utility of the advertiser)
#- the clickthrough rates of the slots
#- the history
#We assume the history is represented as an array that contains an entry for each time step,
#i.e. history[i] contains the information about the i-th auction.
#In particular, for each time step we have that 
#- history[i]["adv_bids"] returns the advertisers' bids as a dictionary in which the keys are advertisers' names and values are their bids
#- history[i]["adv_slots"] returns the assignment as a dictionary in which the keys are advertisers' names and values are their assigned slots
#- history[i]["adv_pays"] returns the payments as a dictionary in which the keys are advertisers' names and values are their assigned prices

#The bot that we implement here is a symple best_response bot:
#it completely disregards the history except the last step,
#and suggest the bid that will maximize the advertiser utility
#given that the other advertisers do not change their bids.
def best_response(name, adv_value, slot_ctrs, history):
    
    step = len(history)
    
    #If this is the first step there is no history and no best-response is possible
    #We suppose that adevertisers simply bid their value.
    #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
    if step == 0:
        return 0
    
    #Initialization
    adv_slots=history[step-1]["adv_slots"]
    adv_bids=history[step-1]["adv_bids"]
    
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
        return min(adv_value, sort_bids[len(sort_slots)])
    
    #prima slot
    if preferred_slot == 0:
        # TIE-BREAKING RULE: I choose the bid that is exactly in the middle between my own value and the next bid
        return float(adv_value+payment)/2
    
    #TIE-BREAKING RULE: If I like slot j, I choose the bid b_i for which I am indifferent from taking j at computed price or taking j-1 at price b_i
    return (adv_value - float(slot_ctrs[sort_slots[preferred_slot]])/slot_ctrs[sort_slots[preferred_slot-1]] * (adv_value - payment))


def best_response_competitive(name, adv_value, slot_ctrs, history):
    
    step = len(history)
    
    #If this is the first step there is no history and no best-response is possible
    #We suppose that adevertisers simply bid their value.
    #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
    if step == 0:
        return adv_value
    
    #Initialization
    adv_slots=history[step-1]["adv_slots"]
    adv_bids=history[step-1]["adv_bids"]
    
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
        #print("ENTRO")
        if i < last_slot: #If I take a slot better than the one previously assigned to me
            tmp_pay = sort_bids[i] #then, I must pay for that slot the bid of the advertiser at which that slot was previously assigned
            
        elif i == len(sort_bids) - 1: #If I take the last slot, I must pay 0
            tmp_pay = 0
            
        else: #If I take the slot as before or a worse one (but not the last)
            tmp_pay = sort_bids[i+1] #then, I must pay for that slot the bid of the next advertiser
        
    #2) Evaluate for each slot, which one gives to the advertiser the largest utility
        new_utility = slot_ctrs[sort_slots[i]]*(adv_value-tmp_pay)
        
        #print ("OLD UTILITY: " +str(utility) +" NEW UTILITY: " +str(new_utility))
        if new_utility > utility:
            utility = new_utility
            preferred_slot = i
            payment = tmp_pay
    
    #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
    #ultima slot
    if preferred_slot == -1:
        print("NO PREFERED")
        return 0
    
    #print(utility,adv_value,payment)
    return max(utility, payment)

def best_response_altruistic(name, adv_value, slot_ctrs, history):
    
    step = len(history)

    #If this is the first step there is no history and no best-response is possible
    #We suppose that adevertisers simply bid their value.
    #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
    if step == 0:
        return 0
    
    #Initialization
    adv_slots=history[step-1]["adv_slots"]
    adv_bids=history[step-1]["adv_bids"]

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
        return 0
    
    return min(utility, payment)


def competitive(name, adv_value, slot_ctrs, history):
    
    step = len(history)
    
    #If this is the first step there is no history and no best-response is possible
    #We suppose that adevertisers simply bid their value.
    #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
    if step == 0:
        return adv_value
    
    #Initialization
    adv_slots=history[step-1]["adv_slots"]
    adv_bids=history[step-1]["adv_bids"]
    
    sort_bids=sorted(adv_bids.values(), reverse=True)
    sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)
    
    return sort_bids[0] + 1


def budget_saving(name, adv_value, slot_ctrs, history):
    
    step = len(history)
    
    #If this is the first step there is no history and no best-response is possible
    #We suppose that adevertisers simply bid their value.
    #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
    if step == 0:
        return 0
    
    #Initialization
    adv_slots=history[step-1]["adv_slots"]
    adv_bids=history[step-1]["adv_bids"]
    
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
        for b in history[i]["adv_bids"].values():
            all_bids.append(b)

    maxbidEVER= max(all_bids)

    return randint(0,maxbidEVER+1)


