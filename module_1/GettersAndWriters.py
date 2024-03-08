from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests
from os.path import exists

### IMPORTANT: Make sure you are in the same working directory as your file containing the URLs you want to scrape.

# the idea behind this module was to separate each information getter and writer into two distinct superclasses so that new functionality could be easily added.
# for now there is only title and article, but with this current skeleton you could easily add new functionality to a scraper, such as getting the author's name.
# it also allows for different getters and different writers per each scraper (as the other module allows for multiple scrapers)
# this module fulfills the Single Responsibility principle, as each class has a single well-defined function, and only has one reason to ever be changed.
# it also fulfills the Liskov Substitution principle, as each subclass exhibits the same behavior as the superclass; each subclass will only have a getInfo/writeInfo method.

# Using both of these principles allows for streamlined implementation of new getters and writers for a specific scraper's needs by just adding new classes based on the superclasses.

# each getter expects the soup (HTML put into BeautifulSoup() parser), which will output the formatted respective text to be written to the file
# each writer expects the sepcific information to be written to the file, the OPENED file's name for writing, and the currentArticle for error reporting
# the writers return nothing but are responsible for writing information to files

class InfoGetters(ABC):
    @abstractmethod
    def getInfo(self, soup) -> str:
        pass

class InfoWriters(ABC):
    @abstractmethod
    def writeInfo(self, information, fileToOutput, currentArticle) -> None:
        pass

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

