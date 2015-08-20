'''
Created on Mar 9, 2015

@author: Panzz
'''
import os
import re
'''
Creates the HTML file with original data.
'''


def createHTMLFile(data, seedURL, doc):
    # ___________ extraction contenu article ______________#
    # If the directory already exists, we skip, otherwiss create it!

    source = seedURL.split("/",4)[-1]
    source = re.sub('[^A-Za-z0-9]+', '', source)
    dName = "output/allHTML/" + source
    title = doc.xpath('//title/text()')
    fName = title[0][:255]

    fName = re.sub('[^A-Za-z0-9]+', '', fName)
    fName = fName + ".html"

    htmlContent = data.decode('iso-8859-15')

    if os.path.isdir(dName):
        pass

    else:
        try:
            os.makedirs(dName)

        except OSError:
            pass

    f = open(dName + "/" + fName, 'w', encoding="'utf-8'")
    f.write(htmlContent)
    f.close()
