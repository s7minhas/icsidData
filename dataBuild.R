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
tmp=data.frame(disp[,c('cyear','status')])
tmp$concDispute=0; tmp$concDispute[tmp$status=='ListConcluded']=1
tmp$pendDispute=0; tmp$pendDispute[tmp$status=='ListPending']=1
tmp=summaryBy(concDispute + pendDispute ~ cyear, data=tmp, FUN=sum, keep.names=T)
disp=merge(tmp, unique(disp[,c('cyear','ccode','cname','year')]), by='cyear')

# Create panel frame and subset to relev vars
dataPanel=addYrPanel(disp, 'year', panel[,1:6], remove=TRUE) # extend panel
dataPanel$cyear=paste0(dataPanel$ccode,dataPanel$year)
relVars=c('cyear','concDispute','pendDispute')
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