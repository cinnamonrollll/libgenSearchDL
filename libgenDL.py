# -*- coding: utf-8 -*-
"""
Python script to save every pdf book link of a Libgen search.
Enter desired search and maximum pages wanted.
Save this script and linksDL.py in the same folder.
Selenium requires geckodriver.exe in the same folder.
Every link is saved in libgenLinkBook.txt
"""

import time
print("starting webdriver\n")
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

search = "oxford"
pagesNb = 2

driver = webdriver.Firefox()
driver.get("https://libgen.is/")
elem = driver.find_element(By.ID, "searchform")
elem.clear()
elem.send_keys(search)
elem.send_keys(Keys.RETURN)

linkList=[] #every link
linkBook=[] #every book link

for i in range(pagesNb):
    #stale exception
    for tab in ['answers', 'questions']:
      js = "window.tab = [...document.querySelectorAll('div.tabs > a')].filter(a => a.innerText === '" + tab + "')[0]"
      driver.execute_script(js)
      driver.execute_script("if(window.tab) window.tab.click()")
      time.sleep(1)    
      
    elements = driver.find_elements(By.TAG_NAME,'a')
    
    for element in elements:
        linkList.append(element.get_attribute("href"))  
        
    for link in linkList:
        if "lol" in link and link not in linkBook:
            linkBook.append(link)
    
    if i!=pagesNb-1:
        driver.get("https://libgen.is/search.php?&req=oxford&phrase=1&view=simple&column=def&sort=def&sortmode=ASC&page={}".format(i+2))
    print("page {} done".format(i+1))

print("\nsearching for links\n")
file = open('libgenLinkBook.txt', 'w')
linkList_2=[]
linkBookFinal=[]

for element in linkBook:
    driver.get(element)
    linkBookPage = driver.find_elements(By.TAG_NAME,'a')
    
    for link in linkBookPage:
        linkList_2.append(link.get_attribute("href"))
  
    for link in linkList_2:
        if "main" in link and "pdf" in link and link not in linkBookFinal:
            linkBookFinal.append(link)
            print("writing : {}".format(link))
            print("\n")
            file.write(link)
            file.write("\n")
        
print("{} pdf books found".format(len(linkBookFinal)))
file.close()































