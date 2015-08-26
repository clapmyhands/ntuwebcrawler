import os
import re
from datetime import *

def getInput():
    newssite = input("Input the news site you want to clean up: ")
    startClean = input("Year-Month-Day to start clean up <strict format>: ")
    amount = int(input("How many files to clean: "))
    startClean = startClean.split('-')
    return [newssite,int(startClean[0]),int(startClean[1]),int(startClean[2]),amount]

def sourceDir(direct,time):
    sourceDir = direct + "/" + str(time.year) + "/" + \
                str(time.month).zfill(2) + "/" + \
                str(time.day).zfill(2) + ".xml"
    return sourceDir

userInput=getInput()
deltatime = timedelta(days=1)

sName = "scripts/output/"
dName = "scripts/output/clean/"
    
def newDir(directory):
    if(os.path.isdir(directory)):
        pass
    else:
        try:
            os.makedirs(directory)
        except OSError:
            pass
newDir(dName)

def writeFile(user_input,amount):
    myTime = date(user_input[1],user_input[2],user_input[3])
    for iter in range(amount):
        fName = sourceDir(userInput[0],myTime)
        readFile =  open(sName+fName,'r',encoding="'utf-8'")
        f = readFile.read().strip()
        readFile.close()

        f = re.sub("\<(.*?)\>"," ",f).strip()
        writeName = fName.split("/",1)[-1].split('.')[0]
        writeName = writeName + ".txt"
        newDir(dName+"/".join(writeName.split('/')[0:-1]))
            
        File = open(dName+writeName,'w',encoding="'utf-8'")
        File.write(f)
        File.close()

        myTime += deltatime

writeFile(userInput,userInput[4])
