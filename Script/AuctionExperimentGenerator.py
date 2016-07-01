import Bots
import load_dataset 
import random as rm
from run_auction import *

queries = ["national", "granmother", "hotel", "painting", "salamander", "buidling", "obama", "university", "console", "art"]
advertiser = ["x", "y", "z", "w", "k", "q"]

num_query = 20
adv_bots = dict()

adv_bots=dict()

my_bots = ['best_response_competitive', 'budget_saving', 'best_preferential_competitor']
other_bots = ['best_response', 'best_response_competitive', 'best_response_altruistic', 'competitor', 'budget_saving', 'random',  'competitor_budget', 'preferential_competitor', 'best_competitor_budget', 'best_preferential_competitor']
for my_bot in my_bots:
	for adv_bot in other_bots:

		adv_bots["x"] = getattr(Bots, my_bot)
		adv_bots["y"] = getattr(Bots, adv_bot)
		adv_bots["z"] = getattr(Bots, adv_bot)
		adv_bots["w"] = getattr(Bots, adv_bot)
		adv_bots["k"] = getattr(Bots, adv_bot)
		adv_bots["q"] = getattr(Bots, adv_bot)

		tot_rev_gsp = 0
		tot_uti_gsp = 0
		tot_val_gsp = 0

		tot_rev_fpa = 0
		tot_uti_fpa = 0
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
			ut  = tmp[1]
			rev = tmp[2]
			#print(val)
			tot_val_gsp += val
			tot_uti_gsp += ut
			tot_rev_gsp += rev

			tmp = run_auction("x", num_query, queries, slot_ctrs, adv_values, adv_budgets, adv_bots, threshold ,"fpa")
			val = tmp[0]
			ut  = tmp[1]
			rev = tmp[2]
			#print(val)
			tot_val_fpa += val
			tot_uti_fpa += ut
			tot_rev_fpa += rev

			#raw_input()

		print ("My bot: " + my_bot + " enemies bot: " + adv_bot) 

		print ("Totale Val GSP:\t\t" + str(float(tot_val_gsp)/rep))
		print ("Totale Uti GSP:\t\t" + str(float(tot_uti_gsp)/rep))
		print ("Totale Rev GSP:\t\t" + str(float(tot_rev_gsp)/rep))
		print ("\n\n")
		print ("Totale Val FPA:\t\t" + str(float(tot_val_fpa)/rep))
		print ("Totale Uti FPA:\t\t" + str(float(tot_uti_fpa)/rep))
		print ("Totale Rev FPA:\t\t" + str(float(tot_rev_fpa)/rep))






