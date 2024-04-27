from xml.etree import ElementTree as ET

def summaryToHTML(inputFile, html_file):
    # open the file containing the articles and the titles
    file = open(inputFile, 'r')
    # create the basic structure of the html file: <html><head><title>
    root = ET.Element("html")
    head = ET.SubElement(root, "head")
    title = ET.SubElement(head, "title")
    title.text = "Summarized AP News"
    # begin <body>
    body = ET.SubElement(root, "body")
    # loops through each line present in the file containing the articles (file is basically an array containing lines, so you can iterate through)
    for line in file:
        # gemini returns each title formatted as **title**, can be used to to differentiate the title lines from body
        if line[0] == '*':
            header = line
            h1 = ET.SubElement(body, "h1")
            # <h1> for each header
            h1.text = header
            # since the body for an article will follow the title, make the rest of the text until the next title in the <p> tag for that article
            p = ET.SubElement(body, "p")
            part_of_body = ""
        else:
            # keep adding to the body (in <p>) until a title
            part_of_body = part_of_body + line
            p.text = part_of_body
        with open(html_file, 'wb') as f:
            tree = ET.ElementTree(root)
            tree.write(f, encoding='utf-8')


def main():
    summaryToHTML("input.txt", "all_articles.html")

if __name__ == "__main__":
    main()
