'''
Created on Dec 22, 2014

@author: Panzz
'''
from seed import buildSeed

class tsdDaily(buildSeed):
    
    def __init__(self):
        pass
    
    def crawlFrontierL2(self, currentQuery):
        baseURL = "http://www.thesundaily.my"
        seedURL = "http://www.thesundaily.my" # Where the seed links are located
        xpath = "//div[@id='primary']//ul//li//a"
        
        date      = currentQuery.split('-') # date
        pageExists = 1
        page = 0
        
        allReturnedURL = list()
        allCatURL = list()
        catCount = 0
        
        date = currentQuery.split('-') # date
        
        allCatURL = buildSeed.crawlFrontierL1(self, currentQuery, baseURL, xpath, seedURL)
        
        print("Found %d categories" % len(allCatURL))     
        
        for catURL in allCatURL:
                
                articleURL = catURL[0]
                articleCount = 0
                category = catURL[2]
                
                while page < 5:
                    doc = buildSeed.retrieveSource(self, articleURL + "?page=" + str(page))                
                                
                    for returnedArticleUrl in doc.xpath('//div[@class="view-content"]//h2[@class="node-title"]//a') :
                        
                        url = baseURL + str(returnedArticleUrl.attrib.get('href')) # Getting attribute value
    
                        allReturnedURL.append([url, str(returnedArticleUrl.text_content()), category, str(date[0]) + str(date[1]) + str(date[2]) ] )
                        
                        articleCount += 1
                        
                    catCount += 1
                    
                    #if len(allReturnedURL) == 100:
                    #    break
                    page += 1
                    print("Collecting articles for category %s, page %d, total %d." % (category, page, len(allReturnedURL)))
                
        return allReturnedURL
    
def buildCrawlFrontier(currentQuery):
    
    allReturnedURL = list()
    
    tsdCrawlFrontier = tsdDaily()
    
    allReturnedURL = tsdCrawlFrontier.crawlFrontierL2(currentQuery)
    
    return allReturnedURL
    
def cleanResultFile(seedURL):
    
    tsdCrawlFrontier = tsdDaily()
    
    tsdCrawlFrontier.doc = tsdCrawlFrontier.retrieveSource(seedURL)
    
    if tsdCrawlFrontier.doc == "":
        return ""

    text = tsdCrawlFrontier.doc.xpath('//div[@id="content"]//div[@class="content"]//p')
    articleAuthorList = tsdCrawlFrontier.doc.xpath('//div[@class="submitted"]//div[@class="article-byline"]')
    articleDateList = tsdCrawlFrontier.doc.xpath('//div[@class="submitted"][1]')
    articleKeywordsList = ""
    
    dateFormat = "Posted on %d %B %Y - %I:%M%p"
    
    return tsdCrawlFrontier.extractContent(articleAuthorList, articleKeywordsList, articleDateList, dateFormat, text)
    
    