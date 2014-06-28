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

# Choose directory
os.chdir('/Users/janus829/Desktop/Research/icsidData')

# # My helper functions
# from invPolHubHelpers import *
def openSoup(x):
	"""Opens URL and create soup"""
	return bsoup(urllib2.urlopen(x).read())


# Load in parsable version of base webpage from UNCTAD's Investment Policy Hub
address = 'https://icsid.worldbank.org/ICSID/FrontServlet?requestType=GenCaseDtlsRH&actionVal=ListConcluded'
# address = 'https://icsid.worldbank.org/ICSID/FrontServlet?requestType=GenCaseDtlsRH&actionVal=ListPending'

soup = openSoup(address)

# Find cases
dirtyCases = soup.findAll('td', {'class':'contentBlueBold'}, colspan='3')

temp=dirtyCases[1]



for i in dirtyCases:
	print i

# Find links to specific countries


# Write to csv
keys=['sender','partner','signDate','ratifDate','status','termDate','termType','treatyLang']
f=open('BITsData.csv', 'wb')
writer=csv.DictWriter(f, keys )
writer.writer.writerow( keys )
writer.writerows( pullout(bitData)  )