#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib2
import csv
from bs4 import BeautifulSoup


# need to add doc number
url = 'https://apps.webofknowledge.com/full_record.do?product=UA&search_mode=GeneralSearch&qid=3&SID=1CnSdiSGNBYzkPof4Er&page=1&doc='

# Header
fieldnames = ['publication','title','authors_emails','authors_names','authors_addresses','institutions','keywords','publication year','if','times_cited']

csvfile = open('results.csv','w')
csv_writer = csv.DictWriter(csvfile,delimiter='\t',fieldnames=fieldnames)
csv_writer.writeheader()

for i in range(1,100):
  print 'getting document ',i,' url: ',url

  response = urllib2.urlopen(url + str(i))
  html = response.read()
  soup = BeautifulSoup(html, 'html.parser')

  #print (soup.prettify())

  # publication name
  try:
    publication = soup.find_all(class_='sourceTitle')
    publication = publication[0].get_text().strip()
    #DEBUG print publication
  except:
    print 'problem getting the publication name'
    publication = soup.find(class_='sourceTitle').get_text()

  if publication in ['NATURE','SCIENCE']:

    csv_row = [] 
    csv_row.append(publication)

    # title
    try:
      title = soup.find_all(class_="title")
      title = title[0].get_text().strip().encode('utf-8')
      #DEBUG print title
      csv_row.append(title)
    except:
      print 'problem getting the title'
      print soup.find_all(class_="title")



    # article informations
    fr_fields = soup.find_all(class_="FR_field")


    # authors emails
    authors = {}
    try:
      # email addresses
      authors['email'] = []
      for values in fr_fields:
        if values.span:
          label = values.span.get_text().strip()
          # authors email
          if label == 'E-mail Addresses:':
            for emails in values.select('a'):
              authors['email'].append(emails.get_text().strip().encode('utf-8'))
      #DEBUG print authors
      csv_row.append(authors['email'])
    except:
      print 'problem getting the authors emails'


    # authors names
    authors['names'] = set()
    try:
      for ch in soup.find_all(title="Find more records by this author"):
        authors['names'].add(ch.get_text().encode('utf-8'))
      #DEBUG print authors
      csv_row.append(authors['names'])
    except:
      print 'Error getting authors names'


    # authors addresses
    authors['addresses_names'] = set()
    authors['addresses'] = set()
    try:
      # organization names
      for ch in soup.select('td[class^="fr_address_"]'):
        authors['addresses'].add(ch.get_text().strip().encode('utf-8'))
      for ch in soup.find_all('preferred_org'):
        authors['addresses_names'].add(ch.get_text().strip().encode('utf-8'))
      #DEBUG print authors
      #DEBUG print authors
      csv_row.append(list(authors['addresses']))
      csv_row.append(list(authors['addresses_names']))
    except:
      print 'Error getting authors addresses'




    # impact factor
    try:
      impact_factors = soup.find_all(class_="Impact_Factor_table")
      _ifs = []
      for _if in impact_factors[0].select('td'):
        _ifs.append(float(_if.get_text().strip()))
      # DEBUG print _ifs
    except:
      print 'problem getting the impact factors'
      impact_factors = soup.find_all(class_="Impact_Factor_table")


    # publication info
    try:
      pub = {}
      for values in fr_fields:
        if values.span:
          label = values.span.get_text().strip()
          # publication date
          if label == 'Published:':
            pub['date'] = values.value.get_text().strip()
          # ISSN 
          elif label == 'ISSN:':
            pub['issn'] = values.value.get_text().strip()
          # publication domain 
          elif label == 'Research Domain':
            pub['domain'] = values.value.get_text().strip()
          # publication volume 
          elif label == 'Volume:':
            pub['volume'] = values.value.get_text().strip()
          # publication issue
          elif label == 'Issue:':
            pub['issue'] = values.value.get_text().strip()
          # publication pages
          elif label == 'Pages:':
            pub['pages'] = values.value.get_text().strip()
      #DEBUG print pub
    except:
      fr_fields = soup.find_all(class_="FR_field")
      print 'problem getting the publication info'


    # keywords
    keywords = set()
    try:
      for ch in soup.find_all(title="Find more records by this keywords plus"):
        keywords.add(ch.get_text())
      #DEBUG print keywords
    except:
        print 'Error getting keywords'


    # citations
    try:
      cited_references = int(soup.find(title="View this record's bibliography").get_text().strip())
      times_cited = int(soup.find(title="View all of the articles that cite this one").get_text().strip())
      #DEBUG print 'cited references',cited_references
      #DEBUG print 'times cited',times_cited
 except:
      print 'Error getting citations'
    
    csv_row.append(list(keywords))
    csv_row.append(pub['date'])
    csv_row.append(_ifs)
    csv_row.append(times_cited)
    #csv_writter.writerow('keywords','publication year','if','times_cited')

    # save everything to a file
    csv_writer.writerow({'publication':publication,'title':title,'authors_emails':authors['email'],'authors_names':list(authors['names']),'authors_addresses':list(authors['addresses']),'institutions':list(authors['addresses_names']),'keywords':list(keywords),'publication year':pub['date'],'if':_ifs,'times_cited':times_cited})
