library("DESeq")

data <- read.delim("E:/thesis/all_f_18_3_2.txt", header = FALSE)

total_counts_unique_botrytis <- data[,10:ncol(data)]
total_counts_unique_botrytis <- data[,10:17]

colnames(total_counts_unique_botrytis) = c("B16A", "B16B", "I12A", "I12B", "I16A", "I16B", "I24B", "I24D",
                                           "AF12", "AF16", "AF24", "M12", "M16", "M24")

rownames(total_counts_unique_botrytis) = data[,9]


head(total_counts_unique_botrytis)

#GEEN IDEE OF DIT WEL KLOPT Want zit hier nu bij geteld dat de ene conditie veel meer reads waren?
# normalizeren!
test = total_counts_unique_botrytis[total_counts_unique_botrytis$I12A > 10 & total_counts_unique_botrytis$B16A < 100, ]
sum(is.na(data))
sum(is.na(res))
sum(is.na(counts(cds,normalized = TRUE)))


coln <- colnames(total_counts_unique_botrytis)
sum_col <- colSums(total_counts_unique_botrytis[,])
sum_col <- c(4065306, 2041463, 24723, 34984, 30738, 26763, 47030, 68489, 27218, 25293, 17721, 1250, 1135, 868) #unique botrytis filtered on length 16-30, mastersheet 



colSums(total_counts_unique_botrytis)
for (i in 1:length(coln)){
  total_counts_unique_botrytis[,paste0(coln[i],"_norm")] <- 
    total_counts_unique_botrytis[,i]/sum_col[i] * 1000000
} 
normalized_total_counts_unique_botrytis<- total_counts_unique_botrytis[,c(15:28)]

expressed_I24 <- normalized_total_counts_unique_botrytis[(normalized_total_counts_unique_botrytis$I24B_norm > 0) &
                                                           (normalized_total_counts_unique_botrytis$I24D_norm > 0),]

expressed2_I24 <- normalized_total_counts_unique_botrytis[(normalized_total_counts_unique_botrytis$I24B_norm > 
                                                             normalized_total_counts_unique_botrytis$B16A_norm) &
                                                           (normalized_total_counts_unique_botrytis$I24D_norm > 
                                                              normalized_total_counts_unique_botrytis$B16A_norm) &
                                                            (normalized_total_counts_unique_botrytis$I24B_norm > 
                                                               normalized_total_counts_unique_botrytis$B16B_norm) &
                                                            (normalized_total_counts_unique_botrytis$I24D_norm >
                                                            normalized_total_counts_unique_botrytis$B16B_norm),]
expressed_I16_I24 <- 
  normalized_total_counts_unique_botrytis[(normalized_total_counts_unique_botrytis$I24B_norm > 
                                             normalized_total_counts_unique_botrytis$B16A_norm) &
                                            (normalized_total_counts_unique_botrytis$I24D_norm > 
                                               normalized_total_counts_unique_botrytis$B16A_norm) &
                                            (normalized_total_counts_unique_botrytis$I24B_norm > 
                                               normalized_total_counts_unique_botrytis$B16B_norm) &
                                            (normalized_total_counts_unique_botrytis$I24D_norm >
                                               normalized_total_counts_unique_botrytis$B16B_norm),]

#volgens mij komt hier wel wat leuks uit:
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

upreg10 <-high.expr[high.expr$I24B_norm > 10*high.expr$B16A_norm &(
  high.expr$I24B_norm > 10*high.expr$B16B_norm) & (
    high.expr$I24D_norm > 10*high.expr$B16A_norm) & (
      high.expr$I24D_norm > 10*high.expr$B16B_norm) & (
        high.expr$I12A_norm > 10*high.expr$B16B_norm) & (
          high.expr$I12A_norm > 10*high.expr$B16A_norm) & (
            high.expr$I12B_norm > 10*high.expr$B16B_norm) & (
              high.expr$I12B_norm > 10*high.expr$B16A_norm) & (
                high.expr$I16A_norm > 10*high.expr$B16B_norm) & (
                  high.expr$I16A_norm > 10*high.expr$B16A_norm) & (
                    high.expr$I16B_norm > 10*high.expr$B16B_norm) & (
                      high.expr$I16B_norm > 10*high.expr$B16A_norm)
  
  
  ,]

write.csv(upreg10, file = 'E:/thesis/upreg10_all_f_18_3_2.csv')
