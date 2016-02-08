#Plot R script tomato genes
args <-commandArgs(trailingOnly = TRUE) 
file_name = args[1] # file name
mean.counts <- read.csv(file_name, row.names = 1, header = T)
p = args[2] # gene name
png(paste(p,'rplot_1.png', sep=""))
#p = 'gene:Solyc00g005000.2'

ttest = t(mean.counts[(paste('gene:', p, sep= "")),])
plot(ttest[,1], xaxt = 'n', pch=19, col = 'red', main = colnames(ttest), xlab = 'sample', ylab = 'normalized readcount')
axis(1,seq(1,length(rownames(ttest))),rownames(ttest))
invisible(dev.off())