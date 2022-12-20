import sqlite3
import Keys
import sys
"""Note : 
If you don't know your user ID which is a number, you can first attempt to use the program (which it won't allow).
After attempting, you can see your user ID in the 'attempts' table of the database 'MainDB'.
Then copy your User ID and place it in the 'Keys' module.
After placing it in the 'Keys' Module, run the """

if __name__ == '__main__':
    try:
        num=sys.argv[1]
        conn = sqlite3.connect("MainDB")
        c = conn.cursor()
        if num=='0':
            c.execute("create table users(uid varchar2(20), password varchar2(100), PHPSESSID varchar2(200), captcha varchar2(20), tid varchar2(50));")
            c.execute("create table attempts (uid number, name varchar(200), nums number);")
            c.execute("create table whitelist (uid number);")

            if (Keys.U_ID!=None):
                c.execute(f"insert into whitelist values ('{Keys.U_ID}');")
                c.execute("commit;")
                print("You can start using the program")
            else:
                print("The program is not yet ready to use")
        elif num=="1":
            if Keys.U_ID!=None:
                c.execute(f"insert into whitelist values ('{Keys.U_ID}');")
                c.execute("commit;")
            else:
                print("Please update your user ID in the 'Keys' module")
        else:
            print("Invalid option. Give 0 - Initialize the DB, 1 - Update your User ID into the whitelist")
    except:
        print("You should enter an argument. Try Again.")



# test=f"insert into whitelist values ('{Keys.U_ID}');"
# print(type(test))