######
#
#   Script to scrape Google Search results
#
#   Created by https://twitter.com/shanejones 
#   Go and give him a follow being so he gave you this script for free
#
######
import re
import time
import requests
from bs4 import BeautifulSoup

sleep = 0.025

search = 'google.com'

outputFile = open("output.csv", "a")
outputFile.write("\n" + 'Keyword, Results, Quoted, All In Title')

with open('keywords.txt') as f:
    for line in f:

        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/66.0"}

        # search a
        standardSearch = requests.get(
            'https://www.' + search + '/search?q=' + line.replace(" ", "+"),
            headers=headers
        )
        time.sleep(sleep)
        quotedSearch = requests.get(
            'https://www.' + search + '/search?q="' + line.replace(" ", "+") + '"', headers=headers
        )
        time.sleep(sleep)
        allInSearch = requests.get(
            'https://www.' + search + '/search?q=allintitle%3A"' +
            line.replace(" ", "+") + '"',
            headers=headers
        )
        time.sleep(sleep)

        standardSearchSoup = BeautifulSoup(
            standardSearch.content, 'html.parser')
        quotedSearchSoup = BeautifulSoup(
            quotedSearch.content, 'html.parser')
        allInSearchSoup = BeautifulSoup(allInSearch.content, 'html.parser')

        standardSearchResultsContainer = standardSearchSoup.find(
            id='result-stats')
        quotedSearchResultsContainer = quotedSearchSoup.find(
            id='result-stats')
        allInSearchResultsContainer = allInSearchSoup.find(
            id='result-stats')

        if(standardSearchResultsContainer):
            standardSearchResultsText = standardSearchResultsContainer.get_text(
                strip=True)
            standardSearchResults = re.findall(
                '([0-9,]+)', standardSearchResultsText)
        else:
            standardSearchResults = '0'

        if(quotedSearchResultsContainer):
            quotedSearchResultsText = quotedSearchResultsContainer.get_text(
                strip=True)
            quotedSearchResults = re.findall(
                '([0-9,]+)', quotedSearchResultsText)
        else:
            quotedSearchResults = '0'

        if(allInSearchResultsContainer):
            allInSearchResultsText = allInSearchResultsContainer.get_text(
                strip=True)
            allInSearchResults = re.findall(
                '([0-9,]+)', allInSearchResultsText)
        else:
            allInSearchResults = '0'

        print(line.rstrip() + " - complete")

        outputFile.write("\n" + line.rstrip() + ", " +
                        standardSearchResults[0].replace(",", "") + ", " +
                        quotedSearchResults[0].replace(",", "") + ", " +
                        allInSearchResults[0].replace(",", "")
                        )

outputFile.close()
