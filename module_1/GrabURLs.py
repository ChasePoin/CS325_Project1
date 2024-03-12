from bs4 import BeautifulSoup
from abc import ABC, abstractmethod


### IMPORTANT: Make sure you are in the same working directory as your file containing the URLs you want to scrape.

# the idea behind this module was to follow the path of the getters and setters and the scrapers and make this follow the same principle: S
# I wanted to make this future proof and make it extremely easy and steamlined to add new ways to get URLs while also following the superclass's set methods.
# Since the only necessary way to grab URLs for this project is from a file, that is the only subclass of this superclass, but it demonstrates how each
# subclass would have a single responsibility.


# each URL Grabber would expect the source of the URLs (for "GetURLSTextFile," a text file) and then return the urls, hence giving them a single responsibility.


class URLGrabber(ABC):
    @abstractmethod
    def getURLs(self, source) -> str:
        pass

class GetURLSTextFile(URLGrabber):
    # using a file
    def getURLs(self, source) -> str:
        # information is the file to open
        try:   
            urls = open(source, "r")
            return urls
        except:
            print("Failure to open file containing URLs.")
            exit()
        # open URL file