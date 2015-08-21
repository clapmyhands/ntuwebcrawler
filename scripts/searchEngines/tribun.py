'''
Created on Aug 21, 2015

@author: StefanSetyadiTjeng / clapmyhands
added getCategory from normal seed.py for handling topic
'''
from seed import buildSeed
from lxml import html


class tribun(buildSeed):

    def __init__(self):
        pass

    def crawlFrontierL2(self, currentQuery):
        baseURL = "http://www.tribunnews.com"
        # Where the seed links are located
        seedURL = "http://www.tribunnews.com/index-news/"
        xpath = "//li[@class='ptb15']//div//a"

        allReturnedURL = list()

        # currentQuery is suited to tribun archive query
        allReturnedURL = buildSeed.crawlFrontierL1(
            self, currentQuery, baseURL, xpath, seedURL + "?date=" + currentQuery)

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

    text = tribunCrawlFrontier.doc.xpath(
        '//div[@id="article_con"]//div[@class="side-article txt-article"]/p')
    articleKeywordsList = tribunCrawlFrontier.doc.xpath(
        '//meta[@name="keywords"]')
    # date in DD-MMMM-YYYY HH:mm
    articleDate = tribunCrawlFrontier.doc.xpath(
        '//meta[@name="og:url"]')
    dateFormat = " %d %B %Y %H:%M "

    articleAuthorList = ""

    #parameter (xpath,xpath,xpath,string,string,string)
    return tribunCrawlFrontier.extractContent(articleAuthor, articleKeywordsList, articleDate, dateFormat, text)
