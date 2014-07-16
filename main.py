#!/usr/bin/python2
# vim: set fileencoding=utf-8 :

import urllib, os
from bs4 import BeautifulSoup

names_file = 'https://cabinet.spbu.ru/Lists/ASP_EntryLists/list1_1_4_1000022_1000006_.html'
names_filename = 'names.html'

urllib.urlretrieve(names_file, names_filename)

names = []
with open(names_filename, 'rb') as cur_file:
  soup = BeautifulSoup(cur_file.read())
  table = soup.find('table')
  columns = table.findAll('td')
  counter = 0
  cur_name = ''
  for td in columns:
    if counter == 0:
      cur_name = ''
    elif counter < 4:
      cur_name += td.find(text = True)
    elif counter == 4:
      names.append(cur_name.strip())
    counter = (counter + 1) % 6

eng_file = 'http://abiturient.spbu.ru/data/asp_doc/for_lang.htm' 
eng_filename = 'for_lang.htm'

urllib.urlretrieve(eng_file, eng_filename)

eng_scores = {}
with open(eng_filename, 'rb') as cur_file:
  soup = BeautifulSoup(cur_file.read())
  table = soup.find('table')
  rows = table.findAll('tr')
  for tr in rows:
    cols  = tr.findAll('td')
    name  = cols[1].find(text = True)
    score = cols[2].find(text = True)
    if name == None:
      continue
    eng_scores[name] = score

scores = {}
for name in names:
  eng_score = eng_scores.get(name, -1)
  scores[name] = eng_score

def tupComp(x, y):
  if x[1] < y[1]:
    return 1
  elif x[1] == y[1]:
    return 0
  else:
    return -1

pos = 1
for rec in sorted(scores.items(), cmp = tupComp):
  print str(pos) + '.', rec[0], rec[1]
  pos += 1
