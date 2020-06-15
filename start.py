import requests
from bs4 import BeautifulSoup
from database import *

def RemoveAnchors(url):
    if "#" in url:
        url = url.split("#")[0];
    if url == "":
        url = 'NULL'
    return url

def RemoveMailTo(url):
    if "mailto:" in url:
        url = "NULL"
    return url

def FromDomain(url, baseUrl):
    #baseUrl = baseUrl.replace("https://","")
    #baseUrl = baseUrl.replace("http://","")
    if url[0] == '/':
        url = baseUrl + url 
    else:
        url = 'NULL'
    return url

def EvaluatePage(webContent):
    i = 0
    soup = BeautifulSoup(webContent, features="html.parser")
    for a in soup.find_all('a', href=True):
        url = a['href']
        url = RemoveAnchors(url)
        url = RemoveMailTo(url)
        url = FromDomain(url, baseUrl)
        if url != "NULL":
            inserted = InserScraped(url, "NULL")
            if inserted == True:
                i=i+1
    return i

def DatabaseLoop():
    url = GetFirstUncrawled()
    print('Scraping:' + str(url))
    response = requests.get(url)
    UpdateScraped(url, response.content)
    numberOfNew = EvaluatePage(response.content)
    print('Added ' + str(numberOfNew) + ' new links.')
    DatabaseLoop()

baseUrl = 'https://www.legaldesk.dk'
databaseurl = baseUrl + "/"

response = requests.get(baseUrl)

InserScraped(databaseurl, response.content)

numberOfNew = EvaluatePage(response.content)
print('Added ' + str(numberOfNew) + ' new links.')
DatabaseLoop()

