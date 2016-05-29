import Bots
import load_dataset 
from random import *
from Test_Bots import run_auction

bots_name = []
to_not_call = ["uniform","randint","sys"]

for method in dir(Bots):
	if not "__" in method and not method in to_not_call:
		bots_name.append(method)

queries = ["national", "granmother", "hotel", "painting", "salamander", "buidling", "obama", "university", "console", "art"]
advertiser = ["x", "y", "z", "w", "k", "q"]

threshold = 10
adv_bots = dict()

for it in range(500):


	slot_ctrs = dict()

	for q in queries:
		slot_ctrs[q] = dict()
		num_slot = randint(2,4)
		for i in range(num_slot):
			slot_ctrs[q]["id"+str(i+1)] = uniform(0,1) 

	adv_values = dict()

	for q in queries:
		adv_values[q] = dict()
		for a in advertiser:
			adv_values[q][a] = randint(0,20)

	adv_budgets = dict()

	for a in advertiser:
		adv_budgets[a] = randint(10,50)

	adv_bots = dict()

	print ("calling GSP #" + str(it) + " on configuration:\n")
	print (slot_ctrs)
	print (adv_values) 
	print(adv_budgets) 

	for io in bots_name:
		adv_bots["x"] = getattr(Bots, io)

		for name in bots_name:
			for other in advertiser:
				if other != "x":
					adv_bots[other] = getattr(Bots, name)

			print(adv_bots)
			run_auction(20, queries, slot_ctrs, adv_values, adv_budgets, adv_bots, threshold, "fpa")

			raw_input()






