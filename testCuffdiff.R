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
#diffGenesNames<-as.matrix(names)
#diffGenesNames<-diffGenesNames[,-1]
#diffGenesData<-diffData(diffGenes)
#row.names(diffGenesData)=diffGenesData$gene_id
#diffGenesData<-diffGenesData[,-1]
#diffGenesOutput<-merge(diffGenesNames,diffGenesData,by="row.names")

M12_M16<-subset(gene_diff_data2, gene_diff_data2$sample_1 == 'M12' & gene_diff_data2$sample_2 == 'M16')
M12_M24<-subset(gene_diff_data2, gene_diff_data2$sample_1 == 'M12' & gene_diff_data2$sample_2 == 'M24')
M12_M16_status <- subset(M12_M16, M12_M16$status == 'OK')

M12_M16_q <- subset(M12_M16_status, M12_M16_status$q_value < 0.05)
M12_M16_lfc<- subset(M12_M16_q, M12_M16_q$log2_fold_change >= 3.32 | M12_M16_q$log2_fold_change <= -3.32 )
M12_M16_inf <- subset(M12_M16_lfc, M12_M16_lfc$log2_fold_change != 'Inf' & M12_M16_lfc$log2_fold_change != '-Inf' )
M12_16_t_not_na <- subset(M12_M16_lfc, M12_M16_lfc$test_stat != 'NA')


M12_I24<-subset(gene_diff_data2, gene_diff_data2$sample_1 == 'M12' & gene_diff_data2$sample_2 == 'I24')
M12_I24_lfc_median <- (median(M12_I24$log2_fold_change))
M12_I24_lfc_mean <- (mean(abs(M12_I24$log2_fold_change)))
M12_I24_lfc_mode<- (mode(M12_I24$log2_fold_change))
M12_I24 <- subset(M12_I24, M12_I24$status == 'OK')
M12_I24 <-subset(M12_I24, M12_I24$q_value < 0.05)
M12_I24 <-subset(M12_I24, M12_I24$log2_fold_change > 1 | M12_I24$log2_fold_change < -1)

#diffGeneIDs <-getSig(cuff_data2,level = "genes", sample("M12","I24"), alpha=0.05)
diffGenes <- getGenes(cuff_data2, diffGeneIDs)
genes <- (diffData(diffGenes))
head(featureNames(diffGenes))

mygene <- getGene(cuff_data2, 'XLOC_022547')
diffData(mygene)
rld <- rlog(dds)
plotPCA(rld)
