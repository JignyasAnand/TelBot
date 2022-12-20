import selenium.webdriver.chrome.webdriver

class CookieHandler:
    def __init__(self,driver: selenium.webdriver.chrome.webdriver.WebDriver):
        self.driver=driver
    def getcookies(self):
        return self.driver.get_cookies()
    def display(self):
        cks= self.driver.get_cookies()
        for i in cks:
            print(i)
    def editc(self,cname, cvalue):
        cks=self.getcookies()
        if isinstance(cname,list):
            for i in range(len(cname)):
                for j in cks:
                    if j["name"]==cname[i]:
                        self.driver.delete_cookie(cname[i])
                        j["value"]=cvalue[i]
                        self.driver.add_cookie(j)
                        break
        else:
            for i in cks:
                if i["name"]==cname:
                    self.driver.delete_cookie(cname)
                    i["value"]=cvalue
                    self.driver.add_cookie(i)
                    break

