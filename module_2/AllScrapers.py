from module_1 import GettersAndWriters as GetWrite
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

# Using both of these SOLID principles allows for very simple and streamlined implementation of new functionality. 
# using Liskov allows for multiple scrapers to exist with a superclass dictating that they all function similarly, and using single responsibility allows
# for these scraper functions to focus on handling errors and calling each getter and writer, allowing for easy implementation of new getters and writers allowing for
# more information to be scraped without needing to remove any pre-existing functionality if it is ever wanted or needed. 

# each scraper's scrape() should only take the file containing the raw URLs to scrape. scrape() returns nothing, but is responsible for making sure each file is output properly

class Scrapers(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def scrape(self, fileToOpen: str) -> None:
        pass

class APscraper(Scrapers):
    def __init__(self):
        self.titleGetter = GetWrite.GetTitle()
        self.titleWriter = GetWrite.WriteTitle()
        self.articleGetter = GetWrite.GetArticle()
        self.articleWriter = GetWrite.WriteArticle()  
   
    def scrape(self, fileToOpen: str) -> None:
        "Pass the name of the file containing the URLs of the AP News articles you want to scrape."    

        try:   
            file = open(fileToOpen, "r")
        except:
            print("Failure to open file containing URLs.")
            exit()
        # open URL file

        articleNumber = 1
        # article number will be used for error reporting
        for url in file:
            # loop in order to repeat process for each url present in the file
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
                print(f"Article {articleNumber} file already exists.")
                articleNumber = articleNumber + 1
        file.close()
        # close the files