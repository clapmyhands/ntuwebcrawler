'''
Created on Dec 22, 2014

@author: Panzz
'''
from seed import buildSeed

class beritasatu(buildSeed):

    def __init__(self):
        pass

    def crawlFrontierL2(self, currentQuery):
        baseURL = "http://sp.beritasatu.com"
        seedURL = "http://sp.beritasatu.com/pages/archive/index.php" # Where the seed links are located
        xpath = "//div[@class='midRedBarArc']//table//tr//td//a"

        allReturnedURL = list()

        date = currentQuery.split('-') # date

        allReturnedURL = buildSeed.crawlFrontierL1(self, currentQuery, baseURL, xpath, seedURL + "?year=" + date[2] + '&month=' + date[1] + '&day=' + date[0])

        return allReturnedURL


def buildCrawlFrontier(currentQuery):

    allReturnedURL = list()

    beritasatuCrawlFrontier = beritasatu()

    allReturnedURL = beritasatuCrawlFrontier.crawlFrontierL2(currentQuery)

    return allReturnedURL

def cleanResultFile(seedURL):

    beritasatuCrawlFrontier = beritasatu()

    beritasatuCrawlFrontier.doc = beritasatuCrawlFrontier.retrieveSource(seedURL)

    if beritasatuCrawlFrontier.doc == "":
        return ""

    text = beritasatuCrawlFrontier.doc.xpath('//div[@id="bodytext"]/p')
    articleKeywordsList = beritasatuCrawlFrontier.doc.xpath('//meta[@name="keywords"]')
    articleDateList = beritasatuCrawlFrontier.doc.xpath('//div[@id="contentwrapper"]/p/span[@class="caption"]')
    articleAuthorList = ""

    dateFormat = " %d %B %Y "

    return beritasatuCrawlFrontier.extractContent(articleAuthorList, articleKeywordsList, articleDateList, dateFormat, text)
