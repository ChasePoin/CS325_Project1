from module_2 import AllScrapers as S

def main():
        fileName = input("Enter the name of the file you want to use: ")
        APscraper = S.APscraper()
        APscraper.scrape(fileName)


if __name__ == "__main__":
    main()