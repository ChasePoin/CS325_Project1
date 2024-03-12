from module_2 import AllScrapers as S
from module_1 import GettersAndWriters as GW
import argparse as ap

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
    APscraper = S.APscraper()
    fileURLGetter = GW.GetURLs()
    urls = fileURLGetter.getInfo(fileName)
    articleNumber = 1
    # this version now passes each URL individually instead of the whole file, so articleNumber is now passed in for error reporting
    for url in urls:
        APscraper.scrape(url, articleNumber)
        articleNumber = articleNumber + 1


if __name__ == "__main__":
    main()