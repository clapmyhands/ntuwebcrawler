'''
Created on Sep 17, 2014

@author: Phuah Chee Chong
'''
# -*- coding: utf-8 -*-
#import urllib2, html5lib
import urllib3, lxml.html, re, requests, xmlrpc, urllib.parse as urlparse, time
from _ast import Str
from scripts.cleaning.cleanText import convertMonthToEnglish
from scripts.htmlHandler.htmlControl import createHTMLFile
###_________________________________________________________________________________####

class buildSeed():
    
    def __init__(self):
        pass
        
    def retrieveSource (self, seedURL):
        
        doc = ""
        count = 1
        
        try:
            seedURL.encode('ascii')
            
        except:
            print("Cannot convert URL to ascii")
            return doc
        
        while True and count < 4:
            try : 
                http = urllib3.PoolManager()
    
                f = http.urlopen('GET', seedURL)
                data = f.data
                f.close()
            
                doc = lxml.html.document_fromstring(data)
                
                createHTMLFile(data, seedURL, doc)
                
            except urllib3.exceptions.HTTPError:
                print("An error occurred, retrying %d" % (count))
                count += 1
                
            break
        
        return doc

    '''
    The required variables are:
        1. The seed (URL)
        2. The xpath to obtain the list of links
        
    '''
        
    def crawlFrontierL1(self, currentQuery, baseURL, xpath, seedURL):
        '''
            input (str="name dd-mm-yyyy-dd-mm-yyyy numberOfPage Key")
            output (list=list of article URL)
            
            at first generates the url for the searche engine using typical patterns
            then realizes a query on Liberation.fr and return the output html5 page to a list
            finally parses the html page to extract links to liberation articles
            
        '''
        self.baseURL = baseURL
        date = currentQuery.split('-') # date
    
    
        allReturnedURL = list()
        
        doc = self.retrieveSource(seedURL)
    
        for returnedUrl in doc.xpath(xpath) :
            
            # return the search page in the form of [url, title, category, published date]
            if "http" in str(returnedUrl.attrib.get('href')):
                url = str(returnedUrl.attrib.get('href'))
                
            else:
                url = self.baseURL + str(returnedUrl.attrib.get('href'))
            
            category = urlparse.urlparse(url).path
            category = category.split('/', 4)
            
            if(len(category) < 3):
                continue
            else:
                category = [category[2]]
            
            allReturnedURL.append([url, str(returnedUrl.text_content()), category[0].replace('_', ' '), str(date[0]) + str(date[1]) + str(date[2]) ] )
            
       
        return allReturnedURL
            
    
    def getAuthor(self, articleAuthorList):
        
        author = ""
        for author in articleAuthorList:
                author = author.text_content()
        
        return author
    
    def getKeyword(self, articleKeywordsList):
        
        articleKeywords = ""
        for articleKeywords in articleKeywordsList:
            articleKeywords = articleKeywords.attrib.get('content')
        
        return articleKeywords
    
    def getArticleDate(self, articleDateList, dateFormat):
        
        articleDate = ""
        for articleDate in articleDateList:
            
            try:
                articleDate = convertMonthToEnglish(articleDate.text_content())
                articleDate = time.strptime(articleDate, dateFormat)
                
            except:
                
                articleDate = ""      
        
        return articleDate
    
    def getArticleContent(self, text):
        combinedSentences = ""
        
        for i in text:
                if re.search("<!--", i.text_content()):
                    continue;
            
                combinedSentences = combinedSentences + " " + i.text_content() + "<*p>"
                
        return combinedSentences
    
    def extractContent(self, articleAuthorList, articleKeywordsList, articleDateList, dateFormat, text):
        ''' input : str(one url)
        output : str (utf8 text of the article) 
        '''
        allContentInfo = list()
 
        author = self.getAuthor(articleAuthorList)
        articleKeywords = self.getKeyword(articleKeywordsList)
        articleDate = self.getArticleDate(articleDateList, dateFormat)
        combinedSentences = self.getArticleContent(text)
        
        allContentInfo.append([combinedSentences, author, articleDate, articleKeywords])
            
        return allContentInfo

        
    
    

