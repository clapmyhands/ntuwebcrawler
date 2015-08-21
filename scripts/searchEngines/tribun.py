'''
Created on Aug 21, 2015

@author: StefanSetyadiTjeng / clapmyhands
added pagination system
'''
from seed import buildSeed
from lxml import html
from urllib3 import PoolManager

class tribun(buildSeed):

    def __init__(self):
        pass

    def crawlFrontierL2(self, currentQuery):
        baseURL = "http://www.tribunnews.com"
        # Where the seed links are located
        seedURL = "http://www.tribunnews.com/index-news/"
        xpath = '//li[@class="ptb15"]/div[contains(@class,"f16") and contains(@class,"fbo")]/a'

        #pagings system
        tempHTML = PoolManager().urlopen('GET',seedURL)
        tempDoc = html.document_fromstring(tempHTML.data)
        tempHTML.close()
        last_page = tempDoc.xpath('//div[@id="paginga"]/div[contains(@class,"paging")]/a[last()]/@href')[0]
        last_page=int(last_page.split('=')[-1])

        allReturnedURL = list()

        #currentQuery is suited to tribun archive query
        for iterator in range(last_page):
            try:
                allReturnedURL.extend(buildSeed.crawlFrontierL1(
                    self, currentQuery, baseURL, xpath, seedURL + "?date=" + currentQuery + "&page=" + str(iterator+1)))
            except:
                allReturnedURL = buildSeed.crawlFrontierL1(
                    self, currentQuery, baseURL, xpath, seedURL + "?date=" + currentQuery + "&page=1")

        return allReturnedURL


def buildQuery(qYear, qMonth, qDay):
    # used to build specific query for each site archive
    qDate = ""
    try:
        qDate = qYear + '-' + qMonth + '-' + qDay
    except:
        qDate = ""
    return qDate


def buildCrawlFrontier(currentQuery):

    allReturnedURL = list()

    tribunCrawlFrontier = tribun()
    allReturnedURL = tribunCrawlFrontier.crawlFrontierL2(currentQuery)

    return allReturnedURL

def cleanResultFile(seedURL):

    tribunCrawlFrontier = tribun()
    tribunCrawlFrontier.doc = tribunCrawlFrontier.retrieveSource(seedURL)

    if tribunCrawlFrontier.doc == "":
        return ""

    text = tribunCrawlFrontier.doc.xpath('//div[contains(@class,"txt-article") and contains(@class,"side-article")]/p')
    articleKeywordsList = tribunCrawlFrontier.doc.xpath('//meta[@name="keywords"]')
    # date in DD-MMMM-YYYY HH:mm
    articleDate = tribunCrawlFrontier.doc.xpath('//div[@id="article"]/div[contains(@class,"bdr3")]/h3')
    dateFormat = "%d %B %Y %H:%M"

    articleAuthor = ""

    #parameter (xpath,xpath,xpath,string,string,string)
    return tribunCrawlFrontier.extractContent(articleAuthor, articleKeywordsList, articleDate, dateFormat, text)
