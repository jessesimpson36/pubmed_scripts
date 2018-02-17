# pip install biopython
import json
from Bio import Entrez
import pandas as pd

# Queries the information in pubmed.
def search(query):
    Entrez.email = 'email@email.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='1000000000', # modify this to accept all articles when ready.
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

    d = { 'pmid':[],'rare_disease':[],'keywords':[], 'article_date':[], 'article_title':[], 'abstract':[], 'authors':[], 'authors_affiliations':[] }
    pmid, rare_disease, keywords, article_date, article_title, abstract, authors = "", "", "", "", "", "", ""  
    with open("diseases.txt", "r") as disease_file:
        
        for disease in disease_file:
            try:
                pmid, rare_disease, keywords, article_date, article_title, abstract, authors, authors_affiliations = "", "", "", "", "", "", "", "" 
                disease = disease.strip()

                # appending AND NC to the end will hopefully give values from north carolina.
                results = search(disease + " AND (NC | North Carolina)")
                id_list = results['IdList']
                papers = fetch_details(id_list)
                for i, paper in enumerate(papers['PubmedArticle']):
                    pmid, rare_disease, keywords, article_date, article_title, abstract, authors, authors_affiliations = "", "", "", "", "", "", "", ""
                    print("ID: ")
                    print(paper['MedlineCitation']['PMID'])
                    pmid = str(paper['MedlineCitation']['PMID'])
                    print()
    
                    rare_disease = disease
    
                    print("Key Words:")
                    for keyword in  paper['MedlineCitation']['KeywordList']:
                        for item in keyword:
                            print(item + ", ")
                            keywords = keywords + item + ", "
            
                    print()
                    print("Date:")
                    for date in paper['MedlineCitation']['Article']['ArticleDate']:
                        print( str(date['Year']) + "/" + date['Month'] +"/"+ date['Day'])
                        article_date = str(date['Year']) + "/" + date['Month'] + "/" + date['Day']
                    print()
            
                    print("article title:")
                    print("%d) %s" % (i + 1, str(paper['MedlineCitation']['Article']['ArticleTitle']).replace("[",'').replace("]","")))
                    article_title = str(paper['MedlineCitation']['Article']['ArticleTitle']).replace("[",'').replace("]","")
            
                    print("Abstract: ")
                    for abstract_data in paper['MedlineCitation']['Article']['Abstract']['AbstractText']:
                        print(abstract_data)
                        abstract = abstract + abstract_data
    
                    print()
                    print("author:")
                    for person in paper['MedlineCitation']['Article']['AuthorList']:
                        print("%s %s" % (person['LastName'], person['ForeName']))
                        for affiliation in person['AffiliationInfo']:
                            print("%s" % affiliation['Affiliation'])
                            affiliation = str(affiliation['Affiliation']).replace(",","")
                            pre_authors = "%s  %s," % (person['LastName'], person['ForeName'])
                            if "NC" in affiliation or "North Carolina" in affiliation:
                                authors = authors + pre_authors
                                authors_affiliations = authors_affiliations + affiliation + ","
    
                    print('<--------NEXT--------->')
        
                    d['pmid'].append(pmid)
                    d['rare_disease'].append(rare_disease)
                    d['keywords'].append(keywords)
                    d['article_date'].append(article_date)
                    d['article_title'].append(article_title)
                    d['abstract'].append(abstract)
                    d['authors'].append(authors)
                    d['authors_affiliations'].append(authors_affiliations)

            except RuntimeError:
                continue
            except KeyError:
                continue
    df = pd.DataFrame(data=d)

    df.to_csv("pubmed_articles.csv")
