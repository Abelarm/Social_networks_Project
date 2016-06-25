import load_dataset as ld
import random as rd

def query():
	query_to_return = dict()
	db = ld.get_db_ordered()

	query = dict()
	query["0.7"] = dict()
	query["0.6"] = dict()
	query["0.5"] = dict()
	query["0.4"] = dict()
	query["0.3"] = dict()

	for k in db:
		if len(db[k]) == 0:
			continue
		p = rd.uniform(0,1)
		if p > 0.7:
			if len(db[k]) > 7:
				query["0.7"][k] = db[k][:7]
		if 0.6 < p < 0.7 :
			if len(db[k]) > 6:
				query["0.6"][k] = db[k][:6]
		if 0.5 < p < 0.6:
			if len(db[k]) > 5:
				query["0.5"][k] = db[k][:5]
		if 0.4 < p < 0.5:
			if len(db[k]) > 4:
				query["0.4"][k] = db[k][:4]
		if 0.3 < p < 0.4:
			if len(db[k]) > 3:
				query["0.3"][k] = db[k][:3]


	for k in query:
		for i in range(5):
			rand_ind = rd.randint(0,len(query[k])-1)
			key = list(query[k].keys())[rand_ind]
			query_to_return[key] = query[k][key]

	return query_to_return
