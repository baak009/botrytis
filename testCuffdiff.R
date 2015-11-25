source("https://bioconductor.org/biocLite.R")
biocLite("cummeRbund")
library(cummeRbund)
cuff_data2 <- readCufflinks("E://thesis/outdiff_I_M_tomato/")
gene_diff_data2 <- diffData(genes(cuff_data2)) # the gene_diff data with the logfold change
sig_gene_data2 <- subset(gene_diff_data2, (significant == 'yes'))
#cuff_genes <- genes(cuff_data)

diffGeneIDs <-getSig(cuff_data2,level = "genes", alpha=1000)
diffGenes <- getGenes(cuff_data2, diffGeneIDs)
names2 <- featureNames(diffGenes)
row.names(names)=names$tracking_id
diffGenesNames<-as.matrix(names)
diffGenesNames<-diffGenesNames[,-1]
diffGenesData<-diffData(diffGenes)
row.names(diffGenesData)=diffGenesData$gene_id
diffGenesData<-diffGenesData[,-1]
diffGenesOutput<-merge(diffGenesNames,diffGenesData,by="row.names")
