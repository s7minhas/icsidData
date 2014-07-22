# Helpers
import requests
import time
import urllib2
import os
import re
from BeautifulSoup import BeautifulSoup as bsoup
import nltk
from countrycode import countrycode
from compiler.ast import flatten
import csv
import pattern
from pattern.web import URL

# Choose directory
os.chdir('/Users/janus829/Desktop/Research/icsidData')

# # My helper functions
# from invPolHubHelpers import *
def openSoup(x):
	"""Opens URL and create soup"""
	return bsoup(urllib2.urlopen(x).read())

def cleanStrSoup(x, a, b, adj=None):
	"""Returns the text between strings a and b"""
	if adj is None: 
		adj=len(a)
	return x[x.find(a)+adj:x.find(b)]


# Load in parsable version of base webpage from UNCTAD's Investment Policy Hub
address = 'https://icsid.worldbank.org/ICSID/FrontServlet?requestType=GenCaseDtlsRH&actionVal=ListConcluded'
# address = 'https://icsid.worldbank.org/ICSID/FrontServlet?requestType=GenCaseDtlsRH&actionVal=ListPending'

soup = openSoup(address)

# Find cases
dirty=soup.findAll('table', {'class':'rightInnerTable'})
table=dirty[0].find('table', {'id':'tabPrc'})
data=table.findAll('tr')

lineBR='<tr><td>&nbsp;</td></tr>'
newCase='<tr><td valign="top" width="30" class="contentBlueBold">'
cases=str(data).split(newCase)
cases=cases[1:len(cases)]
caseData=[case.split(lineBR) for case in cases]

tmp=[]
for i in [nltk.clean_html(x).split(',') for x in caseData[10]]:
	if len(i.strip())!=0:
		tmp.append(i.strip())

# Write to csv
keys=['sender','partner','signDate','ratifDate','status','termDate','termType','treatyLang']
f=open('BITsData.csv', 'wb')
writer=csv.DictWriter(f, keys )
writer.writer.writerow( keys )
writer.writerows( pullout(bitData)  )