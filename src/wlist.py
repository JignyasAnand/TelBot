import Keys as K
import pickle
import sqlinit

class Allowed:
    def __init__(self):
        self.obj=sqlinit.sqlop()
        # self.whitelist=pickle.load(open("whlst.pickle","rb"))
        # self.attempt_list=pickle.load(open("atlist.pickle","rb"))
        # print(self.whitelist)
    def add_usr(self,usr):
        self.obj.insertf("whitelist",usr)
        # self.whitelist.append(usr)
        # with open("whlst.pickle","wb") as f:
        #     pickle.dump(self.whitelist,f)
        # self.whitelist=pickle.load(open("whlst.pickle","rb"))
    def rem_usr(self,usr):
        self.obj.remusr(usr)
        # self.whitelist.remove(usr)
        # with open("whlst.pickle","wb") as f:
        #     pickle.dump(self.whitelist,f)
        # self.whitelist=pickle.load(open("whlst.pickle","rb"))
    def get_list(self):
        return self.obj.getwlist()
        # return self.whitelist
    def add_attempt(self,usr,name):
        self.obj.insertf("attempts",usr, name)
        # if usr in self.attempt_list:
        #     self.attempt_list[usr][1]+=1
        # else:
        #     self.attempt_list[usr]=[]
        #     self.attempt_list[usr].append(name)
        #     self.attempt_list[usr].append(1)
        # with open("atlist.pickle","wb") as f:
        #     pickle.dump(self.attempt_list,f)
        # self.attempt_list=pickle.load(open("atlist.pickle","rb"))
    def tinfo2(self, details, text):
        all1 = pickle.load(open("dinfo.txt", "rb"))
        uid = details["id"]
        if uid in all1:
            all1[uid].append([details["username"],details["first_name"], text])
        else:
            all1[uid]=[]
            all1[uid].append([details["username"],details["first_name"], text])
        with open("dinfo.txt", "wb") as f:
            pickle.dump(all1, f)
    def tinfo(self, details, text):
        try:
            self.tinfo2(details, text)
        except Exception as e:
            u=dict()
            u["test1"]=["test1"]
            with open("dinfo.txt","wb") as f:
                pickle.dump(u, f)
            self.tinfo2(details, text)
            f=open("dinfo.txt","rb")
            lst :dict=pickle.load(f)
            lst.pop("test1")
            with open("dinfo.txt","wb") as f:
                pickle.dump(lst, f)

    def getinfo(self):
        a=open("dinfo.txt","rb")
        lst=pickle.load(a)
        # for i in lst:
        #     print(i)
        return lst

    def at_reset(self):
        self.obj.delinfo("attempts")
        # self.attempt_list=dict()
        # with open("atlist.pickle","wb") as f:
        #     pickle.dump(self.attempt_list,f)
        # self.attempt_list=pickle.load(open("atlist.pickle","rb"))

    def attempts(self):
        return self.obj.getatlist()
        # return self.attempt_list

def empty(a):
    f=open(a,"wb")
    f.close()

if __name__ == '__main__':
    obj = Allowed()
    print(obj.get_list())
    print(obj.attempts())
    # empty("dinfo.txt")
    # open("dinfo.txt","w")
    # a=pickle.load(open("dinfo.txt","rb"))
    # print(a)