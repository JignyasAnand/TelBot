import mainfuncs2
import sqlinit


sqli=sqlinit.sqlop()

def msgall(mode=0,b=""):
    if mode==0:
        a=input()
        mainfuncs2.to_all(a)
    else:
        mainfuncs2.to_all(b)

def msg(tid, mode=0, msg=""):
    if mode==0:
        a=input()
        mainfuncs2.id_message(tid, a)
    else:
        mainfuncs2.id_message(tid, msg)


if __name__ == '__main__':
    pass