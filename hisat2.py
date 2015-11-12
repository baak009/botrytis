"""
Script to run hisat2 build and hisat2
Output is a sam file of the alignment
author: Mirna Baak
Last updated: 6-11-2015
"""

from sys import argv
import os
import subprocess
	

def hisat2_build(fasta_file_name, ref_name):
	"""execute hisat2-build
	ref_name = name of referentie prefix
	fasta_file_name = file_name (including path) of reference genome
	"""
	#check if index is already build, if not build index of hisat2
	if os.path.exists('%s.1.ht2'%(ref_name)) == False:
		cmd = 'hisat2-build %s %s'%(fasta_file_name, ref_name)
		e = subprocess.check_call(cmd, shell=True)
		print e
	else: 
		print "hisat2-build index already exists"
	

def hisat2(splice_site_file_name, ref_name, path_fastq, fastq_file_name):
	"""execute hisat2 

	splice_site_file_name = name of file containg splice sites using 
	gtf file and extract_splice_sites.py
	ref_name = name of referentie prefix
	path_fastq = path of directory were fastq files are present
	fastq_file_name = name of fastq file

	"""
	# name of the created samfile
	output_name = file_name[:5] + '_hisat2.sam'
	print output_name
	# check if output already exists, if not execute hisat2 command
	if os.path.exists('%s'%(output_name)) == False:
		cmd = 'hisat2 --known-splicesite-infile %s --dta-cufflinks -x %s -U %s -S %s 2> stats_%s.txt'%(
			splice_site_file_name, 
			ref_name, path_fastq+fastq_file_name, output_name, file_name)
		e = subprocess.check_call(cmd, shell=True)
		print e
	else: 
		print "hisat2 output already exists"



if __name__ == "__main__":
	#path = os.getcwd()
	#path = "/mnt/scratch/baak009/bowtie/unique_botrytis/clean_t_R/"
	# path of directory where mRNA fastq files are located
	path_fastq = "/mnt/scratch/baak009/trimmed_adapt_reads/merged_mRNA/"
	# create a list of the files in the directory
	dirs = os.listdir(path_fastq)
	# splice site file created with extract_splice_sites.py
	splice_site_file_name = '/mnt/scratch/baak009/data/splice_sites_ITAG2.4.txt'
	#prefix of reference genome
	ref_name = 'S_lyc2.50'
	#reference genome
	fasta_file_name = '/mnt/scratch/baak009/data/S_lycopersicum_chromosomes.2.50.fa'

	#execute hisat2-build
	hisat2_build(fasta_file_name, ref_name)
	counter = 1
	# execute for all fastq files in directory hisat2
	file_name = 'M12Am.fastq' 
	hisat2(splice_site_file_name, ref_name, path_fastq, file_name)
	
	'''
	for file_name in dirs:
		if file_name[-6:] == ".fastq" and counter == 1:
			hisat2(splice_site_file_name, ref_name, path_fastq, file_name)

			#counter += 1
    '''

