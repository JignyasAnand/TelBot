from telegram.ext import *
from telegram.update import Update
import pickle
import Files
import Keys
import Keys as keys
import Responses as R
import requests
import telegram
import Files as F
import os

import sqlinit
from wlist import Allowed
import Comlist
import base as interact
import sqlpickle

usrobj = Allowed()
sobj=sqlpickle.sqlp()
sqli=sqlinit.sqlop()
print("Bot Started")

bot = telegram.Bot(token=keys.API_KEY)


def usr_check(update: Update):
    uid=update.message.from_user["id"]
    if (uid in usrobj.get_list()):
        if uid!=Keys.U_ID:
            usrobj.tinfo(update.message.from_user, update["message"]["text"])
        return True
    usrobj.add_attempt(uid,get_name(update))
    usrobj.tinfo(update.message.from_user, update["message"]["text"])
    err_rep(update)
    # send_attempt(update)
    return False

def guest(update: Update, context: CallbackContext):
    if usr_check(update)==True:
        ele=update.message.text.split(" ")
        if len(ele)==3:
            uname, passw=ele[1], ele[2]
            sobj.addguest(uname, passw, update.message.from_user["id"])
            interact.erplog(update.message.from_user["id"])
        else:
            q=ele[1]
            if q=="minclasses":
                id_message(update.message.from_user["id"],"Starting...Please wait")
                ret = interact.gmethod(4)
                print(ret)
                for i in ret:
                    id_message(update.message.from_user["id"]," | ".join(str(j) for j in i))
                    # priv_message(i+" "+str(ret[i]))
                id_message(update.message.from_user["id"], "END")
            elif q=="att":
                mid=update.message.from_user["id"]
                id_message(mid, "Calculating...Please wait")
                ret=interact.gmethod(3)
                for i in ret:
                    id_message(mid, f"{i[0]} | {i[1]} | {i[2]}")
                id_message(mid, "END")
            elif q=="estclasses":
                mid=update.message.from_user["id"]
                id_message(mid, "Calculating...Please wait")
                ret=interact.calc_classes(1)
                id_message(mid, ret)
                # if len(ret)==0:
                #     id_message(id, "minimum requirements are satisfied")
                #     return
                # for i in ret:
                #     id_message(mid, i+"   "+str(ret[i]))
                id_message(mid, "END")
            elif q=="logout":
                interact.gmethod("logout")


def err_rep(update: Update):
    update.message.reply_text("You are not authorized.")

def rep(update: Update,text):
    update.message.reply_text(text)

def id_message(uid, text):
    bot.send_message(chat_id=uid, text=text)

def to_all(text):
    for i in usrobj.get_list():
        id_message(i, text)

def getcap(update : Update, context : CallbackContext):
    q=update.message.text.split(" ")
    print(q[1])
    sobj.updateinfobyid(update.message.from_user["id"], "captcha", q[1])
    # picklehandler.getinfo()

# def getcreds(update: Update):
#     q=update.message.text
#     q.split(" ")
#     return q[1],q[2]

def priv_p(path):
    bot.send_photo(chat_id=Keys.U_ID, photo=open(path,"rb"))


def id_photo(uid,path=f"{Keys.TEST_PATH}"):
    bot.send_photo(chat_id=uid, photo=open(path,"rb"))

def send_attempt(update:Update):
    info = update.message.from_user
    bot.send_message(chat_id=keys.U_ID,text="Attempted Usage")
    bot.send_message(chat_id=keys.U_ID,text="{} {}".format(info["first_name"],info["last_name"]))
    bot.send_message(chat_id=keys.U_ID,text="u_name : {} id : {}".format(info["username"],info["id"]))

def priv_message(message):
    bot.send_message(chat_id=keys.U_ID,text=message)

def start(update: Update,context):
    if usr_check(update)==True:
        rep(update,"Hello {}".format(update.message.from_user["last_name"]))


def send_doc(update: Update, context: CallbackContext):
    if (usr_check(update)==True):
        fname=str(update.message.text[7:])
        files=F.ret_loc(fname)
        for i in files:
            if os.path.isdir(i):
                continue
            doc=open(i,"rb")
            # isd=update.callback_query.message.chat_id
            context.bot.sendDocument(update.message.from_user["id"],doc)
            doc.close()
        # print(update.message.document.file_id)
        rep(update,"End")



def doc_downloader(update: Update, context: CallbackContext):
    if (usr_check(update)==True):
        fname = update.message.document.file_name
        path=keys.R_PATH+fname
        context.bot.get_file(update.message.document).download(custom_path=path)
        print(update.message.document.file_id)
        rep(update,"Successfully uploaded")



def handle(update, context):
    if (usr_check(update)==True):
        text=str(update.message.text).lower()
        resp = R.sample(text)
        update.message.reply_text(resp)

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def etable():
    priv_message("Starting...Please wait")
    dts=interact.gmethod(1)
    # dts=interact.gmethod(1)
    # dts=ERP_S.interact.gmethod(1)
    for i in dts:
        resp=i+" "+str(dts[i])
        priv_message(resp)
    priv_message("END")
#
# def cclasses():
#     priv_message("Starting...Please wait")
#     tab=interact.gmethod(2)
#     if tab==[]:
#         priv_message("Minimum requirement satisfied")
#     for i in tab:
#         priv_message(i+" "+str(tab[0]))
#     priv_message("END")
def minclasses():
    priv_message("Starting...Please wait")
    ret=interact.gmethod(3)
    print(ret)
    for i in ret:
        priv_message(" | ".join(str(j) for j in i))
        # priv_message(i+" "+str(ret[i]))
    priv_message("END")
def direct(a):
    interact.gmethod(a)
def elog():
    interact.erplog(0)
def clear(update: Update, context:CallbackContext):
    a=sobj.checkusrbyid(update.message.from_user["id"])
    if a==True:
        id_message(update.message.from_user["id"], "Found a record. Deleting your data...")
        sobj.delusr(update.message.from_user["id"])
        id_message(update.message.from_user["id"], "Deleted your data.")

    else:
        id_message(update.message.from_user["id"],"Your data is not present in the server")
    usrobj.tinfo(update.message.from_user, update["message"]["text"])
def adminfunc(update: Update, context: CallbackContext):
    if (update.message.from_user["id"]==keys.U_ID):
        fname = str(update.message.text[3:])
        conts=fname.split(" ")
        if conts[0].lower()=="add":
            usrobj.add_usr(int(conts[1]))
            rep(update,"Added UID : {}".format(conts[1]))
            id_message(conts[1],"You are now authorized.")
        elif conts[0].lower()=="ttable":
            interact.get_ttable()
        elif conts[0]=="testphoto":
            id_photo(update.message.from_user["id"])
        elif conts[0].lower()=="rem":
            usrobj.rem_usr(int(conts[1]))
            rep(update, "Removed UID : {}".format(conts[1]))
            id_message(conts[1],"Authorization expired")
        elif conts[0]=="lsfs":
            lst = Files.ret_loc_all()
            rep(update,lst)
        elif conts[0]=="allusers":
            ulist=[str(i) for i in usrobj.get_list()]
            rep(update,"\n".join(ulist))
        elif conts[0]=="attempts":
            print(usrobj.attempts())
        elif conts[0]=="all":
            to_all(" ".join(conts[1:]))
        elif conts[0]=="pm":
            id_message(conts[1], " ".join(conts[2:]))
        elif conts[0]=="attemptsls":
            ldict=usrobj.attempts()
            ulist=[]
            if len(ldict)==0:
                priv_message("No attempts")
            else:
                print(ldict)
                for i in ldict:
                    print(ldict[i][0],ldict[i][1])
                    ulist.append(str(i)+" : "+str(ldict[i][0])+" - "+str(ldict[i][1]))
                priv_message("\n".join(ulist))
        elif conts[0]=="commands":
            priv_message("\n".join(Comlist.commands))
        elif conts[0]=="erpin":
            elog()
        elif conts[0]=="allmsgs":
            a=usrobj.getinfo()
            if conts[1]=="1":
                for i in a:
                    priv_message(i)
                    for j in a[i]:
                        priv_message(j)
            else:
                t = open("temp.txt", "w")
                for i in a:
                    t.write("ID - "+str(i)+"\n")
                    count=1
                    for j in a[i]:
                        t.write(f"{count} - {j}\n")
                        count+=1
                    t.write("\n")
                t.close()
                context.bot.sendDocument(Keys.U_ID, open("temp.txt","rb"))
        elif conts[0]=="dm":
            try:
                ele=int(conts[1])
            except:
                ele=conts[1]
            direct(ele)
        else:
            rep(update,f"Hey {Keys.name}")
    else:
        rep(update, f"This command works only for {Keys.name}.")

def get_name(update: Update):
    fname,lname= update.message.from_user["first_name"],update.message.from_user["last_name"]
    if (lname==None):
        return fname
    return fname+" "+lname

# def samp1(update: Update, context: CallbackContext):
    #buttons=[[""]]
    # update.message.reply_text("This is a function", reply_markup=telegram.ReplyKeyboardRemove())
    # update.message.reply_text("This is a function", reply_markup=telegram.ReplyKeyboardMarkup(buttons, one_time_keyboard=True))


    # kb = [[telegram.KeyboardButton('/command1')],
    #       [telegram.KeyboardButton('/command2')]]
    # kb_markup = telegram.ReplyKeyboardMarkup(kb)
    # bot.send_message(chat_id=update.message.chat_id,
    #                  text="your message",
    #                  reply_markup=kb_markup)