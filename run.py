from module_2 import ScrapersGettersSetters as SGS
from module_1 import GrabURLs
import argparse as ap


### IMPORTANT: Make sure you are in the same current working directory as the folder containing the URLs and all of the downloaded files/folders.
## module 1 imports the way to get the URLs from the file. module 2 imports the scraper


def argparser():
    parser=ap.ArgumentParser()
    parser.add_argument(help='Your file containing URLs', dest='file', type=str)
    arguments = parser.parse_args()
    file = arguments.file
    return file

def main():
    # URL getter gets all of the URLs from the file, passes in each individually to the scraper
    fileName = argparser()
    # make objects of scraper and URL getter
    APscraper = SGS.APscraper()
    fileURLGetter = GrabURLs.GetURLSTextFile()
    urls = fileURLGetter.getURLs(fileName)
    articleNumber = 1
    # this version now passes each URL individually instead of the whole file, so articleNumber is now passed in for error reporting
    for url in urls:
        APscraper.scrape(url, articleNumber)
        articleNumber = articleNumber + 1


if __name__ == "__main__":
    main()