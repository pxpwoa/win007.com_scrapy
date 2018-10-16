import pickle

with open('league.pickle', 'rb') as f:
    old = pickle.load(f)

l = [x for x in old if '杯' not in x]
l = [x for x in l if '赛' not in x]

