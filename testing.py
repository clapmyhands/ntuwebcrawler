"""
USE FUCKING XML TO PARSE THE CLEAN FILE DAMNIT DONT BRUTE FORCE MY UCKING WAY

"""
import re,lxml

dName = "scripts/output/tribun/2015/08"
fName = "02.xml"

oName = "scripts/clean/tribun/2015/08"
ofName = "02.xml"

with open(dName + '/' + fName,'r') as myFile:
  f=myFile.read()

f = re.sub("\<(.*?)\>","",f)
f = re.sub("[\t]+","",f)
f = re.sub("[\n]+","\n",f)
f = re.sub(" +"," ",f)
f = f.split("\n")
for lines in f:
    lines = lines.strip()
for i in range (20):
  print(i,"~",repr(f[i]))

#f = re.sub("[\n]+","\n",f)
#f = re.sub("( )+"," ",f)
