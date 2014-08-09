# Helpers
import requests
import time
import urllib2
import os
import re
from BeautifulSoup import BeautifulSoup as bsoup
import csv
import pattern
from pattern.web import URL

def openSoup(x):
	"""Opens URL and create soup"""
	return bsoup(urllib2.urlopen(x).read())

def cleanStrSoup(x, a, b, adj=None):
	"""Returns the text between strings a and b"""
	if adj is None: 
		adj=len(a)
	return x[x.find(a)+adj:x.find(b)]

def extInfo(raw,label):
	store=dict.fromkeys(['plaintiff','claimant','year','month'])
	store['plaintiff']=cleanStrSoup(raw[0],'colspan="3"',' v. ')
	store['claimant']=cleanStrSoup(raw[0],' v. ',' (ICSID')
	yr=cleanStrSoup(raw[0],'No. ARB/',')</td>').split('/')
	if(len(yr[0])==2 and int(yr[0])>20):
		year='19'+yr[0]
	else:
		year='20'+yr[0]
	store['year']=year
	store['month']=yr[1]
	store['type']=label
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
	return [extInfo(x,page) for x in caseData]

def pullout(x):
	"""Pulls out individual dictionary element from a 
	list that contains a list of dictionaries"""
	values=[]
	for i in range(0,len(x)):
		slice=x[i]
		for j in range(0,len(slice)):
			values.append(slice[j])
	return values