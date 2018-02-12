from bs4 import BeautifulSoup
import urllib
# gets the data from the license links. commenting the 
# prints was done to prevent unicode errors.


with open("listOfNonDuplicateLicenseLinks.txt", "r", encoding="utf-8") as links:
    with open("data.txt", "w", encoding="utf-8") as data:
        i = 0
        for link in links:
            print(i)
            i += 1
            r = urllib.request.urlopen(link).read()
            soup = BeautifulSoup(r, "lxml")
            data.write("--------------------------")
            # print("----------------------------")
            data.write(soup.p.text)
            # print(soup.p.text)
            for row in soup.find_all("tr"):
                data.write(row.text.replace("\n", " ")) 
                # print(row.text.replace("\n"," "))

