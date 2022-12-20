import os
import Keys

def ret_loc(name):
    files=os.listdir(f"{Keys.R_PATH}")
    noted=[]
    for i in files:
        if name in i:
            noted.append(i)
    for i in range(len(noted)):
        noted[i]=Keys.PATH+"/"+noted[i]
    return noted

def ret_loc_all():
    cfiles = os.listdir(Keys.R_PATH)
    final = "\n".join(cfiles)
    return final


if __name__ == '__main__':
    ret_loc("cf")