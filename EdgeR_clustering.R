source("https://bioconductor.org/biocLite.R")
biocLite("edgeR")
biocLite("ggplot2")

library('edgeR')
library('ggplot2')
dir = "E:/thesis/outhtseq_botrytis_merged/"
data <- read.delim("E:/thesis/outhtseq_botrytis_merged/htseq_botrytis_merged.txt", row.names = 1, header = F)
tail(data)
data <- data[c(0:(nrow(data)-5)),] #remove htseq total counts
tail(data)
colnames(data) = c("B16A", "B16B", "I12A", "I12B", "I16A", "I16B", "I24B", "I24D",
                   "M12", "M16", "M24")
data <-  data[,0:(ncol(data)-3)] # remove tomato samples
#data <- data[1:(nrow(data)-30000),]

group <- c('B16', 'B16', 'I12','I12','I16','I16','I24','I24')
dge <- DGEList(counts = data, group = group)
#y$samples


dge <- estimateCommonDisp(dge)
dge <- estimateTagwiseDisp(dge)
dge.cpm <- cpm(dge,log=T,normalized.lib.sizes=T)

genes.cor <- cor(t(dge.cpm),method="pearson")

genes.dist<- as.dist(0.5 - 0.5 * (genes.cor) )
hc_tree <- hclust (genes.dist, method="complete" )

# pdf(file=paste("patterns_",temperature,".pdf",sep=""),12,8)
jpeg('E:/thesis/outhtseq_botrytis_merged/hctree.jpg')
plot(hc_tree)
dev.off()

hc<- cutree(hc_tree, h=0.4)
table(hc)
hc <- cutree(hc_tree, h= 0.8)


par(mfrow=c(1,1),mgp=c(3,0.5,0),mar=c(5,3,0.75,0.5),tck=-0.025,omi=c(0.1,0.5,0.5,0.1))
par(las=2)
#eerste honderd grootste clusters
for (loop in as.integer(names(sort(table(hc), decr = T)[1:20]))) { 
  IDs <- names(hc)[hc == loop]
  df <- data.frame(dge.cpm[rownames(dge.cpm) %in% IDs,])
  df.scaled<-apply(df,1,scale)
  names(df.scaled)<-names(df)
  colnames(df.scaled)<-rownames(df)
  rownames(df.scaled)<-colnames(df)
  df.new <- as.data.frame(as.table(as.matrix(df.scaled)))
  names(df.new) <- c("timepoint","gene","Z_score")
  #jpeg(paste("E:/thesis/outhtseq_botrytis_merged/clust", loop, ".png", sep=""))
  print(ggplot(df.new,aes(x=timepoint,y=Z_score)) +
          geom_point()  + theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
          stat_smooth(se=FALSE,method="loess") +
          labs(title=paste("cluster",loop,", size:",length(IDs))) +
          theme(legend.text = element_text(size = 6)))
  ggsave(paste(dir, "clust", loop, ".png", sep=""), width=5, height = 5, dpi=100)
  clust1 = row.names(data)[hc==loop]
  write.csv(dge.cpm[clust1,], file = paste(dir, "clust", loop, ".csv", sep=""))
}
clust <- 8
clust1 = row.names(data)[hc==clust] # get the names of the genes in the cluster
clust1[1]
dge.cpm[clust1,] # get the normalized values of the genes. in the cluster. 
write.csv(dge.cpm[clust1,], file = paste("E:/thesis/outhtseq_botrytis_merged/clust", clust, ".csv", sep=""))

