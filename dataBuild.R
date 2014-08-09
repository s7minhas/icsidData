# Load workspace
source('/Users/janus829/Desktop/Research/icsidData/setup.R')

# Clean up
disp$type=char(disp$type)
disp$type[disp$type=='1 Ltd.  v. Republic of Peru  (ICSID Case No. ARB']='ARB'

# Clean country names in BITData
disp$pClean[disp$plaintiff=='United Mexican States']='MEXICO'
disp$cname=cname(disp$pClean)
disp$cname[disp$pClean=='HELLENIC REPUBLIC']='GREECE'
disp$cname[disp$pClean=='FRENCH REPUBLIC']='FRANCE'
disp$cname[disp$pClean=='ITALIAN REPUBLIC']='ITALY'

# Drop cases where plaintiffs are companies
disp$drop=0
disp[which(is.na(disp$cname)),'drop']=1
disp$drop[disp$plaintiff=='Perupetro S A']=1
disp=disp[which(disp$drop!=1),1:(ncol(disp)-1)]

# Add numeric id for countries
# disp$cnameYear=paste0(disp$cname,disp$year)
disp$ccode=panel$ccode[match(disp$cname,panel$cname)]
disp$cyear=paste0(disp$ccode,disp$year)

# Add dispute vars
disp$concDispute=0; disp$concDispute[disp$status=='ListConcluded']=1
disp$pendDispute=0; disp$pendDispute[disp$status=='ListPending']=1
disp$dispType=disp$type

# Create panel frame and subset to relev vars
dataPanel=addYrPanel(disp, 'year', panel[,1:6], remove=TRUE) # extend panel
dataPanel$cyear=paste0(dataPanel$ccode,dataPanel$year)
relVars=c('cyear','concDispute','pendDispute','dispType')
disp=disp[,relVars]

# Merge
dispPanel=merge(dataPanel,disp,by='cyear',all.x=T,all.y=T)
dispPanel$concDispute[is.na(dispPanel$concDispute)]=0
dispPanel$pendDispute[is.na(dispPanel$pendDispute)]=0

# Calculating rolling sums
vars=c('concDispute','pendDispute')
for(var in vars){dispPanel=csumPnl(dispPanel,'cname','year',var)}

# Save data
save(dispPanel,file='dispPanel.rda')