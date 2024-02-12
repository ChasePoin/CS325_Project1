# AP News Web Scraper
## Details:
This is a web scraper that was made for a project in class. It is programmed in Python 3.9.18 and uses BeautifulSoup and Requests packages in order to get web data and organize it into text files. The python environment (containing these packages) is attached in a file called "requirements.yml."

-The project1.py file contains a single function that acts as the web scraper. The function takes a TEXT file name containing a list of AP News URLs (how ever many you want, could be 1 URL, could be 50). ex// scrape("news_urls.txt"); this will open news_urls.txt and use the URLs present in the file.

-The "news_urls.txt" file is an example file of how the URLs should be organized for the program to use them correctly. The file is in the repository to provide an example to use. You do not have to actually use the provided text file.

-It is VERY important that you are in the same working directory (your cmd is in the folder containing your text file) when you run the program. The path is NOT specified so it will search the current directory for the name of the file you passed into the function.

-The function will create text files named "ArticleX.txt," with X being based on the order of the URLs in the text file you passed in; for example, the first article in the list will be named "Article1.txt," while the fifth article will be named "Article5.txt." These created article files will ALSO be output into the current working directory (folder your cmd is working in).

-Five examples of how the files are output are also present in the repo; these use the URLs present in the "news_urls.txt" file, so you are able to compare the files to where the files' text comes from.

### Step by Step Walkthrough:
This assumes you have an python environment management system such as conda (recommended, as this is what was used to test) and visual studio code installed. There are plenty of guides on the internet on how to install these.

1. Download the zip from this repo by pressing the green code button and then "Download zip." Unpack this zip to your folder of choice.

2. Open your cmd and navigate the working directory to the folder you unpacked the zip to. (Example: cd .. takes you back a directory and cd "folder" will take you to the folder directory. Just look at your file explorer and move your cmd directory in accordance with each folder you see.)

3. This is where you will create your python environment; you will create this new environment based off the requirements.yml file. To do this in conda, type "conda env create -f requirements.yml." By default the name of this environment will be project1. If you want the environment to be a different name edit the "name" (first line) of the requirements.yml file. If you are using a different environment manager find the command to make a new environment based off a yml/yaml file.

4. Open the folder you extracted your zip file to in visual studio code.

5. Now press ctrl + shift + p to open the command palette and type in "python: select interpreter." Select the option with the corresponding name; a list will appear. Choose the option with the name of the environment you just created.

6. Take the URLs you want to scrape and either make a new text file and order the URLs as you want (look at news_urls.txt for formatting) or just replace the URLs in news_urls.txt with the ones you want to scrape.

7. Make sure your terminal in VSC is in the folder with your text file.

8. Uncomment the main by highlighting it and pressing ctrl + /.

9. If you made a new file, replace "news_urls.txt" with "your_file_name".

10. Run the program. Your newly output files should appear in the same folder.
