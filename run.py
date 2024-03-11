from module_2 import AllScrapers as S
import argparse as ap

def argparser():
    parser=ap.ArgumentParser()
    parser.add_argument(help='Your file containing URLs', dest='file', type=str)
    arguments = parser.parse_args()
    file = arguments.file
    return file

def main():
    fileName = argparser()
    APscraper = S.APscraper()
    APscraper.scrape(fileName)


if __name__ == "__main__":
    main()