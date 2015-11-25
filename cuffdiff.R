#cufflinks

source("https://bioconductor.org/biocLite.R")
biocLite("cummeRbund")
library(cummeRbund)
cuff_data <- readCufflinks("E://thesis/outdiff_I_M_tomato/")
cuff_data <- readCufflinks(("E://thesis/outdiff_testt"))
cuff_data <- readCufflinks(("E://thesis/outdiff_M_tomato/"))
cuff_data <- readCufflinks(("E://thesis/outdiff_I_B_botrytis/"))
disp <- dispersionPlot(genes(cuff_data))
disp
csDensity(genes(cuff_data), replicates = T) #can with and without replicates
b <- csBoxplot(genes(cuff_data))
b
s <- csScatterMatrix(genes(cuff_data))
s
s <- csScatter(genes(cuff_data), 'M12', 'M16', smooth = T)
s
dend <- csDendro(genes(cuff_data), replicates = T)
v <- csVolcanoMatrix(genes(cuff_data))
test = genes(cuff_data)


diffGeneIDs <-getSig(cuff_data,level = "genes", alpha=1000)
diffGenes <- getGenes(cuff_data, diffGeneIDs)

names <- featureNames(diffGenes)


csVolcano(genes(cuff_data), "M12Am", "M16Am")
cuff_data
gene_diff_data <- diffData(genes(cuff_data))
sig_gene_data <- subset(gene_diff_data, (significant == 'yes'))
nrow(sig_gene_data)
head(sig_gene_data)
mySigGeneIds <- getSig(cuff_data, alpha=0.05, level = 'genes')
head (mySigGeneIds)
length(mySigGeneIds)

sig_gene_data_M24_I24 <-(getSig(cuff_data, x = "M24", y ="I24", alpha = 0.05, level = 'genes'))
length(sig_gene_data_M24_I24)
sig_gene_data_M16_M12 <-(getSig(cuff_data, x = "M16", y ="M12", alpha = 0.05, level = 'genes'))
length(sig_gene_data_M16_M12)

mygene <- getGene(cuff_data, 'Solyc00g005040.2')
expressionBarplot(mygene)
(genes(cuff_data))
b <- csBoxplot(genes(cuff_data))
b

head(features(mygene))

diffGeneIDs <- getSig(cuff_data, level = 'genes', alpha=0.05)
diffGenes <-getGenes(cuff_data, diffGeneIDs)
head(featureNames(diffGenes))


mysigMat <- sigMatrix(cuff_data, level = 'genes', alpha =0.05)
#png('E://thesis/outdiff_I_M_tomato/graphs/mysigMat.png')
png('E://thesis/outdiff_I_B_botrytis/graphs/mysigMat.png')
mysigMat
dev.off()


cuff_genes <- genes(cuff_data)
