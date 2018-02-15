from bs4 import BeautifulSoup
import urllib
# gets the data from the license links. commenting the 
# prints was done to prevent unicode errors.
import pandas as pd

with open("listOfNonDuplicateOrganizationLinks.txt", "r", encoding="utf-8") as links:
    i = 0
    d = { 'id':[],'License Number':[],'Status':[],'Renewal Date': [], 'Name':[],'Address':[],'County':[], 'Telephone':[],'Limitation':[],'Classifications':[], 'Qualifiers':[] }
    name, license, status, renewal, classifications, qualifiers, county, limitation, telephone, address = "","","","","","","","","",""
    for link in links:
        print(i)
        i += 1
        r = urllib.request.urlopen(link).read()
        soup = BeautifulSoup(r, "lxml")
        
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
        d['Renewal Date'].append(renewal)
        d['Classifications'].append(classifications)
        d['Qualifiers'].append(qualifiers)

        name, license, status, renewal, classifications, qualifiers, county, limitation, telephone, address = "","","","","","","","","",""

        for row in soup.find_all("tr"):
            text = row.text.replace(",","")
            text = text.replace("\t","")
            text = text.replace(";","")
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
            if "Name" in text:
                mode = "Name"
            if "Renewal Date" in text:
                mode = "Renewal Date"
            if "Classifications" in text:
                mode = "Classifications"
            if "Qualifiers" in text:
                mode = "Qualifiers"

            text = text.replace("License Number", "")
            text = text.replace("Status", "")
            text = text.replace("County","")
            text = text.replace("Limitation","")
            text = text.replace("Telephone","")
            text = text.replace("Address","")
            text = text.replace("Name","")
            text = text.replace("Renewal Date","")
            text = text.replace("Classifications","")
            text = text.replace("Qualifiers","")
            text = text.replace(",","")
            text = text.replace("\n"," ")

            if text == "":
                continue

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
            if mode == "Name":
                name = name + " " + text
            if mode == "Renewal Date":
                renewal = renewal + " " + text
            if mode == "Classifications":
                classifications = classifications + " " + text
            if mode == "Qualifiers":
                qualifiers = qualifiers + " " + text



df = pd.DataFrame(data=d)

df.to_csv("contractor_companies_licenses.csv")
            
