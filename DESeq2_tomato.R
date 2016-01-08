# DESEQ2 tomato script
# DESEQ2
source("https://bioconductor.org/biocLite.R")
biocLite("DESeq2")
library("DESeq2")

directory <- "E:/thesis/outhtseq_tomato2_I_M_samples/" # directory with files # define this
new_directory <- paste(directory, "output_ImMm/", sep = "")
dir.create(new_directory, showWarnings = TRUE, recursive = FALSE)


logfoldValue <- 1 # define this
padjValue <- 0.05 # define this

sampleFiles <- grep(".txt", list.files(directory), value = TRUE)

#sampleCondition <-sub("(...*).*","\\1", sampleFiles) 
sampleCondition = c("I12","I12", "I16", "I16", "I24", "I24", "M", "M", "M") # define this
#sampleCondition = c("I","I", "I", "I", "I", "I", "M", "M", "M") # define this
sampleTable <- data.frame(sampleName = sampleFiles,
                          fileName = sampleFiles,
                          condition = sampleCondition)


ddsHTSeq <- DESeqDataSetFromHTSeqCount(sampleTable = sampleTable,
                                       directory = directory,
                                       design= ~ condition)
dds <-DESeq(ddsHTSeq)

dds <- dds[rowSums(counts(dds))>1,] # prefiltering
#plotDispEsts(dds)
# specify the reference level
dds$condition <- relevel(dds$condition, ref = "I12")

#results
cond <- unique(sampleCondition)
combination <- combn(cond, 2)



output = paste(new_directory,'stats', padjValue, logfoldValue,'.txt', sep = '')
write('HTSEQ-DESeq\nSampleconditions:\n', output)

for (i in 1:ncol(combination)){
  s = combination[,i]
  write(paste('combination:',s ,sep = '\t'),output, append = T)
  
  res1 <- results(dds, contrast = c("condition", s[1], s[2]))
  
  resOrdered <- res1[order(res1$padj),]
  
  p <- nrow(subset(resOrdered, padj<padjValue))
  t <- nrow(subset(resOrdered, padj<padjValue & log2FoldChange < -logfoldValue))
  v <- nrow(subset(resOrdered, padj<padjValue & log2FoldChange > logfoldValue))
  
  write(paste('padj<',padjValue,p ,sep = '\t'),output, append = T)
  write(paste('LFC >',logfoldValue, t, sep = '\t'), output, append =T)
  write(paste('LFC <',-logfoldValue, v, '\n', sep = '\t'),output, append =T)
  resSig <- subset(resOrdered, padj < padjValue & (log2FoldChange < -(logfoldValue) | log2FoldChange > logfoldValue))
  write.csv(x = resSig, file = paste(new_directory, "sig",s[1],s[2], padjValue, logfoldValue,".csv", sep = ""))
}

#res

rld <- rlog(dds)
vsd <- varianceStabilizingTransformation(dds)
head(assay(rld), 3)
library("RColorBrewer")
sampleDists <- dist(t(assay(rld)))
sampleDistMatrix <- as.matrix(sampleDists)
rownames(sampleDistMatrix) <- colnames(rld)
colnames(sampleDistMatrix) <- colnames(rld)
colors <- colorRampPalette( rev(brewer.pal(9, "Blues")) )(255)
library("pheatmap")

pheatmap(sampleDistMatrix,
         clustering_distance_rows=sampleDists,
         clustering_distance_cols=sampleDists,
         col=colors)

plotCounts(dds,gene = 'gene:Solyc09g042740.2', intgroup = c("condition"))
plotCounts(dds,gene = 'gene:Solyc01g066560.2', intgroup = c("condition"))
plotCounts(dds,gene = 'gene:Solyc04g049620.2', intgroup = c("condition"))
plotCounts(dds,gene = 'gene:Solyc12g056280.1', intgroup = c("condition"))
par(pch = 8, col = 'black')

par
#saving of the normalized counts of dds
normalized.counts <- as.data.frame(counts(dds,normalized=TRUE))
colnames(normalized.counts) = sampleCondition
sub = normalized.counts['gene:Solyc09g042740.2',]
sub = t(sub)
barplot(sub)


#to save your dds dataset
save(dds,file="E:/thesis/dds.RData")
#to load the dds dataset
load(file="E:/thesis/dds.RData")
