library("DESeq")
data <- read.delim("E:/test.txt", header = FALSE)
data <- read.delim("E:/readcounts/all_15_5_5.txt", header = FALSE)
data <- read.delim("E:/readcounts/all_15_3_2.txt", header = F)
total_counts_unique_botrytis <- data[,10:ncol(data)]
total_counts_unique_botrytis <- data[,10:17]

colnames(total_counts_unique_botrytis) = c("B16A", "B16B", "I12A", "I12B", "I16A", "I16B", "I24B", "I24D",
                                           "AF12", "AF16", "AF24", "M12", "M16", "M24")

colnames(total_counts_unique_botrytis) = c("B16A", "B16B", "I12A", "I12B", "I16A", "I16B", "I24B", "I24D")


rownames(total_counts_unique_botrytis) = data[,9]
botrytisDesign = data.frame(row.names = colnames(total_counts_unique_botrytis),
                            condition = c("B16", "B16", "I12", "I12", "I16", "I16", "I24", "I24",
                                          "AF12", "AF16", "AF24", "M12", "M16", "M24"),
                            libType = c("single-end", "single-end", 
                                        "single-end", "single-end",
                                        "single-end", "single-end",
                                        "single-end", "single-end",
                                        "single-end", "single-end", 
                                        "single-end", "single-end",
                                        "single-end", "single-end"
                                        ))

botrytisDesign = data.frame(row.names = colnames(total_counts_unique_botrytis),
                            condition = c("B16", "B16", "I12", "I12", "I16", "I16", "I24", "I24"
                                          ),
                            libType = c("single-end", "single-end", 
                                        "single-end", "single-end",
                                        "single-end", "single-end",
                                        "single-end", "single-end"
                            ))
head(total_counts_unique_botrytis)
condition = botrytisDesign$condition
condition

cds = newCountDataSet(total_counts_unique_botrytis, condition)
cds = estimateSizeFactors(cds)
sizeFactors(cds)
head(counts(cds, normalized = TRUE))
cds = estimateDispersions((cds))
cds = estimateDispersions(cds, fitType = c("local")) #used with only botrytis and I samples
res = nbinomTest(cds, "B16", "I16")
nieuw = na.omit(res) 
res = nieuw
#res[res$pval < 0.5,]
#plotMA(res)
#head(res)
#plotMA(res)
resSig = res[res$padj <0.1,]
head(resSig[order(resSig$pval),])
#upregulated ones
head(resSig[order(-resSig$foldChange, -resSig$baseMean),])
upregulated = resSig[order(-resSig$foldChange, -resSig$baseMean),]
#GEEN IDEE OF DIT WEL KLOPT Want zit hier nu bij geteld dat de ene conditie veel meer reads waren?
# normalizeren!
test = total_counts_unique_botrytis[total_counts_unique_botrytis$I12A > 10 & total_counts_unique_botrytis$B16A < 100, ]
sum(is.na(data))
sum(is.na(res))
sum(is.na(counts(cds,normalized = TRUE)))

hist(res$pval, breaks = 100)
hist(res$padj, breaks = 100)

coln <- colnames(total_counts_unique_botrytis)
sum_col <- colSums(total_counts_unique_botrytis[,])
colSums(total_counts_unique_botrytis)
for (i in 1:length(coln)){
  total_counts_unique_botrytis[,paste0(coln[i],"_norm")] <- 
    total_counts_unique_botrytis[,i]/sum_col[i] * 1000000
} 
normalized_total_counts_unique_botrytis<- total_counts_unique_botrytis[,c(15:28)]

high.expr <- normalized_total_counts_unique_botrytis[(normalized_total_counts_unique_botrytis$I24B_norm >
                                                        quantile(normalized_total_counts_unique_botrytis$I24B_norm, .90))|
                                                       (normalized_total_counts_unique_botrytis$I24D_norm >
                                                          quantile(normalized_total_counts_unique_botrytis$I24D_norm, .90))|
                                                       (normalized_total_counts_unique_botrytis$I12A_norm >
                                                          quantile(normalized_total_counts_unique_botrytis$I12A_norm, .90))|
                                                       (normalized_total_counts_unique_botrytis$I12B_norm >
                                                          quantile(normalized_total_counts_unique_botrytis$I12B_norm, .90))|
                                                       (normalized_total_counts_unique_botrytis$I16A_norm >
                                                          quantile(normalized_total_counts_unique_botrytis$I16A_norm, .90))|
                                                       (normalized_total_counts_unique_botrytis$I16B_norm >
                                                          quantile(normalized_total_counts_unique_botrytis$I16B_norm, .90)),]


upreg <-high.expr[high.expr$I24B_norm > 4*high.expr$B16A_norm &(
  high.expr$I24B_norm > 4*high.expr$B16B_norm) & (
    high.expr$I24D_norm > 4*high.expr$B16A_norm) & (
      high.expr$I24D_norm > 4*high.expr$B16B_norm) & (
        high.expr$I12A_norm > 4*high.expr$B16B_norm) & (
          high.expr$I12A_norm > 4*high.expr$B16A_norm) & (
            high.expr$I12B_norm > 4*high.expr$B16B_norm) & (
              high.expr$I12B_norm > 4*high.expr$B16A_norm) & (
                high.expr$I16A_norm > 4*high.expr$B16B_norm) & (
                  high.expr$I16A_norm > 4*high.expr$B16A_norm) & (
                    high.expr$I16B_norm > 4*high.expr$B16B_norm) & (
                      high.expr$I16B_norm > 4*high.expr$B16A_norm)
  
  
  ,]

