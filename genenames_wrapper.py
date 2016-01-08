from sys import argv
import os
import subprocess


if __name__ == "__main__":
	#path = '/mnt/scratch/baak009/bowtie/unique_tomato/clean_t_r/'
	path = os.getcwd()
	dirs = os.listdir(path)
	#terms = '/mnt/scratch/baak009/mRNA/ITAG2.4_gene_models.mRNA.gff3'
	terms = '/mnt/scratch/baak009/data/Botrytis_cinerea_GO_annotation_EBI_june2015.txt'
	for file_name in dirs:
		if file_name[-4:] == ".csv" and file_name[-8:] != 'gene.csv':
			print file_name
			print os.getcwd()
			cmd = ('python ~/gitrepos/botrytis/genenames.py %s %s'%(terms, file_name))
			print cmd
			e = subprocess.check_output(cmd, shell=True)
			print e

 #python ~/scripts/read_count.py Botrytis_genome_sizes.txt 50 /mnt/scratch/baak009/bowtie/unique_botrytis/clean_t_R/I12As_trimmed0.mapped0.un_mapped0_clean.bam
#python ~/gitrepos/botrytis/genenames.py ITAG2.4_gene_models.mRNA.gff3 sigIM0.052.csv