"""Overall mapping script
"""
from sys import argv
import os
import subprocess
def make_directory(directory):
	if os.path.exists('/mnt/scratch/baak009/%s'%(directory)) == False:
		os.system('mkdir /mnt/scratch/baak009/%s'%(directory))
		print 'directory %s created'%(directory)
	else:
		print 'directory already exists'
	
def run_bowtie(directory, path, file_name, genome, genome_name, num_mismatch):
	print 'run bowtie'
	cmd = ('cd %s; python ~/scripts/bowtiescript2.py %s %s %s %s'%
		(directory, genome, genome_name, path+file_name, num_mismatch))

	e = subprocess.check_output(cmd, shell=True)
	print e

def run_bedtools_intersect(directory, path, file_name, trna_file, rrna_file):
	print 'run bedtools intersect'
	cmd = ('cd %s; python ~/scripts/bedtools_intersect.py %s %s %s %s_clean_t_rRNA.bam'%\
			(directory,(path+file_name), trna_file, rrna_file, file_name[:-4]))
	e = subprocess.check_output(cmd, shell=True)
	print e

def run_bam_to_fastq(directory, path, file_name ):
	print 'run bam to fastq'
	print '1', directory
	cmd = ('cd %s; python ~/scripts/bam_to_fastq2.py %s %s'%\
		(directory, path, file_name))
	#cmd = 'cd %s; echo "hoi" > test.txt'%(directory)
	e = subprocess.check_output(cmd, shell=True)
	print e

def run_unmapped_bam_to_fastq(directory, path, file_name ):
	print 'run bam to fastq'
	print '1', directory
	cmd = ('cd %s; python ~/scripts/bam_to_fastq_unmapped2.py %s %s'%\
		(directory, path, file_name))
	#cmd = 'cd %s; echo "hoi" > test.txt'%(directory)
	e = subprocess.check_output(cmd, shell=True)
	print e
		
if __name__ == "__main__":
	# first mapping against botrytis and tomato
	path = '/mnt/scratch/baak009/trimmed_adapt_reads/merged/'
	dirs = os.listdir(path)
	genome_botrytis = '/mnt/scratch/baak009/data/NCBI_BcinB0510_revised11012015_2.fasta'
	genome_name_botrytis = 'B_cinB0510'
	num_mismatch_botrytis = 0

	genome_tomato = '/mnt/scratch/baak009/data/S_lycopersicum_chromosomes.2.50.fa'
	genome_name_tomato = 'S_lyn_2_50'
	num_mismatch_tomato = 0
	'''
	x = 0
	for file_name in dirs:
		if file_name[-6:] == ".fastq" and x == 0:
			print file_name
			print os.getcwd()
			directory = 'test_mapped_botrytis'
			make_directory(directory)
			#genome_botrytis = '/mnt/scratch/baak009/data/NCBI_BcinB0510_revised11012015_2.fasta'
			#genome_name_botrytis = 'B_cinB0510'
			#num_mismatch_botrytis = 0
			run_bowtie(directory, path, file_name, genome_botrytis, genome_name_botrytis, num_mismatch_botrytis)

			directory = 'test_mapped_tomato'
			make_directory(directory)
			#genome_tomato = '/mnt/scratch/baak009/data/S_lycopersicum_chromosomes.2.50.fa'
			#genome_name_tomato = 'S_lyn_2_50'
			#num_mismatch_tomato = 0
			run_bowtie(directory, path, file_name, genome_tomato, genome_name_tomato, num_mismatch_tomato)

		x += 1

	
	# removing tRNA and rRNA from samples 
	path = '/mnt/scratch/baak009/test_mapped_botrytis/'
	dirs = os.listdir(path)
	x = 0
	directory = 'test_clean_t_rRNA_botrytis'
	make_directory(directory)
	trna_file_botrytis = '/mnt/scratch/baak009/tRNA/trnas_Botrytis_default.bed'
	rrna_file_botrytis = '/mnt/scratch/baak009/rRNA/botrytis_rRNA_chr4_9kb.bed'
	for file_name in dirs:
		if file_name[-4:] == ".bam":
			print file_name
			run_bedtools_intersect(directory, path, file_name, trna_file_botrytis, rrna_file_botrytis)

		#path = '/mnt/scratch/baak009/test_mapped_botrytis/'
	#dirs = os.listdir(path)
	x = 0

	path = '/mnt/scratch/baak009/test_mapped_tomato/'
	dirs = os.listdir(path)
	directory = 'test_clean_t_rRNA_tomato'
	make_directory(directory)
	trna_file_tomato = '/mnt/scratch/baak009/tRNA/trnas2_tomato_default.bed'
	rrna_file_tomato = '/mnt/scratch/baak009/rRNA/solanum_rrna.bam'
	for file_name in dirs:
		if file_name[-4:] == ".bam":
			print file_name
			run_bedtools_intersect(directory, path, file_name, trna_file_tomato, rrna_file_tomato)
			
	
	#bam to fastq botrytis
	path = '/mnt/scratch/baak009/test_clean_t_rRNA_botrytis/'
	dirs = os.listdir(path)
	directory = 'test_mapped_fastq_botrytis'
	make_directory(directory)
	for file_name in dirs:
		if file_name[-4:] == ".bam":
			print file_name
			run_bam_to_fastq(directory, path, file_name)

	#bam to fastq tomato
	path = '/mnt/scratch/baak009/test_clean_t_rRNA_tomato/'
	dirs = os.listdir(path)
	directory = 'test_mapped_fastq_tomato'
	make_directory(directory)
	for file_name in dirs:
		if file_name[-4:] == ".bam":
			print file_name
			run_bam_to_fastq(directory, path, file_name)
	'''		
	# botrytis to tomato genome
	path = '/mnt/scratch/baak009/test_mapped_fastq_botrytis/'
	dirs = os.listdir(path)
	directory = 'test_mapped_botrytis_tomato'
	make_directory(directory)
	for file_name in dirs:
		if file_name[-6:] == ".fastq":
			print file_name
			run_bowtie(directory, path, file_name, genome_tomato, genome_name_tomato, num_mismatch_tomato)

	# tomato to botrytis genome
	path = '/mnt/scratch/baak009/test_mapped_fastq_tomato/'
	dirs = os.listdir(path)
	directory = 'test_mapped_tomato_botrytis'
	make_directory(directory)
	for file_name in dirs:
		if file_name[-6:] == ".fastq":
			print file_name
			run_bowtie(directory, path, file_name, genome_botrytis, genome_name_botrytis, num_mismatch_botrytis)

	#bam to fastq to get unique tomato
	path = '/mnt/scratch/baak009/test_mapped_tomato_botrytis/'
	dirs = os.listdir(path)
	directory = 'test_unique_tomato'
	make_directory(directory)
	for file_name in dirs:
		if file_name[-4:] == ".bam":
			print file_name
			run_unmapped_bam_to_fastq(directory, path, file_name)

	#bam to fastq to get unique botrytis
	path = '/mnt/scratch/baak009/test_mapped_botrytis_tomato/'
	dirs = os.listdir(path)
	directory = 'test_unique_botrytis'
	make_directory(directory)
	for file_name in dirs:
		if file_name[-4:] == ".bam":
			print file_name
			run_unmapped_bam_to_fastq(directory, path, file_name)

	#bam to fastq to get overlapped reads
	path = '/mnt/scratch/baak009/test_mapped_botrytis_tomato/'
	dirs = os.listdir(path)
	directory = 'test_overlap'
	make_directory(directory)
	for file_name in dirs:
		if file_name[-4:] == ".bam":
			print file_name
			run_bam_to_fastq(directory, path, file_name)

