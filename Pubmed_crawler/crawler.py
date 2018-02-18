# pip install biopython
import json
from Bio import Entrez
import pandas as pd
import sys
import traceback

def progress_bar(iteration, total, barLength=50):
    percent = int(round((iteration / total) * 100))
    nb_bar_fill = int(round((barLength * percent) / 100))
    bar_fill = '#' * nb_bar_fill
    bar_empty = ' ' * (barLength - nb_bar_fill)
    sys.stdout.write("\r  [{0}] {1}%".format(str(bar_fill + bar_empty), percent))
    sys.stdout.flush()

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
    with open("diseases.txt", "r", encoding='utf-8') as disease_file:
        j = 0
        for disease in disease_file:
            try:
                print("  " + disease)
                j += 1
                # progress_bar(j,6537,100)
                progress_bar(j,156,100)

                pmid, rare_disease, keywords, article_date, article_title, abstract, authors, authors_affiliations = "", "", "", "", "", "", "", "" 
                disease = disease.strip()

                # appending AND NC to the end will hopefully give values from north carolina.
                try:
                    results = search(disease + " AND (NC OR North Carolina)")
                    id_list = results['IdList']
                    papers = fetch_details(id_list)
                # May throw a runtime error if there is no results for the searched disease.
                except RuntimeError:
                    continue
                
                for i, paper in enumerate(papers['PubmedArticle']):
                    pmid, rare_disease, keywords, article_date, article_title, abstract, authors, authors_affiliations = "", "", "", "", "", "", "", ""
                    # print("ID: ")
                    # print(paper['MedlineCitation']['PMID'])
                    pmid = str(paper['MedlineCitation']['PMID'])
                    # print()

                    rare_disease = disease.replace(",","")

                    # print("Key Words:")
                    for keyword in  paper['MedlineCitation']['KeywordList']:
                        for item in keyword:
                            # print(item + ", ")
                            keywords = keywords + item + ", "
            
                    # print()
                    # print("Date:")
                    for date in paper['MedlineCitation']['Article']['ArticleDate']:
                        # print( str(date['Year']) + "/" + date['Month'] +"/"+ date['Day'])
                        article_date = str(date['Year']) + "/" + str(date['Month']) + "/" + str(date['Day']) 
                    # print()
            
                    # print("article title:")
                    # print("%d) %s" % (i + 1, str(paper['MedlineCitation']['Article']['ArticleTitle']).replace("[",'').replace("]","")))
                    article_title = str(paper['MedlineCitation']['Article']['ArticleTitle']).replace("[",'').replace("]","").replace(",","")
            
                    # print("Abstract: ")
                    if "Abstract" in paper['MedlineCitation']['Article'].keys():
                        for abstract_data in paper['MedlineCitation']['Article']['Abstract']['AbstractText']:
                            # print(abstract_data)
                            abstract = abstract + str(abstract_data).replace(",","")

                    # print()
                    # print("author:")
                    if "AuthorList" in paper['MedlineCitation']['Article'].keys():
                        for person in paper['MedlineCitation']['Article']['AuthorList']:
                            # print("%s %s" % (person['LastName'], person['ForeName']))
                            for affiliation in person['AffiliationInfo']:
                                # print("%s" % affiliation['Affiliation'])
                                affiliation = str(affiliation['Affiliation']).replace(",","")
                                if 'LastName' in person.keys() and 'ForeName' in person.keys():
                                    pre_authors = "%s  %s," % (str(person['LastName']), str(person['ForeName']))
                                    if "NC" in affiliation or "North Carolina" in affiliation:
                                        authors = authors + pre_authors + " | "
                                        authors_affiliations = authors_affiliations + str(affiliation) + " | "
                    

                    # print('<--------NEXT--------->')
        
                    d['pmid'].append(pmid)
                    d['rare_disease'].append(rare_disease)
                    d['keywords'].append(keywords)
                    d['article_date'].append(article_date)
                    d['article_title'].append(article_title)
                    d['abstract'].append(abstract)
                    d['authors'].append(authors)
                    d['authors_affiliations'].append(authors_affiliations)

            except:
                    df = pd.DataFrame(data=d)
                    df.to_csv("pubmed_articles_final_part2.csv")
                    traceback.print_exc()
                    exit()

            


    df = pd.DataFrame(data=d)

    df.to_csv("pubmed_articles_final_part2.csv")
