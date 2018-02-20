from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib
import re
from nltk import word_tokenize
import csv

RARE_DX_CO_FILE = "data/rare_dx_co_list.csv"

def get_website_url():
    with open(RARE_DX_CO_FILE, "r") as rdx_co_file:
        datareader = csv.reader(rdx_co_file)
        for row in datareader:
            url = "http://" + row[0] + ""
            yield url

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser', from_encoding='utf-8')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return " ".join(t.strip() for t in visible_texts)

def get_rdx_co_name():
    for url in get_website_url():
    # url = 'http://www.janssen.com/us/our-products'
    # outf = 'janssen.com.txt'
        print '============================='
        try:
            conn = urllib.urlopen(url)
            html = conn.read()
            conn.close()
            output = text_from_html(html)
            encoded = output.encode('ascii', 'ignore')
            tokens = word_tokenize(encoded)
            print(" ".join(tokens))
            #with open(outf, 'wb') as f:
            #    f.write(output.encode('ascii', 'ignore'))

            last = len(tokens) - 1
            for i in range(last, -1, -1):
                if tokens[i] == "Inc.":
                    if i != 0 and tokens[i-1] == ",":
                        print(tokens[i-2])
        except IOError:
            print ("BROKEN", url)

get_rdx_co_name()


