
import os
import csv

# Choose directory
basePath='/Users/janus829/Desktop/Research/icsidData'
os.chdir(basePath)

# My helper functions
from ICSIDhelpers import *

# Load in parsable version of base webpage from UNCTAD's Investment Policy Hub
addresses = ['https://icsid.worldbank.org/ICSID/FrontServlet?requestType=GenCaseDtlsRH&actionVal=ListConcluded','https://icsid.worldbank.org/ICSID/FrontServlet?requestType=GenCaseDtlsRH&actionVal=ListPending']

data=scrapeICSID(addresses[0])
data.extend(scrapeICSID(addresses[1]))

# Write to csv
keys=['type','plaintiff','claimant','year','month']
f=open('DisputesData.csv', 'wb')
writer=csv.DictWriter(f, keys )
writer.writer.writerow( keys )
writer.writerows( pullout(data)  )