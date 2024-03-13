from module_2 import ScrapersGettersSetters as SGS
from module_1 import GrabURLs
import argparse as ap
from os.path import exists

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
    titleWriter = SGS.WriteTitle()
    articleWriter = SGS.WriteArticle()
    urls = fileURLGetter.getURLs(fileName)
    articleNumber = 1
    # this version now passes each URL individually instead of the whole file, so articleNumber is now passed in for error reporting
    for url in urls:
        APscraper.scrape(url, articleNumber)
        # RAW is original file format, with article title + article body
        # PROCESSED is new file format, with only the article body        
        rawFileName = APscraper.titleText + "_RAW.txt"
        rawFileName = rawFileName.replace(" ", "_")
        fileName = APscraper.titleText + ".txt"
        procFileName = fileName.replace(" ", "_")

        # RAW:
        if (not exists("./Data/raw/" + rawFileName)):
            # handles writing raw data
            # RAW == ORIGINAL FORM OF WRITING
            rawFileToOutput = open("./Data/raw/" + rawFileName, "x")
            try:
                titleWriter.writeInfo(APscraper.titleText, rawFileToOutput, articleNumber)
                # writes the title to the file
            except:
                print(f"Failed to write title for article {articleNumber}.")
            

            try:
                articleWriter.writeInfo(APscraper.body, rawFileToOutput, articleNumber)
            except:
                print(f"Failed to write Article data for RAW, article {articleNumber}")
            print(f"RAW Article {articleNumber} file created successfully.")
        else:
            print(f"RAW Article {articleNumber} file already exists.")

        # PROCESSED:
        if (not exists("./Data/processed/" + procFileName)):
            # handles writing processed data
            # PROCESSED == NEW FORM OF WRITING
            fileToOutput = open("./Data/processed/" + procFileName, "x")

            try:
                articleWriter.writeInfo(APscraper.body, fileToOutput, articleNumber)
                # passes the newly created array in as well as the file to write to, and writes the article to the file
            except:
                print(f"Failed to write the article data to the file for article {articleNumber}")

            # the try except blocks do not fail the program but instead just fail on a per article basis
            print(f"PROCESSED Article {articleNumber} file created successfully.")
            fileToOutput.close()
        else:
            print(f"PROCESSED Article {articleNumber} file already exists.")

        articleNumber = articleNumber + 1


if __name__ == "__main__":
    main()