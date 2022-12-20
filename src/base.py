import collections
import pickle
import threading
from selenium.webdriver.chrome.options import Options
import Keys
import mainfuncs2
import sqlpickle as picklehandler
import dispcookies
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import math
import time
from collections import defaultdict
import mainfuncs2 as mainfuncs

lstatus=0
driver=-1
ckobj=-1
als=0
cap=""
cur_id=""
pkobj=picklehandler.sqlp()

class bufcreds:
    def __init__(self, name, passw):
        self.username=name
        self.passw=passw
        self.captcha=""
    def getuname(self):
        return self.username
    def getpass(self):
        return self.passw
    def getcap(self):
        return self.captcha
    def setuname(self,name):
        self.username=name
    def setpass(self,passw):
        self.passw=passw
    def setcap(self,cap):
        self.captcha=cap

# ==========================================================================================================================================================================
def erplog(uid):
    # mainfuncs.priv_message("Logging in")
    t1 = threading.Thread(target=login, args=(uid, ))
    t1.start()

def gmethod(a,b=0):
    if a==1:
        return get_ttable(1)
        # return get_ttable()
    elif a==2: # return which days to attend
        b=calc_classes(1)
        return b
    elif a==3: # returns current percetage along with min no.of classes to attend
        # print(calc_attendance())
        b=calcmin(calc_attendance(),1)
        return b
    elif a==4: # return how many days the periods can be skipped along with maintaining minimum attendance
        return calc_skip(calc_attendance())
    elif a=="logout":
        logout()
        # lstatus=0
        # driver.quit()
        # mainfuncs.priv_message("Logged out")

def calc_skip(a):
    ele=[]
    for i in a:
        calc = ((100*a[i][1])-(85*a[i][0]))//85
        ele.append([f"({i})-[{str(calc)} classes]"])
    return ele

def calc_attendance():
    try:
        driver.get("https://newerp.kluniversity.in/index.php?r=studentattendance%2Fstudentdailyattendance%2Fsearchgetinput")
        driver.maximize_window()
        time.sleep(2)
        s1 = Select(driver.find_element(By.ID,"dynamicmodel-academicyear"))
        s1.select_by_visible_text("2022-2023")
        s2 = Select(driver.find_element(By.ID,"dynamicmodel-semesterid"))
        s2.select_by_index(1)
        driver.find_element(By.XPATH,"/html/body/div[1]/div[4]/div/div/div[2]/div/div/form/div/div[4]/button[1]").click()
        time.sleep(2)
        # table=driver.find_element(By.CSS_SELECTOR,"table table-striped table-bordered")
        table=driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div/div/div[2]/div[1]/div[1]/div/div[1]/table/tbody')
        trs=table.find_elements(By.TAG_NAME,"tr")
        slist=dict()
        subcodes=dict()
        c=0
        for tr in trs:
            if c==5:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            c+=1
            subcode=tr.find_elements(By.TAG_NAME,"td")[1].text
            sub=tr.find_elements(By.TAG_NAME,"td")[2].text
            tot=tr.find_elements(By.TAG_NAME,"td")[8].text
            att=tr.find_elements(By.TAG_NAME,"td")[9].text
            subcodes[subcode]=sub
            if sub in slist:
                slist[sub][0]+=int(tot)
                slist[sub][1]+=int(att)
            else:
                slist[sub]=[int(tot),int(att),subcode]
        with open("subcodes.txt","wb") as f:
            pickle.dump(subcodes,f)
        return slist
    except Exception as e:
        print(e)

def calcmin(atdict,mode=0):
    data=[]
    reqat=dict()
    for i in atdict:
        l=[]
        tot=atdict[i][0]
        att=atdict[i][1]
        cperc=(att/tot)*100
        if cperc>=85:
            resp="Minimum attendance satisfied for now"
        else:
            calc=((0.85*tot)-att)/0.15
            calc=math.ceil(calc)
            resp=f"Need to attend {calc} more classes"
            reqat[atdict[i][2]]=calc
        l.extend([i,str(cperc),resp])
        data.append(l)
        # print(i,f"Current {cperc} |",resp)
    if mode==1:
        return data
    colw = -1
    for i in data:
        tcolw=max(len(j) for j in i)
        colw=max(colw,tcolw)
    colw+=5
    for i in data:
        print("".join(j.ljust(colw) for j in i))
    return reqat




def get_ttable(mode=0):
    try:
        time.sleep(2)
        driver.get("https://newerp.kluniversity.in/index.php?r=timetables%2Funiversitymasteracademictimetableview%2Findexstudentindisearch")
        driver.maximize_window()
        time.sleep(2)
        sel = Select(driver.find_element(By.XPATH,'//*[@id="universitymasteracademictimetableview-academicyear"]'))
        sel.select_by_index(1)
        sel2=Select(driver.find_element(By.XPATH,'//*[@id="universitymasteracademictimetableview-semesterid"]'))
        sel2.select_by_index(2)
        driver.find_element(By.XPATH,'//*[@id="w0"]/div/div[3]/button[1]').click()
        time.sleep(1)
        tbl=driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div/div/div[2]/div/div/div/div/table/tbody')
        trs=tbl.find_elements(By.TAG_NAME,"tr")
        subdict=dict()
        c=0
        sdict=defaultdict(list)
        for tr in trs:
            if (c==3):
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            c+=1
            tds=tr.find_elements(By.TAG_NAME,"td")
            subdict[tds[0].text]=dict()
            # for i in tds:
            #     print(i.text, end=" ")
            # print()
            for i in range(1,len(tds)):
                ele=tds[i].text[:9]
                sdict[tds[0].text].append(ele)
                # print("ele = ",ele)
                if ele=="-":
                    continue
                if ele[-1]=="-":
                    ele=ele[:8]
                if ele in subdict[tds[0].text]:
                    subdict[tds[0].text][ele]+=1
                else:
                    subdict[tds[0].text][ele]=1
        print(sdict)
        if mode==2:
            with open("etable.txt","wb") as f:
                pickle.dump(sdict, f)
            return
        with open("tables.txt","wb") as f:
            pickle.dump(subdict,f)
        # for i in subdict:
        #     print(i,subdict[i])
        if (mode==1):
            return subdict
    except Exception as e:
        print(1,e)

def totleft(a):
    return sum(a[i] for i in a if a[i]>=0)

def calc_classes(mode=0):
    # week_classes=pickle.load(open("tables.txt","rb"))
    week_classes=get_ttable(1)
    cur_req=calcmin(calc_attendance(),1)
    print("cr", cur_req)
    if len(cur_req)==0:
        print("Minimum requirement satisfied")
        return []
    else:
        # cur_req={'21AD2104':4}
        print(week_classes)
        print(cur_req)
        weeks=collections.defaultdict(int)
        while(totleft(cur_req)>0):
            for i in week_classes:
                st=1
                for j in week_classes[i]:
                    if j in cur_req and cur_req[j]>0:
                        cur_req[j]-=week_classes[i][j]
                        st=0
                if st==0:
                    # print(i,week_classes[i],cur_req)
                    weeks[i]+=1
        print("wwww",weeks)
        if mode==1:
            return weeks
        print("Minimum weeks")
        for i in weeks:
            print(i,weeks[i])
        print("----------------------")
        print(f"Maybe you need to attend {max(abs(weeks[i]) for i in weeks)} weeks continuously.")
        print("----------------------")
        print("After completing the above requirements, you will have attended : ")
        for i in cur_req:
            print(f"{i} - {abs(cur_req[i])} extra classes")
def startdriver():
    PATH = f"{Keys.Driver_Path}"
    service = Service(executable_path=PATH)
    copt  =Options()
    copt.add_experimental_option("detach",True)
    driver = webdriver.Chrome(service=service)
    return driver

def logout():
    global als

    driver.quit()
    als=0
    mainfuncs2.id_message(cur_id, "Logged out")
    # lb = driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div/div/nav/div/div[2]/ul/li/form/button")
    # lb.click()


def capcheck(uid):
    global cap
    incap=pkobj.getinfo(uid, "captcha")
    count=0
    while count<1:
        ret=pkobj.getinfo(uid, "captcha")
        if ret==incap:
            time.sleep(3)
        else:
            cap=ret
            count=1

# ==========================================================================================================================================================================

def login(tid):
    """
    sdet:
    0 - uid
    1 - password
    2 - phpsessid
    3 - captcha
    4 - tid
    """
    global driver, ckobj, als, cur_id
    if als==1:
        logout()
        als=0
    uid=pkobj.getuid(tid)
    print("uid - ", uid)
    sdet=pkobj.allinfo(uid)
    print("sdet - ", sdet)
    mainfuncs.id_message(sdet[0][4], "Logging in")

    driver=startdriver()
    ckobj = dispcookies.CookieHandler(driver)
    driver.get("https://newerp.kluniversity.in")
    lgim = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div/div/section/div/ul/li[1]/div/div/div/a")
    lgim.click()
    time.sleep(4)
    # ckobj.display()
    try:
        ckobj.editc("PHPSESSID", pkobj.getinfo(sdet[0][0],"PHPSESSID"))
    except:
        print("User cookie err 1")
    driver.refresh()
    indic = 1
    while (indic):
        try:
            try:
                driver.find_element(By.ID, "loggedIn")
                cur_id=sdet[0][4]
                pkobj.updateinfo(sdet[0][0],"PHPSESSID", driver.get_cookie("PHPSESSID")["value"])
                indic = 0
                print("Logged in")
                als=1
            except:
                indic = 1
                raise Exception
        except:
            # driver.quit()
            driver.close()
            driver = startdriver()
            driver.get("https://newerp.kluniversity.in")
            lgim = driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div/div/div/section/div/ul/li[1]/div/div/div/a")
            lgim.click()
            time.sleep(2)

            uname_inp = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/form/div[1]/input")
            uname_inp.send_keys(sdet[0][0])
            uname_pass = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/form/div[2]/input")
            uname_pass.send_keys(sdet[0][1])

            driver.find_element(By.XPATH,"/html/body/div[3]/div/div/div[2]/div/div/div/form/div[3]/label/input").click()
            driver.save_screenshot("capt.png")

            mainfuncs2.bot.send_photo(Keys.U_ID,open("capt.png", "rb"))
            t1=threading.Thread(target=capcheck, args=(sdet[0][0],))
            t1.start()
            t1.join()
            captcha = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/form/div[4]/input")
            captcha.send_keys(cap)
            driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/form/div[7]/button").click()
            pkobj.updateinfo(sdet[0][0],"PHPSESSID",driver.get_cookie("PHPSESSID")["value"])

            time.sleep(4)

    mainfuncs.id_message(sdet[0][4],"Logged in")
    # threading.Event()._stop().set()

