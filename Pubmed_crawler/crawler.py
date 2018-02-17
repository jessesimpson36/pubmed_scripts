# pip install biopython
import json
from Bio import Entrez
import pandas as pd

# Queries the information in pubmed.
def search(query):
    Entrez.email = 'email@email.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='1',
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results

# gets the details of the query.
def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'email@email.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results

if __name__ == '__main__':

    d = { 'id':[],'keywords':[], 'date_completed':[], 'date_revised':[], 'article_date':[], 'article_title':[], 'abstract':[], 'authors':[] }


    results = search('Trisomy 18')
    id_list = results['IdList']
    papers = fetch_details(id_list)
    for i, paper in enumerate(papers['PubmedArticle']):
        #print("%d) %s" % (i + 1, paper['MedlineCitation']['Article']))
        print("id: %s" %  str(i))
        print()
        for keyword in  paper['MedlineCitation']['KeywordList']:
            for item in keyword:
                print(item)

        

        print("article title:")
        print("%d) %s" % (i + 1, paper['MedlineCitation']['Article']['ArticleTitle']))

        print("Abstract: ")
        print("%s" % paper['MedlineCitation']['Article']['Abstract']['AbstractText'])
        print()
        print("author:")
        for person in paper['MedlineCitation']['Article']['AuthorList']:
            print("%s %s" % (person['LastName'], person['ForeName']))
            for affiliation in person['AffiliationInfo']:
                print("%s" % affiliation['Affiliation'])
        print('<--------NEXT--------->')
    # Print the details like JSon for better view
    # print(json.dumps(papers['PubmedArticle'], indent=2, separators=(',', ':')))




    df = pd.DataFrame(data=d)

    df.to_csv("contractor_companies_licenses.csv")
