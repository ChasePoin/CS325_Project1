from bs4 import BeautifulSoup
import requests

### IMPORTANT: Make sure you are in the same working directory as your file containing the URLs you want to scrape.
## The newly created text files will be output to the same working directory as the one you are in.
def scrape(fileToOpen: str) -> None:
    "Pass the name of the file containing the URLs of the AP News articles you want to scrape."    
    try:   
        file = open(fileToOpen, "r")
    except:
        print("Failure to open file containing URLs.")
        exit()
    # open URL file

    articleNumber = 1
    # article number will be used for the output files' names
    for url in file:
        # loop in order to repeat process for each url present in the file
        try:
            html = requests.get(url, headers={"Connection": "keep-alive", "User-agent": "Mozilla/5.0"})
        except:
            print("Failure to request web data for article " + str(articleNumber) + ".")
        
        soup = BeautifulSoup(html.content, "lxml")
        # requests sends a request for the data from the web server
        # BeautifulSoup parses and allows the particular data we want to be pulled easily

        fileName = "Article" + str(articleNumber) + ".txt"
        fileToOutput = open(fileName, "x")
        # creates file that the article text and title are going to be written to
        try:
            titleText = getTitle(soup)
            # calls getTitle() to, well, get the title
        except:
            print(f"Failed to get title for article {articleNumber}.")

        try:
            fileToOutput.write(titleText)
            # writes the beautiful title to the file
        except:
            print(f"Failed to write title for article {articleNumber}.")

        try:
            body = soup.find_all('p')
            # gets actual article text from <p> tags, find_all() puts it into an array
        except:
            print(f"Failed to get article data for article {articleNumber}.")

        try:
            writeArticle(body, fileToOutput)
            # passes the newly created array in as well as the file to write to, and writes the article to the file
        except:
            print(f"Failed to write the article data to the file for article {articleNumber}")

        # the try except blocks do not fail the program but instead just fail on a per article basis

        articleNumber = articleNumber + 1
        # increment for next file name
        fileToOutput.close()
    file.close()
    # close the files

# gets title from <h1> tags, makes it pretty, encoding it into ascii and decoding it back to a string in order to remove
# unicode characters from appearing as "question marks," returns the title  
def getTitle(soup) -> str:
    title = soup.find('h1', class_='Page-headline').text
    encodedTitle = title.encode('ascii', 'ignore')
    titleText = "Title: " + encodedTitle.decode() + "\n"
    return titleText

# loops through newly created array, makes it pretty, encoding it into ascii and decoding it back to a string in order to remove unicode
# does not return anything and instead writes each part of the array to the file
def writeArticle(body, fileToOutput) -> None:
    count = 0
    for partsOfArticle in body:
    # "count" is present in order to not print out the copyright at the beginning 
        if count == 1:        
            encodeParts = partsOfArticle.text.encode('ascii', 'ignore')
            # this gets rid of the "question marks" by encoding the file in ascii characters
            fileToOutput.write((encodeParts.decode()) + "\n")
            # writes the article data to the file and decodes it in order to make it a string
        count = 1
