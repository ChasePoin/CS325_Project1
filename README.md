# README! AP News Web Scraper
This is a web scraper that was made for a project in class. It is programmed in Python and uses BeautifulSoup and Requests packages in order to get web data and organize it into text files. The python environment is attached in a file called "requirements.yml."

-The project1.py file contains a single function that acts as the web scraper. You will need to pass in a TEXT file containing a list of AP News URLs (how ever many you want, could be 1 URL, could be 50).

-It is VERY important that you are in the same working directory (your cmd is in the folder containing your text file) when you run the program. The path is NOT specified so it will search the current directory for the name of the file you passed into the function.

-The function will create text files named "ArticleX.txt," with X being based on the order of the URLs in the text file you passed in; for example, the first article in the list will be named "Article1.txt," while the fifth article will be named "Article5.txt." These created article files will ALSO be output into the current working directory (folder your cmd is working in).

-The "news_urls.txt" file is an example file of how the URLs should be organized for the program to use them correctly. The file is in the repository to provide an example to use. You do not have to actually use the provided text file.
