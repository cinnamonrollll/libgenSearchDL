# -*- coding: utf-8 -*-
"""
Python script to download every file from links saved in libgenLinkBook with libgenDL.py.
"""

import requests

i=0
chunkCn=0
chunkTotal=0
file = open('libgenLinkBook.txt', 'r')
lines = file.readlines()

print("\nStarting Downloading files, '--' every Mo")
for line in lines:
    name = line.split("/")
    file_name=name[-1].replace("%20"," ").replace("%28","").replace("%29","").replace("%2C","").replace("\n","")
    r = requests.get(line, stream = True)
    print("\n")
    print("{}/{} : {}\n".format(i+1,len(lines),file_name))
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

print("finished {} downloads, {} Ko total".format(len(lines),chunkTotal/1000))
