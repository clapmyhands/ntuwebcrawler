'''
Created on Sep 30, 2014

@author: Phuah Chee Chong

This file normalises the articles by calling perl scripts

1. Remove unwanted characters and combine all days of month into text file
2. Expand abbrevations
'''
import subprocess, xml.etree.ElementTree as ET#, num2words

def normalise(yr, mn, endMn, source):
#     sources = []
#
#     xmldocRequest = ET.parse(input)
#     rootRequest = xmldocRequest.getroot()
#
#     for s in rootRequest:
#         sources.append(s.get('source'))
#
#     for source in sources:
#
    for mn in range(int(mn), int(endMn)+1):
        pipe = subprocess.call(["perl", "normalisation/1_cleanUnwantedChars.pl", yr, str(mn).zfill(2), str(source)])
        pipe = subprocess.call(["perl", "normalisation/2_expand_abb.pl", yr, str(mn).zfill(2), str(source)])
        pipe = subprocess.call(["perl", "normalisation/3_split_snt.pl", yr, str(mn).zfill(2), str(source)])
        pipe = subprocess.call(["perl", "normalisation/4_remove_pnc.pl", yr, str(mn).zfill(2), str(source)])
        pipe = subprocess.call(["perl", "normalisation/5_append_sos.pl", yr, str(mn).zfill(2), str(source)])
