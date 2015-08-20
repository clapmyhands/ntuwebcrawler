#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import datetime
import calendar
from xmlHandler.xmlControl import *
from normalisation.normalise import normalise
from dateutil.relativedelta import relativedelta

sys.path.append("searchEngines/")
#~ import LIBERATION

'''
The crawling is a 3 step process:
1. Load up the search result with dates specified in archiveList.xml
2. For each day, return the list of news articles' URL
3. For each URL return the content of the article and other meta information (i.e. [url, title, category, published date])
'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='From a list of query contained in a file, poduce xml documents conaining text articles')
    parser.add_argument('-i', '--input', dest='input',
                        help='Query file', required=True)
    parser.add_argument('-o', '--outputDir', dest='outputDir',
                        help='OutputDirectory', required=True)
    # parser.add_argument('-d', '--done'  , dest='listDone', help='Defines the list of query to process and already processed idStart="0" idEnd="0" idDone="0" included, if -1 project to maxima', required=True)
    parser.add_argument('-v', '--verbose', dest='verbose',
                        help='verbose mode', action='store_true')
    args = parser.parse_args()

    ########## ___loading or creating listDone___ ########

    # default values #

    ##############################

    #___loading rule file___#
    if not os.path.exists(args.input):
        print('no input file! exiting...')
        exit()

    elif os.path.exists(args.input):
        with open(args.input, 'r') as f:
            fContent = f.readlines()

    xmldocRequest = ET.parse(args.input)
    rootRequest = xmldocRequest.getroot()

    # Get when this crawler was initiated

    now = datetime.datetime.now()
    iniCrawlY = now.year
    iniCrawlM = now.month
    iniCrawlD = now.day

    for s in rootRequest:
        source = s.get('source')
        iniStartY = s.get('startY')
        iniStartM = s.get('startM')
        iniStartD = s.get('startD')
        endY = s.get('endY')
        endM = s.get('endM')
        endD = s.get('endD')

        '''
		if no end date is specified, the current date will be used
		'''

        if endD == "":
            endD = iniCrawlD

        if endM == "":
            endM = iniCrawlM

        if endY == "":
            endY = iniCrawlY

        startDates = datetime.date(
            int(iniStartY), int(iniStartM), int(iniStartD))
        endDates = datetime.date(int(endY), int(endM), int(endD))
        day = datetime.timedelta(days=1)
        normaliseUptoDate = startDates

        while (startDates <= endDates):

            modifiedFiles = list()

            if "Monthly" in source:
                startDates += datetime.timedelta(days=calendar.monthrange(
                    int(startDates.year), int(startDates.month))[1] - 1)

            strCurD = str(startDates.day)
            strCurD = strCurD.zfill(2)  # Pads zero to the left

            strCurM = str(startDates.month)
            strCurM = strCurM.zfill(2)

            strCurY = str(startDates.year)

            currentQuery = module.buildQuery(strCurY,strCurM,strCurD)

            urlList = list()

            # peut permettre de généraliser la gestion de modules en les
            # chargeant si nécessaire.
            module = __import__(source)

            #~ (urlList, urlQuery) = LIBERATION.produceAddressURL(currentQuery)
            #~ (urlList, urlQuery) = module.produceAddressURL(currentQuery)
            # Get the list of links from the archive search
            #urlList = module.produceAddressURL(currentQuery)

            urlList = module.buildCrawlFrontier(currentQuery)

            if not urlList:
                print("No Article found for date: " + currentQuery)
                startDates += day
                updateDoneList(args.input, source, startDates)
                continue

            print(source + ' ' + currentQuery + ": " +
                  str(len(urlList)) + ' documents found')

            # recuperation des conenus de articles dans une structure pour une
            # écriture en une seule fois
            contenu = list()

            #~ print 'extracting content'

            # For every article link belonging to the same publication date we
            # update the xml file
            for link in urlList:
                url = link[0]
                title = link[1]
                category = link[2]
                fullDate = link[3]

                ''' This function needs to be unpacked in the following order,
				1. Content of Article
				2. Author
				3. Article Date
				4. Article Keywords
				'''

                allContentInfo = module.cleanResultFile(url)

                if allContentInfo == "":
                    continue

                for contentInfo in allContentInfo:
                    article = contentInfo[0]
                    author = contentInfo[1]
                    # 2 = day, 1 = month, 0 = year
                    articleDate = contentInfo[2]
                    articleKeywords = contentInfo[3]

                if articleDate == "":
                    fName = "unknownDate.xml"
                    # Since no known published date, put it to the crawling
                    # date.
                    articleDate = "unknownDate"
                    dName = args.outputDir + "/" + source + "/" + strCurY + "/" + strCurM

                else:
                    dName = args.outputDir + "/" + source + "/" + \
                        str(articleDate[0]).zfill(2) + "/" + \
                        str(articleDate[1]).zfill(2)

                    # Now we need to assign the published date as normal
                    # datetime format
                    articleDate = str(articleDate[1]).zfill(2) + str(articleDate[0])

                    fName = articleDate + '.xml'

                # Create XML File if it does not already exists.
                createXMLFile(dName, fName, strCurD, strCurM,
                              strCurY, source, currentQuery)

                xmldoc = openXMLFile(dName, fName)

                articleNode = checkArticle(xmldoc, dName, fName, category, url)

                # Skip it since it has been crawled!
                if articleNode is not None:
                    print("Article found in corpus! Skipping...")
                    continue

                root = checkCategoryTag(xmldoc, dName, fName, category)

                if str(url.encode('utf-8')).find("\\xc2\\xb0") != -1:
                    continue

                try:
                    print(title)

                except:
                    pass

                for cat in root.findall('category'):
                    if category == cat.get('name'):
                        catNode = cat  # Get the specific node the article belongs to
                        break

                createArticleTag(xmldoc, dName, fName, catNode, article,
                                 url, title, author, articleDate, articleKeywords)

                if fName not in modifiedFiles:
                    modifiedFiles.append(dName + "/" + fName)

            # Reopens the file to format it before writing it back to the same
            # file again.
            print('Formatting files that has been modified...')

            formatXML(modifiedFiles)

            startDates += day

            updateDoneList(args.input, source, startDates)

            # Normalising after every month and after the end date is reached
# 			if normaliseUptoDate.month != startDates.month or startDates > endDates:
# 				# When the month is done
# 				print('Normalising...')
# 				normalise(normaliseUptoDate.year, normaliseUptoDate.month, source)
# 				normaliseUptoDate + relativedelta(months=1)
