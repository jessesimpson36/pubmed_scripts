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

    d = { 'pmid':[],'keywords':[], 'date_completed':[], 'date_revised':[], 'article_date':[], 'article_title':[], 'abstract':[], 'authors':[] }


    results = search('Trisomy 18')
    id_list = results['IdList']
    papers = fetch_details(id_list)
    for i, paper in enumerate(papers['PubmedArticle']):
        print("ID: ")
        print(paper['MedlineCitation']['PMID'])
        print()
        print("Key Words:")
        for keyword in  paper['MedlineCitation']['KeywordList']:
            for item in keyword:
                print(item)

        print()
        print("Date:")
        for date in paper['MedlineCitation']['Article']['ArticleDate']:
            print( str(date['Year']) + "/" + date['Month'] +"/"+ date['Day'])
        print()

        print("article title:")
        print("%d) %s" % (i + 1, str(paper['MedlineCitation']['Article']['ArticleTitle']).replace("[",'').replace("]","")))

        print("Abstract: ")
        for abstract in paper['MedlineCitation']['Article']['Abstract']['AbstractText']:
            print(abstract)
        print()
        print("author:")
        for person in paper['MedlineCitation']['Article']['AuthorList']:
            print("%s %s" % (person['LastName'], person['ForeName']))
            for affiliation in person['AffiliationInfo']:
                print("%s" % affiliation['Affiliation'])
        print('<--------NEXT--------->')


    df = pd.DataFrame(data=d)

    df.to_csv("pubmed_articles.csv")
