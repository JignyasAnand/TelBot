import sqlite3
import wlist
import picklehandler

class sqlop:
    def __init__(self):
        self.conn=sqlite3.connect("MainDB",check_same_thread=False)
        self.select="select * from "
        self.selectp="select {} from {} "
        self.insert="insert into {} values "
        self.delete="delete from {}"
        self.update="update {} set "
    def remusr(self,uid):
        smd=self.delete.format("whitelist")+f" where uid={uid};"
        print(smd)
        self.conn.execute(smd)
        self.conn.execute("commit;")
    def insertf(self, tname, *args):
        # print(tname)
        # print(args)
        smd=""
        if tname=="attempts":
            args=list(args)
            ats=self.conn.execute(f"select * from attempts where uid={args[0]};").fetchall()
            print(ats)
            if ats==[]:
                args[1] = f"\"{args[1]}\""
                smd = self.insert.format(tname) + "(" + ",".join(str(i) for i in args) + ",1 );"
            else:
                smd=self.update.format(tname)+f"nums={ats[-1][-1]+1} where uid={ats[0][0]};"
        elif tname=="whitelist":
            smd=self.insert.format(tname)+f"({args[0]});"
        elif tname=="users":
            smd=self.insert.format("users (uid, password, tid)")+f"('{args[0]}', '{args[1]}','{args[2]}');"
        self.conn.execute(smd)
        self.conn.execute("commit;")
        return smd
    def updatef(self, tname,part, val, uid):
        if tname=="users":
            smd=self.update.format(tname)+f"{part}='{val}' where uid={uid};"
        self.conn.execute(smd)
        self.conn.execute("commit;")
    def get_pinfo(self, tname, uname, part):
        if tname=="users":
            smd=self.selectp.format(part, tname)+f"where uid={uname};"
        return self.conn.execute(smd).fetchall()
    def getwlist(self):
        com=self.select+"whitelist;"
        ret= self.conn.execute(com).fetchall()
        ret1=[]
        for i in ret:
            ret1.append(i[0])
        return ret1
    def getatlist(self):
        com=self.select+"attempts;"
        ret= self.conn.execute(com).fetchall()
        ret1=dict()
        for i in ret:
            ret1[i[0]]=[i[1],i[2]]
        return ret1
    def getinfo(self, name, det):
        com=self.select+name+f" where uid={det};"
        ret=self.conn.execute(com).fetchall()
        return ret
    def delinfo(self, name):
        smd=self.delete.format(name)+";"
        print(smd)
        self.conn.execute(smd)
        # self.commit
        self.conn.execute("commit;")

if __name__ == '__main__':
    conn=sqlite3.connect("MainDB", check_same_thread=False)

    # obj=wlist.Allowed()
    # wl=obj.get_list()
    # ats=obj.attempts()
    # smd = "insert into whitelist values "
    # atc = "insert into attempts values "
    # wget="select * from whitelist;"
    #
    # ln=len(wl)
    # count=0
    # for i in wl:
    #     if count!=ln-1:
    #         smd+=f"({i}),"
    #     elif count==ln-1:
    #         smd+=f"({i});"
    #     count+=1
    # print(smd)
    # # conn.execute(smd)
    # # conn.execute("commit;")
    # # print(conn.execute(wget).fetchall())
    #
    # count=0
    # ln=len(ats)
    # for i in ats:
    #     if count!=ln-1:
    #         atc+=f"({i},\"{ats[i][0]}\", {ats[i][1]}),"
    #     else:
    #         atc+=f"({i},\"{ats[i][0]}\", {ats[i][1]});"
    #     count+=1
    # print(atc)
    # conn.execute(atc)
    # conn.execute("commit;")
    obj=sqlop()
    print(obj.getwlist())
    print(obj.getatlist())
    # print(obj.insertf("whitelist",123, "hello"))
    # obj.delinfo("test")
    smd="insert into users values "
    obj=picklehandler.getinfo()
    for i in obj:
        smd+=f"('{i}',"
        for j in obj[i]:
            smd+=f"'{obj[i][j]}',"
        smd=smd[:-1]+");"
    print(smd)
    conn.execute(smd)
    conn.execute("commit;")