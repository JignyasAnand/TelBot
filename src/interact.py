import collections
import pickle
import threading
from selenium.webdriver.chrome.options import Options
import Keys
import picklehandler
import dispcookies
from selenium.webdriver.chrome.service import Service
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import math
import time
import mainfuncs2 as mainfuncs
import sys

lstatus=0
driver=-1
ckobj=-1
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
def erplog(b=0):
    # mainfuncs.priv_message("Logging in")
    t1 = threading.Thread(target=login, args=(b, ))
    t1.start()

def gmethod(a,b=0):
    if a==1:
        print(get_ttable(1))
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
        # lstatus=0
        driver.quit()
        mainfuncs.priv_message("Logged out")

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
        s2.select_by_index(Keys.SEMID)
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
        sel2.select_by_index(Keys.SEMID)
        driver.find_element(By.XPATH,'//*[@id="w0"]/div/div[3]/button[1]').click()
        time.sleep(2)
        tbl=driver.find_element(By.XPATH,'/html/body/div[1]/div[4]/div/div/div[2]/div/div/div/div/table/tbody')
        trs=tbl.find_elements(By.TAG_NAME,"tr")
        subdict=dict()
        c=0
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
                # print("ele = ",ele)
                if ele=="-":
                    continue
                if ele[-1]=="-":
                    ele=ele[:8]
                if ele in subdict[tds[0].text]:
                    subdict[tds[0].text][ele]+=1
                else:
                    subdict[tds[0].text][ele]=1
        with open("tables.txt","wb") as f:
            pickle.dump(subdict,f)
        # for i in subdict:
        #     print(i,subdict[i])
        if (mode==1):
            return subdict
    except Exception as e:
        print(e)

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
    lb = driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div/div/nav/div/div[2]/ul/li/form/button")
    lb.click()


def login(mode=0):
    # global lstatus, driver, ckobj
    global driver, ckobj
    if mode==0:
        mainfuncs.priv_message("Logging in")
    else:
        mainfuncs.id_message(picklehandler.guestp("tid"), "Logging in")
    # if lstatus==1:
    #     return
    if mode==0:
        obj=bufcreds(f"{Keys.Student_ID}",picklehandler.getpart(f"{Keys.Student_ID}"))
    else:
        # time.sleep(30)
        # obj=bufcreds(picklehandler.getguest("uname"), passw=picklehandler.getguest("password"))
        obj=bufcreds(picklehandler.guestp("uname"), passw=picklehandler.guestp("password"))
    driver=startdriver()
    ckobj = dispcookies.CookieHandler(driver)
    driver.get("https://newerp.kluniversity.in")
    lgim = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div/div/section/div/ul/li[1]/div/div/div/a")
    lgim.click()
    time.sleep(4)
    # ckobj.display()
    if mode==0:
        ckobj.editc("PHPSESSID", picklehandler.getpart(f"{Keys.Student_ID}"))
    driver.refresh()
    indic = 1
    while (indic):
        try:
            try:
                driver.find_element(By.ID, "loggedIn")
                if mode==0:
                    picklehandler.updateinfo(f"{Keys.Student_ID}", sess=driver.get_cookie("PHPSESSID")["value"])
                indic = 0
                print("Logged in")
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
            un=obj.getuname()
            uname_inp.send_keys(un)
            uname_pass = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/form/div[2]/input")
            if mode==0:
                uname_pass.send_keys(picklehandler.getpart(un, part="password"))
            else:
                uname_pass.send_keys(obj.getpass())
            driver.find_element(By.XPATH,"/html/body/div[3]/div/div/div[2]/div/div/div/form/div[3]/label/input").click()
            driver.save_screenshot("capt.png")
            if mode==0:
                mainfuncs.priv_p("capt.png")
            else:
                mainfuncs.send_p("capt.png")
            time.sleep(15)
            captcha = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/form/div[4]/input")
            # if mode==0:
            captcha.send_keys(picklehandler.getcap(f"{Keys.Student_ID}"))
            # else:
            #     captcha.send_keys(picklehandler.guestcap(mode=1))
            # captcha.send_keys(input("Enter the captcha : "))
            driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/form/div[7]/button").click()
            if mode==0:
                picklehandler.updateinfo(f"{Keys.Student_ID}", sess=driver.get_cookie("PHPSESSID")["value"])
                picklehandler.addcap(f"{Keys.Student_ID}", "None")
            time.sleep(4)

    # lstatus=1
    if mode==0:
        mainfuncs.priv_message("Logged in")
    else:
        mainfuncs.id_message(picklehandler.guestp("tid"), "Logged in")
    # threading.Event()._stop().set()