import pickle

import Keys
import sqlinit


def updateinfo(uid,pw=None,sess=None, cap=None):
    st=getinfo()
    if pw!=None and sess!=None:
        st[str(uid) if isinstance(uid, int) else uid]["password"]= pw
        st[str(uid) if isinstance(uid, int) else uid]["PHPSESSID"]= sess
    elif sess!=None:
        st[str(uid) if isinstance(uid, int) else uid]["PHPSESSID"]= sess
    elif pw!=None:
        st[str(uid) if isinstance(uid, int) else uid]["password"]= pw

    with open("creds.txt","wb") as fh:
        pickle.dump(st,fh)
def addcap(uid, cap):
    st=getinfo()
    st[str(uid)]["captcha"]=cap
    with open("creds.txt","wb") as fh:
        pickle.dump(st,fh)
    print("efdv")

def getcap(uid):
    st=getinfo()
    if "captcha" in st[str(uid)]:
        return st[str(uid)]["captcha"]
    else:
        return None
def addinfo(uid,pw,sess):
    st=getinfo()
    st[str(uid) if isinstance(uid, int) else uid]={"password":pw, "PHPSESSID":sess}
    with open("creds.txt","wb") as fh:
        pickle.dump(st, fh)
def getinfo():
    floc=open("creds.txt","rb")
    udict=pickle.load(floc)
    return udict

def getpart(uid,part="PHPSESSID"):
    info=getinfo()
    return info[str(uid) if isinstance(uid, int) else uid][part]

def check(uname):
    info=getinfo()
    if str(uname) in info:
        return True
    return False

def pickleread(name):
    info=pickle.load(open(name,"rb"))
    print(info)

def addguest(uname, passw):
    st=dict()
    st[uname]={"password":passw}
    with open("guest.txt","wb") as f:
        pickle.dump(st, f)
def adp(a, b):
    st=pickle.load(open("guest.txt","rb"))
    fele=list(st.keys())[0]
    st[fele][a]=b
    with open("guest.txt","wb") as f:
        pickle.dump(st, f)
def guestp(part):
    st=pickle.load(open("guest.txt","rb"))
    ele=list(st.keys())[0]
    if part=="uname":
        return ele
    return st[ele][part]
def guestcap(mode=0, cap=0):
    if mode==1:
        st=pickle.load(open("guest.txt","rb"))
        return st["captcha"]
    else:
        st=pickle.load(open("guest.txt","rb"))
        fele = list(st.keys())[0]
        st[fele]["captcha"]=cap
        with open("guest.txt","wb") as f:
            pickle.dump(st, f)

def sqlgetinfo(det,uname="users"):
    ret=sqlinit.sqlop().getinfo(uname,det)
    print(ret)

if __name__ == '__main__':
    print(getinfo())
    print(getpart(f"{Keys.Student_ID}"))
    pickleread("guest.txt")
    sqlgetinfo("users",f"{Keys.Student_ID}")
    # pickleread("creds.txt")
    # pickleread("tables.txt")