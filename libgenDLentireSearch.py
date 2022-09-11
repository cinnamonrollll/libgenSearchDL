# -*- coding: utf-8 -*-
"""
Python script to save every pdf book link of a Libgen search.
Enter desired search and maximum pages wanted.
Save this script and linksDL.py in the same folder.
Selenium requires geckodriver.exe in the same folder.
Every link is saved in libgenLinkBook.txt
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import requests

search = "oxford"
pagesNb = 2

print("starting webdriver\n")
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

print("\nsearching for links")

linkList_2=[]
linkBookFinal=[]
i=0
chunkCn=0
chunkTotal=0

for link in linkBook:
    driver.get(link)
    linkBookPage = driver.find_elements(By.TAG_NAME,'a')
    print("|",end="")
    
    for link in linkBookPage:
        linkList_2.append(link.get_attribute("href"))
        
    for link in linkList_2:
        if "main" in link and "pdf" in link and link not in linkBookFinal:
            linkBookFinal.append(link)
            
print(" {} pdf books found\n".format(len(linkBookFinal)))

for book in linkBookFinal:    
    name = book.split("/")
    file_name=name[-1].replace("%20"," ").replace("%28","").replace("%29","").replace("%2C","").replace("\n","")
    r = requests.get(book, stream = True)
    print("Starting Downloading files, '--' every Mo\n")
    print("{}/{} : {}\n".format(i+1,len(linkBookFinal),file_name))
    with open(file_name,"wb") as pdf:
        i+=1
        for chunk in r.iter_content(chunk_size=1024):
            chunkCn+=1
            # writing one chunk at a time to pdf file
            if chunkCn>1000:
                print(" --",end="")
                chunkCn=0
            if chunk:
                pdf.write(chunk)
                chunkTotal+=1

driver.quit()
print("finished {} downloads, {} Ko total".format(len(linkBookFinal),chunkTotal/1000))


    























