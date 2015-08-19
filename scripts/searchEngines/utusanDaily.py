'''
Created on Dec 22, 2014

@author: Panzz
'''
from seed import buildSeed

class utusanDaily(buildSeed):
    
    def __init__(self):
        pass
    
    def crawlFrontierL2(self, currentQuery):
        baseURL = "http://www.utusan.com.my"
        seedURL = "http://www.utusan.com.my/special/arkib" # Where the seed links are located
        xpath = "//div[@class='menu menuTop menuTwo']//ul//a"
        
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
                
                if category == "terkini" or category == "video":
                    continue
                
                doc = buildSeed.retrieveSource(self, articleURL)                
                
                for returnedArticleUrl in doc.xpath('//div[@class="element teaser"]//h2//a') :
                    
                    url = baseURL + str(returnedArticleUrl.attrib.get('href')) # Getting attribute value

                    allReturnedURL.append([url, str(returnedArticleUrl.text_content()), category, str(date[0]) + str(date[1]) + str(date[2]) ] )
                    
                    articleCount += 1
                    
                catCount += 1
                
                #if len(allReturnedURL) == 100:
                #    break
                
                print("%d Articles for category %d. %s" % (articleCount, catCount, category))
                
        return allReturnedURL
    
    
def buildCrawlFrontier(currentQuery):
    
    allReturnedURL = list()
    
    utusanCrawlFrontier = utusanDaily()
    
    allReturnedURL = utusanCrawlFrontier.crawlFrontierL2(currentQuery)
    
    return allReturnedURL
    
def cleanResultFile(seedURL):
    
    utusanCrawlFrontier = utusanDaily()
    
    utusanCrawlFrontier.doc = utusanCrawlFrontier.retrieveSource(seedURL)
    
    if utusanCrawlFrontier.doc == "":
        return ""
    
    text = utusanCrawlFrontier.doc.xpath('//div[@class="element article"]//div[@class="articleBody"]//p[@style="BD Bodytext" or @style="BD Body Text" or @style="BD Text"]')
    articleKeywordsList = utusanCrawlFrontier.doc.xpath('//meta[@name="keywords"]')
    articleAuthorList = utusanCrawlFrontier.doc.xpath('//div[@class="element article"]//div[@class="dateLine"]//span[@class="author"]')
    articleDateList = utusanCrawlFrontier.doc.xpath('//div[@class="element article"]//div[@class="dateLine"]//span[@class="date"]')
    
    dateFormat = "%d %B %Y %I:%M %p"
    
    return utusanCrawlFrontier.extractContent(articleAuthorList, articleKeywordsList, articleDateList, dateFormat, text)
    
    