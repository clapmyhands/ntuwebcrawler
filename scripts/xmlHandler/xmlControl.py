'''
Created on Oct 1, 2014

@author: Phuah Chee Chong
'''
import xml.etree.ElementTree as ET
import os
from lxml import etree
from xml.dom.minidom import parse, parseString


'''
Creates the XML file if it does not exist.
'''
def createXMLFile(dName, fName, strCurD, strCurM, strCurY, source, currentQuery):
    # ___________ extraction contenu article ______________#
    # If the directory already exists, we skip, otherwiss create it!
    if os.path.isdir(dName) and os.path.isfile(dName + "/" + fName):
        pass
    
    else:
        try:
            if os.path.isdir(dName):
                pass
            
            else:
                os.makedirs(dName)
            # Create the xml file so we may update it later
            f = open( dName + "/" + fName , 'w', encoding="'utf-8'")
    
            f.write('<corpus id="' + strCurD + strCurM  + strCurY + '" source="' + source +'" date="'+ currentQuery + '">')
            f.write('</corpus>')
        
            f.close()
    
        except OSError :
            pass

        
'''
Opens the XML file that is to be processed.
'''
def openXMLFile(dName, fName):
    
    try:
        xmldoc = ET.parse(dName + "/" + fName)
        return xmldoc
    except:
        return -1;
    

'''
Check for existing category, otherwise create it.
'''
def checkCategoryTag(xmldoc, dName, fName, category):
    
    if(xmldoc == -1):
        return None
    
    root = xmldoc.getroot()
    found = 0

    # Find a category with the name already created.
    for cat in root.findall('category'):
        if category == cat.get('name'):
            found = 1
            break
        
    # If no category with the name provides is found, we need to create it!
    if found == 1:
        pass
    else:
        createCatTag = ET.SubElement(root, 'category', {'name': category})
        xmldoc.write(dName + "/" + fName, xml_declaration=True, encoding='utf-8', method="xml")
    
    return root

'''
Check for existing articles, otherwise create it.
'''
def checkArticle(xmldoc, dName, fName, category, url):
    
    if (xmldoc == -1):
        return None;
    
    else:
        UrlNode = xmldoc.getroot()
        categoryNode = UrlNode.find(".//category[@name='" + category + "']")
        
        if categoryNode is not None:
            articleNode = categoryNode.find(".//article[@link='" + url + "']")
        else:
            articleNode = None
               
        return articleNode

'''
Creates an <article> tag and appends data and attributes to it.
'''
def createArticleTag(xmldoc, dName, fName, catNode, articleContent, url, title, author, articleDate, articleKeywords):
    
    
    articleTag = ET.SubElement(catNode, 'article', {'link': url, 'title': title, 'author': author, 'published': articleDate, 'keywords': articleKeywords})
    
    if(articleContent.find("<*p>")):
        for paragraph in articleContent.split("<*p>"):
            pTag = ET.SubElement(articleTag, 'p')
            pTag.text = paragraph
    else:
        articleTag.text = articleContent
        
    xmldoc.write(dName + "/" + fName, xml_declaration=True, encoding='utf-8', method="xml")
    
'''
Reparse the XML document to make it more readable.
'''   
def prettify(elem):
    rough_string = ET.tostring(elem, encoding = "utf-8", method = "xml")
    reparsed = parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

'''
Opens the XML file by removing all previous whitespace characters and calling the prettify function to format it again.
'''
def formatXML(modifiedFiles):
    parserFormat = etree.XMLParser(remove_blank_text=True)
    
    for toFormatFile in modifiedFiles:
        xmldoc = ET.parse(toFormatFile, parserFormat)
        root = xmldoc.getroot()
        
        f = open( toFormatFile  ,'w', encoding = "utf-8")
    
        f.write(prettify(root))
        
        f.close()    
    
'''
Opens the XML done file to correct the starting date.
'''
def updateDoneList(input, source, startDates):
    # Updates the done list
    xmldocRequest = ET.parse(input)
    rootRequest = xmldocRequest.getroot()
    
    queryNode = rootRequest.find('.//query[@source="' + source + '"]')
    queryNode.set('startY', str(startDates.year))
    queryNode.set('startM', str(startDates.month))
    queryNode.set('startD', str(startDates.day))
    xmldocRequest.write(input, xml_declaration=True, encoding='utf-8', method="xml")