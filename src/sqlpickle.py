import pickle
import sqlite3

import sqlinit

class sqlp:
    def __init__(self):
        self.obj=sqlinit.sqlop()
        self.conn=sqlite3.connect("MainDB", check_same_thread=False)
    def checkusr(self, uname):
        ret=self.conn.execute(f"select * from users where uid='{uname}';").fetchall()
        if ret==[]:
            return False
        return True
    def checkusrbyid(self, tid):
        ret=self.conn.execute(f"select * from users where tid='{tid}';").fetchall()
        if ret==[]:
            return False
        return True
    def delusr(self, tid):
        self.conn.execute(f"delete from users where tid='{tid}';")
        self.conn.execute("commit;")
    def addguest(self,uname, passw, tid):
        if self.checkusr(uname)==False:
            self.obj.insertf("users",uname,passw, tid)
    def updateinfo(self, uname, part, info):
        self.obj.updatef("users",part, info, uname)
    def updateinfobyid(self, tid, part, info):
        smd=f"update users set {part}='{info}' where tid='{tid}';"
        self.conn.execute(smd)
        self.conn.execute("commit;")
    def getinfo(self, uname, part):
        return self.obj.get_pinfo("users",uname,part)[0][0]
    def allinfo(self, det):
        return self.obj.getinfo("users",det)
    def getuid(self, tid):
        return self.conn.execute(f"select uid from users where tid='{tid}';").fetchall()[0][0]
