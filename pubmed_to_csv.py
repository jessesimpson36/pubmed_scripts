import csv
import sys
import pandas as pd

f = open("rare_dx.csv", "r", encoding="utf-8")
reader = csv.reader(f)

rare_dx_list = []

for row in reader:
    rare_dx_list.append(row)
f.close()

print(rare_dx_list)

rare_dx_info = open("pubmed_filter_1.txt", "r", encoding="utf-8")

d= {'id':[], 'title':[], 'abstract':[], 'authors':[], 'location':[], 'rare_dx':[]}
id, title, abstract, authors, location, rare_dx = "", "", "", "", "", ""


mode="PMID"
for line in rare_dx_info:
    if line.startswith("PMID"):

        for dx in rare_dx_list:
            if dx[0] in title or dx[0] in abstract:
                rare_dx = dx[0]
            else:
                rare_dx = "N/A"

        d['id'].append(id)
        d['title'].append(title)
        d['abstract'].append(abstract)
        d['authors'].append(authors)
        d['location'].append(location)
        d['rare_dx'].append(rare_dx)

        id = line
        title = ""
        abstract = ""
        authors = ""
        location = ""
        mode="PMID"
    if line.startswith("TI"):
        title += line
        mode="TI"
    if line.startswith("AB"):
        abstract+= line
        mode="AB"
    if line.startswith("FAU"):
        authors+=line
        mode="FAU"
    if line.startswith("AD"):
        location+=line
        mode="AD"
    if line.startswith("PL"):
        continue
    if line.startswith("      "):
        if mode == "PMID":
            id += line
        if mode == "TI":
            title += line
        if mode == "AB":
            abstract += line
        if mode == "FAU":
            authors += line
        if mode == "AD":
            location += line
        if mode == "PL":
            continue

rare_dx_info.close()
df = pd.DataFrame(data=d)

df.to_csv("pubmed_research_papers.csv")