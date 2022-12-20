import pickle

attempts=dict()
def load():
    with open("atlist.pickle","wb") as f:
        pickle.dump(attempts,f)
# load()
# atr = pickle.load(open("atlist.pickle","rb"))
# print(atr)
