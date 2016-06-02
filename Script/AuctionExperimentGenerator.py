from Bots import *
import load_dataset 
import random as rm
from Test_Bots import run_auction

queries = ["national", "granmother", "hotel", "painting", "salamander", "buidling", "obama", "university", "console", "art"]
advertiser = ["x", "y", "z", "w", "k", "q"]

num_query = 20
adv_bots = dict()

adv_bots=dict()
adv_bots["x"] = best_preferential_competitor
adv_bots["y"] = best_preferential_competitor
adv_bots["z"] = best_preferential_competitor
adv_bots["w"] = best_preferential_competitor
adv_bots["k"] = best_preferential_competitor
adv_bots["q"] = best_preferential_competitor

tot_rev_gsp = 0
tot_val_gsp = 0

tot_rev_fpa = 0
tot_val_fpa = 0

rep = 500
for it in range(rep):

	threshold =  rm.randint(5,15)

	slot_ctrs = dict()

	for q in queries:
		slot_ctrs[q] = dict()
		num_slot = rm.randint(2,4)
		for i in range(num_slot):
			slot_ctrs[q]["id"+str(i+1)] = rm.uniform(0,1) 

	adv_values = dict()

	for q in queries:
		adv_values[q] = dict()
		for a in advertiser:
			adv_values[q][a] = rm.randint(0,20)

	adv_budgets = dict()

	for a in advertiser:
		adv_budgets[a] = rm.randint(10,50)

	'''
	print ("calling GSP #" + str(it) + " on configuration:\n")
	print("------Slot Clickthrough------")
	print ("\t\t" + str(slot_ctrs))
	print("------Adv Values------")
	print ("\t\t"+str(adv_values)) 
	print("------Slot Clickthrough------")
	print("\t\t"+ str(adv_budgets)) 
	'''

	#print("--------STARTING AUCTION--------")
	tmp = run_auction("x", num_query, queries, slot_ctrs, adv_values, adv_budgets, adv_bots, threshold ,"gsp")
	val = tmp[0]
	rev = tmp[1]
	#print(val)
	tot_val_gsp += val
	tot_rev_gsp += rev

	tmp = run_auction("x", num_query, queries, slot_ctrs, adv_values, adv_budgets, adv_bots, threshold ,"fpa")
	val = tmp[0]
	rev = tmp[1]
	#print(val)
	tot_val_fpa += val
	tot_rev_fpa += rev

	#raw_input()


print ("Totale Val GSP:\t\t" + str(float(tot_val_gsp)/rep))
print ("Totale Rev GSP:\t\t" + str(float(tot_rev_gsp)/rep))
print ("\n\n")
print ("Totale Val FPA:\t\t" + str(float(tot_val_fpa)/rep))
print ("Totale Rev FPA:\t\t" + str(float(tot_rev_fpa)/rep))






