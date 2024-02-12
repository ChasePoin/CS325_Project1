from bs4 import BeautifulSoup
import requests

### IMPORTANT: Make sure you are in the same working directory as your file containing the URLs you want to scrape.
## The newly created text files will be output to the same working directory as the one you are in.
def scrape(fileToOpen: str) -> None:
    "Pass the name of the file containing the URLs of the AP News articles you want to scrape."       
    file = open(fileToOpen, "r")
    articleNumber = 1
    # article number will be used for the outputted files' names
    for url in file:
        # loop in order to repeat process for each url present in the file

        html = requests.get(url, headers={"Connection": "keep-alive", "User-agent": "Mozilla/5.0"})
        soup = BeautifulSoup(html.content, "lxml")
        # requests sends a request for thecd data from the web server
        # BeautifulSoup parses and allows the particular data we want to be pulled easily

        fileName = "Article" + str(articleNumber) + ".txt"
        fileToOutput = open(fileName, "x")
        # creates file that the article text and title are going to be written to

        title = soup.find('h1', class_='Page-headline').text
        encodedTitle = title.encode('ascii', 'ignore')
        titleText = "Title: " + encodedTitle.decode() + "\n"
        # gets title from <h1> tags, makes it pretty, encoding it into ascii and decoding it back to a string in order to remove
        # unicode characters from appearing as "question marks"

        fileToOutput.write(titleText)
        # writes the beautiful title to the file

        body = soup.find_all('p')
        # gets actual article text from <p> tags, find_all() puts it into an array

        count = 0
        for partsOfArticle in body:
        # Loops through array of text found in <p> tags. "count" is present in order to not print out the copyright at the beginning 
            if count == 1:        
                encodeParts = partsOfArticle.text.encode('ascii', 'ignore')
                # this gets rid of the "question marks" by encoding the file in ascii characters
                fileToOutput.write(str(encodeParts.decode()) + "\n")
                # writes the article data to the file and decodes it in order to make it a string
            count = 1
        articleNumber = articleNumber + 1
        fileToOutput.close()
    file.close()
    # close the files
        



## example main of how to use the function
# def main():
#         scrape("news_urls.txt")


# if __name__ == "__main__":
#     main()