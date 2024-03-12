from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests
from os.path import exists

# The idea behind this module was to take the pre-existing scrape function and make it a subclass of a superclass named Scrapers(), making Scrapers() a template
# for future scrapers to be made, and for the APscraper to simply be one of many subclass scrapers if the functionality were ever to be needed.
# each scraper would have an __init__ function so when an object is created it creates objects of each getter and writer from the imported module. There is no limit
# on the amount of getters and writers, you just simply have to implement the functionality of what you want to get and what you want to write

# This module fulfills the Liskov Substitution principle; the superclass has two defined functions: an init to declare necessary getter and writer objects, and a
# scrape() to scrape the document using the getters and the writers. The subclass demonstrates the exact same behavior as the superclass.
# This module also fulfills the single responsibility principle; each scraper has one functionality: to scrape, using the getters and writers created for that scraper;
# the class should only have one reason to change: to add/remove functionality of the scraper.

# The InfoGetters and InfoWriters also follow these exact principles, allowing for easy implementation of different data grabbers.
# This allows for easy restructing of scrapers to change in accordance to which data you want to grab from the article. It also allows for different scrapers to have
# different getters/setters without affecting old ones.

# Using both of these SOLID principles allows for very simple and streamlined implementation of new functionality. 
# using Liskov allows for multiple scrapers to exist with a superclass dictating that they all function similarly, and using single responsibility allows
# for these scraper functions to focus on handling errors and calling each getter and writer, allowing for easy implementation of new getters and writers allowing for
# more information to be scraped without needing to remove any pre-existing functionality if it is ever wanted or needed. 
# These principles allow for great amounts of freedom when designing the output of a scraper.

# each scraper's scrape() should only take a raw URL to scrape. scrape() returns nothing, but is responsible for making sure each file is output properly
# each info getter expects the soup (the beautifulsoup parsed html)

class Scrapers(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def scrape(self, url: str, articleNum: int) -> None:
        pass

class InfoGetters(ABC):
    @abstractmethod
    def getInfo(self, soup) -> str:
        pass

class InfoWriters(ABC):
    @abstractmethod
    def writeInfo(self, information, fileToOutput, currentArticle) -> None:
        pass

class APscraper(Scrapers):
    def __init__(self):
        self.titleGetter = GetTitle()
        self.titleWriter = WriteTitle()
        self.articleGetter = GetArticle()
        self.articleWriter = WriteArticle()  
   
    def scrape(self, url: str, articleNumber: int) -> None:
        "Pass the url wanted to be scraped."    
        # article number will be used for error reporting
        try:
            html = requests.get(url, headers={"Connection": "keep-alive", "User-agent": "Mozilla/5.0"})
        except:
            print("Failure to request web data for article " + str(articleNumber) + ".")
        
        soup = BeautifulSoup(html.content, "lxml")
        # requests sends a request for the data from the web server
        # BeautifulSoup parses and allows the particular data we want to be pulled easily

        try:
            titleText = self.titleGetter.getInfo(soup)
            # calls getTitle() to, well, get the title
        except:
            print(f"Failed to get title for article {articleNumber}.")

        # RAW is original file format, with article title + article body
        # PROCESSED is new file format, with only the article body
        rawFileName = titleText + "_RAW.txt"
        rawFileName = rawFileName.replace(" ", "_")
        fileName = titleText + ".txt"
        fileName = fileName.replace(" ", "_")
        # RAW:
        if (not exists("./Data/raw/" + rawFileName)):
            # handles writing raw data
            # RAW == ORIGINAL FORM OF WRITING
            rawFileToOutput = open("./Data/raw/" + rawFileName, "x")
            try:
                self.titleWriter.writeInfo(titleText, rawFileToOutput, articleNumber)
                # writes the title to the file
            except:
                print(f"Failed to write title for article {articleNumber}.")
            
            try:
                body = self.articleGetter.getInfo(soup)
            except:
                print(f"Failed to get Article for RAW, article {articleNumber}")

            try:
                self.articleWriter.writeInfo(body, rawFileToOutput, articleNumber)
            except:
                print(f"Failed to write Article data for RAW, article {articleNumber}")
        else:
            print(f"RAW Article {articleNumber} file already exists.")

        # PROCESSED:
        if (not exists("./Data/processed/" + fileName)):
            # handles writing processed data
            # PROCESSED == NEW FORM OF WRITING
            fileToOutput = open("./Data/processed/" + fileName, "x")

            try:
                body = self.articleGetter.getInfo(soup)
                # gets actual article text from <p> tags
            except:
                print(f"Failed to get article data for article {articleNumber}.")

            try:
                self.articleWriter.writeInfo(body, fileToOutput, articleNumber)
                # passes the newly created array in as well as the file to write to, and writes the article to the file
            except:
                print(f"Failed to write the article data to the file for article {articleNumber}")

            # the try except blocks do not fail the program but instead just fail on a per article basis
            print(f"Article {articleNumber} file created successfully.")
            articleNumber = articleNumber + 1
            # increment for next file name
            fileToOutput.close()
        else:
            print(f"PROCESSED Article {articleNumber} file already exists.")

# unused class to write raw html, but it shows how easily new functionality can be added
# class WriteRawData(InfoWriters):
#     def writeInfo(self, information, fileToOutput, currentArticle) -> None:
#         prettySoup = information.prettify()
#         prettySoup = prettySoup.encode('ascii', 'ignore')
#         prettySoup = prettySoup.decode()
#         try:
#             fileToOutput.write(prettySoup)
#         except: 
#             print(f"Failed to write RAW html for article {currentArticle}")        

class GetTitle(InfoGetters):
    def getInfo(self, soup) -> str:
        # gets title from <h1> tags, makes it pretty, encoding it into ascii and decoding it back to a string in order to remove
        # unicode characters from appearing as "question marks," returns the title  
        title = soup.find('h1', class_='Page-headline').text
        encodedTitle = title.encode('ascii', 'ignore')
        titleText = encodedTitle.decode()
        return titleText

class WriteTitle(InfoWriters):
    def writeInfo(self, information, fileToOutput, currentArticle) -> None:
        formattedTitle = "Title: " + information + "\n"
        # formats the title to write it using unformatted title text (information)
        try:
            fileToOutput.write(formattedTitle)
            # writes the beautiful title to the file
        except:
            print(f"Failed to write title for article {currentArticle}.")
    
class GetArticle(InfoGetters):
    def getInfo(self, soup) -> str:
        # gets actual article text from <p> tags, find_all() puts it into an array
        body = soup.find_all('p')
        return body

class WriteArticle(InfoWriters):
    def writeInfo(self, information, fileToOutput, currentArticle) -> None:
        # loops through newly created array, makes it pretty, encoding it into ascii and decoding it back to a string in order to remove unicode
        # does not return anything and instead writes each part of the array to the file
        count = 0
        for partsOfArticle in information:
        # "count" is present in order to not print out the copyright at the beginning 
            if count == 1:        
                encodeParts = partsOfArticle.text.encode('ascii', 'ignore')
                # this gets rid of the "question marks" by encoding the file in ascii characters
                fileToOutput.write((encodeParts.decode()) + "\n")
                # writes the article data to the file and decodes it in order to make it a string
            count = 1