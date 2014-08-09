
import time
import urllib2
import os
from BeautifulSoup import BeautifulSoup as bsoup
import re
import string
from nltk import clean_html as clWeb
from countrycode import countrycode
import csv

def openSoup(x):
	"""Opens URL and create soup"""
	try:
		return bsoup(urllib2.urlopen(x).read())
	except urllib2.HTTPError, e:
		print 'Taking a breather...'
		time.sleep(120)
		return bsoup(urllib2.urlopen(x).read())

def cleanStrSoup(x, a, b, adj=None):
	"""Returns the text between strings a and b"""
	if adj is None: 
		adj=len(a)
	return x[x.find(a)+adj:x.find(b)]

def rPunct(text):
	"""Remove punctuation and html leftovers"""
	nwText=clWeb(text)
	puncts=string.punctuation
	repPunct = string.maketrans(string.punctuation, ' '*len(string.punctuation))
	return nwText.translate(repPunct).rstrip().lstrip()

def extInfo(raw,label):
	store=dict.fromkeys(['plaintiff','pClean','claimant','year','month','type','status'])
	store['claimant']=rPunct( cleanStrSoup(raw[0],'colspan="3">',' v. ') )
	store['plaintiff']=rPunct( cleanStrSoup(raw[0],' v. ',' (ICSID') )
	if store['plaintiff'] in 'Democratic Republic of the Congo':
		store['pClean']='CONGO, THE DEMOCRATIC REPUBLIC OF'
	else:
		store['pClean']=countrycode(
			store['plaintiff'],'country_name','country_name').upper()
	yr=cleanStrSoup(raw[0],'No. ',')</td>').split('/')
	if store['claimant'] not in 'Oded Besserglik':
		store['type']=yr[0]
		if(len(yr[1])==2 and int(yr[1])>20):
			year='19'+yr[1]
		else:
			year='20'+yr[1]
		store['year']=year
		store['month']=yr[2]
	else:
		store['type']='ARB(AF)'
		store['year']='2014'
		store['month']='2'
	store['status']=label
	return store

def scrapeICSID(address):
	soup = openSoup(address)
	page = address.split('Val=')[1]

	# Find cases
	dirty=soup.findAll('table', {'class':'rightInnerTable'})
	table=dirty[0].find('table', {'id':'tabPrc'})
	data=table.findAll('tr')

	lineBR='<tr><td>&nbsp;</td></tr>'
	newCase='<tr><td valign="top" width="30" class="contentBlueBold">'
	cases=str(data).split(newCase)
	cases=cases[1:len(cases)]
	caseData=[case.split(lineBR) for case in cases]

	# For now lets take simple approach and just pull out case-year info
	return [[extInfo(x,page)] for x in caseData]

def pullout(x):
	"""Pulls out individual dictionary element from a 
	list that contains a list of dictionaries"""
	values=[]
	for i in range(0,len(x)):
		slice=x[i]
		for j in range(0,len(slice)):
			values.append(slice[j])
	return values