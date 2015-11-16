#!/usr/bin/env python

import urllib2
from bs4 import BeautifulSoup


# need to add doc number
url = 'https://apps.webofknowledge.com/full_record.do?product=UA&search_mode=GeneralSearch&qid=3&SID=4FU9EfsOv1yoMWFj6ac&page=1&doc='
url = 'https://apps.webofknowledge.com/full_record.do?product=UA&search_mode=GeneralSearch&qid=3&SID=1CnSdiSGNBYzkPof4Er&page=1&doc='

for i in range(1,2):
  response = urllib2.urlopen(url + str(i))
  html = response.read()
  soup = BeautifulSoup(html, 'html.parser')

  #print (soup.prettify())


  # filter only the interesting ones
  #content = soup.find_all(class_="l-content")
  content = soup.find_all('value')

  # fields
  title = soup.find_all(class_="title")
  fr = soup.find_all(class_="FR_field")
  publication = soup.find_all(class_='sourceTitle')

  # publication info
  pub_info = soup.find_all(class_="FR_field")
  # TODO -- filter all as dictionary class_="FR_label" : value

  # impact factor (inside the table)
  impact_factors = soup.find_all(class_="Impact_Factor_table")

  # getting Abstract and Keywords, etc
  additional_info = soup.find_all(class_="block-record-info")

  for el in additional_info:
    print el.find(class_='title3')

    try:
      for ch in el.find(class_='FR_label'):
        _x = BeautifulSoup(ch,'html.parser')
        if _x.span:
            print _x.span
        elif _x.p:
            print _x.p
    except:
        print 'Error here'

    try:
      for ch in el.find(class_='FR_field'):
        _x = BeautifulSoup(ch,'html_parser')
        if _x.span:
            print _x.span
        elif _x.p:
            print _x.p
    except:
        print 'Error here'
