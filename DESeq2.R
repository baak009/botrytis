# DESEQ2
source("https://bioconductor.org/biocLite.R")
biocLite("DESeq2")
library("DESeq2")
directory <- "E:/thesis/outhtseq_tomato2/"
sampleFiles <- grep("counts", list.files(directory), value = TRUE)
sampleCondition <-sub("(.*m).*","\\1", sampleFiles)
sampleCondition = c("I12","I12","I16","I16","I24","I24","M12","M16", "M24")
sampleTable <- data.frame(sampleName = sampleFiles,
                          fileName = sampleFiles,
                          condition = sampleCondition)


ddsHTSeq <- DESeqDataSetFromHTSeqCount(sampleTable = sampleTable,
                                       directory = directory,
                                       design= ~ condition)
dds <-DESeq(ddsHTSeq)
dds <- estimateSizeFactors(dds)
dds <- estimateDispersions(dds)
dds <- nbinomWaldTest(dds)
plotDispEsts(dds)
res <-results(dds)
res
resSig = res[res$padj <0.1,]
head(resSig[order(resSig$pval),])
summary(res)
sampleFiles
rld <- rlog(dds)

rld <- rlog(dds)
vsd <- varianceStabilizingTransformation(dds)
head(assay(rld), 3)
library("RColorBrewer")
sampleDists <- dist(t(assay(rld)))
sampleDistMatrix <- as.matrix(sampleDists)
rownames(sampleDistMatrix) <- paste(rld$condition, rld$type, sep="-")
colnames(sampleDistMatrix) <- NULL
colors <- colorRampPalette( rev(brewer.pal(9, "Blues")) )(255)
library("pheatmap")
pheatmap(sampleDistMatrix,
         clustering_distance_rows=sampleDists,
         clustering_distance_cols=sampleDists,
         col=colors)

