from bs4 import BeautifulSoup
from database import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def LaunchSelenium():
    options = Options()
	# Following two lines makes the chrome browser not show
	#options.add_argument('--headless')
	#options.add_argument('--disable-gpu')
    
    # Keeps browser open
    #options.add_experimental_option("detach", True)
    options.add_argument("user-data-dir=selenium")
    browser = webdriver.Chrome('./chromedriver', chrome_options=options)
    return browser

def AppendDomain(linkList, baseUrl):
    newList = []
    for url in linkList:
        if url[0] == '/':
            url = baseUrl + url
            newList.append(url)
    return newList

def EvaluatePage(webContent):
    linkList = []
    soup = BeautifulSoup(webContent, features="html.parser")
    for a in soup.find_all('a', href=True):
        url = a['href']
        linkList.append(url)
    return linkList

def CleanList(linkList):
    newList = []
    for url in linkList:
        # Checking for anchors #
        if "#" in url:
            url = url.split("#")[0]
        if url == "":
            url = 'NULL'

        # Checking for mailto
        if "mailto:" in url:
            url = "NULL"

        if url != "NULL":
            newList.append(url)
    return newList

def RemoveDuplicates(linkList):
    newList = []
    for url in linkList:
        if url not in newList:
            newList.append(url)
    return newList

def Main(url):
    done = False
    firstRun = True
    while done == False:
        if firstRun == True:
            firstRun = False
            # Launching selenium
            browser = LaunchSelenium()
        else:
            url = GetFirstUncrawled()
        browser.get(url)
        # Get raw list of URLs
        linkList = EvaluatePage(browser.page_source)
        # Remove duplicates from list
        linkList = RemoveDuplicates(linkList)
        # Remove anchors and Mailto URLs
        linkList = CleanList(linkList)
        # Append Domain
        linkList = AppendDomain(linkList, url)
        # Store in DB
        SaveURLs(linkList)
        # Set URL as crawled
        SetAsScraped()

# Deleting existing DB 
DeleteDatabaseData()
Main('https://www.legaldesk.dk')
