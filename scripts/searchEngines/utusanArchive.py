'''
Created on Dec 22, 2014

@author: Panzz
'''
from seed import buildSeed

class utusanArchive(buildSeed):
    
    def __init__(self):
        pass
    
    def crawlFrontierL2(self, currentQuery):
        baseURL = "http://ww1.utusan.com.my"
        seedURL = "http://ww1.utusan.com.my/utusan/search.asp" # Where the seed links are located
        xpath = "//div[@class='search']//ul//a"
        
        allReturnedURL = list()
        
        date = currentQuery.split('-') # date
        
        allReturnedURL = buildSeed.crawlFrontierL1(self, currentQuery, baseURL, xpath, seedURL + '?paper=um&dd=' + date[0] + '&mm=' + date[1] + '&yy=' + date[2] + '&query=Search&stype=dt')   
                
        return allReturnedURL
    
    
def buildCrawlFrontier(currentQuery):
    
    allReturnedURL = list()
    
    utusanCrawlFrontier = utusanArchive()
    
    allReturnedURL = utusanCrawlFrontier.crawlFrontierL2(currentQuery)
    
    return allReturnedURL
    
def cleanResultFile(seedURL):
    
    utusanCrawlFrontier = utusanArchive()
    
    utusanCrawlFrontier.doc = utusanCrawlFrontier.retrieveSource(seedURL)
    
    if utusanCrawlFrontier.doc == "":
        return ""
    
    text = utusanCrawlFrontier.doc.xpath('//div[@class="fullstory"]//p')
    articleKeywordsList = utusanCrawlFrontier.doc.xpath('//meta[@name="keywords"]')
    articleDateList = utusanCrawlFrontier.doc.xpath('//div[@class="leftcolumn2"]//div[@style="color:maroon"]')
    articleAuthorList = utusanCrawlFrontier.doc.xpath('//div[@class="element article"]//div[@class="dateLine"]//span[@class="date"]')
    
    dateFormat = "ARKIB : %d/%m/%Y"
    
    return utusanCrawlFrontier.extractContent(articleAuthorList, articleKeywordsList, articleDateList, dateFormat, text)
    
    