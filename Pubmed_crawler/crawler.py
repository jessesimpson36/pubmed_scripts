# pip install biopython
import json
from Bio import Entrez

def search(query):
    Entrez.email = 'email@email.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='10',
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'email@email.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results

if __name__ == '__main__':
    results = search('doolittle robert patrick')
    id_list = results['IdList']
    papers = fetch_details(id_list)
    for i, paper in enumerate(papers['PubmedArticle']):
        #print("%d) %s" % (i+1, paper['MedlineCitation']['Article']['ArticleTitle']))
        print("%d) %s" % (i + 1, paper['MedlineCitation']['Article']['ArticleTitle']))
        print('<--------NEXT--------->')
    # Print the details like JSon for better view
    #print(json.dumps(papers['PubmedArticle'], indent=2, separators=(',', ':')))
