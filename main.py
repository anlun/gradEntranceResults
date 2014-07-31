#!/usr/bin/python2
# vim: set fileencoding=utf-8 :

import urllib, os
from bs4 import BeautifulSoup
import sys, codecs
sys.stdout=codecs.getwriter('utf-8')(sys.stdout)

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

#names += ['Гражевская Александра Сергеевна']

eng_file = 'http://abiturient.spbu.ru/data/asp_doc/for_lang.htm' 
eng_filename = 'for_lang.htm'
urllib.urlretrieve(eng_file, eng_filename)

phil_file = 'http://abiturient.spbu.ru/data/asp_doc/filosofia.htm'
phil_filename = 'filosofia.htm'
urllib.urlretrieve(phil_file, phil_filename)

spec_file = 'http://abiturient.spbu.ru/data/asp_doc/spec.htm'
spec_filename = 'spec.htm'
urllib.urlretrieve(spec_file, spec_filename)

i_scores = [{}, {}, {}]
file_number = 0

def updateEngResults(filename = eng_filename, file_number = 0):
  with open(filename, 'rb') as cur_file:
    soup = BeautifulSoup(cur_file.read())
    table = soup.find('table')
    rows = table.findAll('tr')
    for tr in rows:
      cols  = tr.findAll('td')
      name  = cols[1].find(text = True)
      score = cols[2].find(text = True)
      if name == None:
        continue
      name = name.replace('\n  ', ' ')
      i_scores[file_number][name] = score
updateEngResults()

def textFromP(td):
  try:
    return td.findAll('p')[0].find(text = True)
  except:
    return None

def updatePhilResults(filename = phil_filename, file_number = 1):
  with open(filename, 'rb') as cur_file:
    soup = BeautifulSoup(cur_file.read())
    table = soup.find('table')
    rows = table.findAll('tr')
    for tr in rows:
      cols  = tr.findAll('td')
      td_num = 0
      res = map(textFromP, cols) 
      name  = res[1]
      score = res[2]
      if name == None:
        continue
      name = name.replace('\n  ', ' ')
      i_scores[file_number][name] = score
updatePhilResults()

def updateSpecResults(filename = spec_filename, file_number = 2):
  with open(filename, 'rb') as cur_file:
    soup = BeautifulSoup(cur_file.read())
    table = soup.find('table')
    rows = table.findAll('tr')
    for tr in rows:
      cols  = tr.findAll('td')
      res = map(textFromP, cols) 
      name  = res[0]
      score = res[2]
      if name == None:
        continue
      name = name.replace('\n  ', ' ')
      i_scores[file_number][name] = score
updateSpecResults()

scores = {}
for name in names:
  try:
      scores[name] =  int(i_scores[0].get(name, 0))
      scores[name] += int(i_scores[1].get(name, 0))
      scores[name] += int(i_scores[2].get(name, 0))
  except TypeError:
      pass

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
