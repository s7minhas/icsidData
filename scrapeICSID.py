
import os
from compiler.ast import flatten
import csv

# Choose directory
basePath='/Users/janus829/Desktop/Research/icsidData'
os.chdir(basePath)

# My helper functions
from ICSIDhelpers import *

# Load in parsable version of base webpage from UNCTAD's Investment Policy Hub
addresses = ['https://icsid.worldbank.org/ICSID/FrontServlet?requestType=GenCaseDtlsRH&actionVal=ListConcluded','https://icsid.worldbank.org/ICSID/FrontServlet?requestType=GenCaseDtlsRH&actionVal=ListPending']

dataConc=scrapeICSID(addresses[0])
dataPend=scrapeICSID(addresses[1])
data=flatten([dataConc,dataPend])

# Write to csv
keys=['type','plaintiff','claimant','year','month']
f=open('DisputesData.csv', 'wb')
writer=csv.DictWriter(f, keys )
writer.writer.writerow( keys )
writer.writerows( pullout(data)  )