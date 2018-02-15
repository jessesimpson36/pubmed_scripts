from bs4 import BeautifulSoup
import urllib
# gets the data from the license links. commenting the 
# prints was done to prevent unicode errors.
import pandas as pd

with open("listOfNonDuplicateLicenseLinks.txt", "r", encoding="utf-8") as links:
    i = 0
    d = { 'id':[],'Name':[],'License Number':[],'Status':[],'County':[], 'Limitation':[],
                'Telephone':[], 'Address':[] }
    name, license, status, county, limitation, telephone, address = "","","","","","",""
    for link in links:
        print(i)
        i += 1
        r = urllib.request.urlopen(link).read()
        soup = BeautifulSoup(r, "lxml")
        # data.write("--------------------------\n")
        # print("----------------------------")
        # data.write(soup.p.text + "\n")
        # data.write(soup.p.text.replace(",","") + ",")
        text = ""
        mode = ""

        d['id'].append(i)
        d['Name'].append(name)
        d['License Number'].append(license)
        d['Status'].append(status)
        d['County'].append(county)
        d['Limitation'].append(limitation)
        d['Telephone'].append(telephone)
        d['Address'].append(address)
        name, license, status, county, limitation, telephone, address = "","","","","","",""



        name = soup.p.text.replace(",","")

        for row in soup.find_all("tr"):
            text = row.text
            if "License Number" in text:
                mode = "License Number"
            if "Status" in text:
                mode = "Status"
            if "County" in text:
                mode = "County"
            if "Limitation" in text:
                mode = "Limitation"
            if "Telephone" in text:
                mode = "Telephone"
            if "Address" in text:
                mode = "Address"

            text = row.text.replace("License Number", "")
            text = text.replace("Status", "")
            text = text.replace("County","")
            text = text.replace("Limitation","")
            text = text.replace("Telephone","")
            text = text.replace("Address","")
            text = text.replace(",","")
            text = text.replace("\n"," ")

            if mode == "Address":
                address = address + " " + text
            if mode == "Telephone":
                telephone = telephone + " " + text
            if mode == "Limitation":
                limitation = limitation + " " + text
            if mode == "County":
                county = county + " " + text
            if mode == "Status":
                status = status + " " + text
            if mode == "License Number":
                license = license + " " + text



df = pd.DataFrame(data=d)

df.to_csv("contractor_licenses.csv")
            
