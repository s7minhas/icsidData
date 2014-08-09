# Setup
setwd('/Users/janus829/Desktop/Research/icsidData')
load('panel.rda')
disp=read.csv('DisputesData.csv')

# Libraries
require(countrycode)
require(doBy)

# Helpful functions
cname=function(x){countrycode(x,'country.name','country.name')}
char=function(x){as.character(x)}
num=function(x){as.numeric(as.character(x))}
substrRight=function(x, n){substr(x, nchar(x)-n+1, nchar(x))}

# Add missing years to panel
addYrPanel=function(data, dyear, frame, remove){
	toAdd=setdiff(unique(data[,dyear]), unique(frame$year))

	# Add years
	if(length(toAdd)!=0){
		cat(paste0('Adding data for following years: '), toAdd, '\n')
		for(ii in 1:length(toAdd)){
			# Determine position of closest year
			clYr=frame$year[which.min(abs(frame$year-toAdd[ii]))]
			sliceAdd=frame[frame$year==clYr,]
			sliceAdd$year=toAdd[ii]
			frame=rbind(frame, sliceAdd)
		}
		if(remove){
			toRem=sort(unique(panel$year[which(panel$year<min(disp[,'year']))]))
			cat(paste0('Removing data for following years: '), toRem, '\n')
			frame[which(frame$year>=min(data[,dyear])),]
		} else { frame }	
	}
}

# Builds country-year dataset
cYrBld=function(data, id, idP, var, nvar, cyData, cntry, year){
	if( length( setdiff(nvar, colnames(cyData)) )>0 ){	
		# Subset relevant info from event data
		slice=data[,c(id, idP, var)]
		slice=na.omit(slice)
		toSumm=data.frame(cbind(char(slice[,1]),slice[,3],1))
		colnames(toSumm)=c(id,var,nvar)
		toSumm[,var]=num(toSumm[,var]); toSumm[,nvar]=num(toSumm[,nvar])

		# Remove duplicate partner countries (keep early version)
		sliceD=cbind(slice,sp=paste(slice[,id],slice[,idP],sep='_'))
		fm=formula(paste0(var,'~ sp'))
		minYr=summaryBy(fm, data=sliceD, FUN=min, keep.names=TRUE)
		cpairs=matrix(
			unlist( strsplit( char( minYr[,'sp'] ), '_' ) ),
			ncol=2, byrow=TRUE )
		toSummD=data.frame(cbind(cpairs[,1], minYr[,var], 1))
		colnames(toSummD)=c(id,var,nvar)
		toSummD[,var]=num(toSummD[,var]); toSummD[,nvar]=num(toSummD[,nvar])
		
		# Calculate number of occurences by year
		fm=formula(paste0(nvar,'~', id, '+', var))
		yrSumm=summaryBy(fm, data=toSumm, FUN=sum, keep.names=TRUE)
		yrSummD=summaryBy(fm, data=toSummD, FUN=sum, keep.names=TRUE)
		colnames(yrSummD)[3]=paste0(nvar,'NoDupl')

		# Merge in to dataset
		cyData$mVar=paste0(cyData[,cntry], cyData[,year])
		yrSumm$mVar=paste0(yrSumm[,id], yrSumm[,var])
		tmp=merge(cyData, yrSumm[,3:4], by='mVar', all.x=T)
		yrSummD$mVar=paste0(yrSummD[,id], yrSummD[,var])
		tmp=merge(tmp, yrSummD[,3:4], by='mVar', all.x=T)		
		
		# Clean up merged file and remove merge variable
		tmp[is.na(tmp[,nvar]),nvar]=0
		tmp[is.na(tmp[,paste0(nvar,'NoDupl')]),paste0(nvar,'NoDupl')]=0		
		tmp[,2:ncol(tmp)]
		} else { cat(paste0(nvar, ' already in dataset\n')) } 
}

# Rolling sum of BITs
csumPnl=function(data,cntry,year,var){
	data=cbind(data, NA)
	colnames(data)[ncol(data)]=paste0(var, 'C')
	data=data[order(data[,cntry],data[,year]),]
	cntries=unique(data[,cntry])
	for(ctry in cntries){
		data[which(data[,cntry]==ctry),paste0(var, 'C')] = 
			cumsum(data[which(data[,cntry]==ctry),var])
	}
	data
}