"""siRNA

Author: Mirna Baak
Last editted: 19-11-2015
"""
#import modules
from sys import argv
import os
import subprocess

def length_filtering(input_nm, min_length = 18, max_length = 25):
	""" length filtering 
	"""
	output_nm = '%s_filtered_l.fasta'%(input_nm[:-6])
	
	if os.path.exists(output_nm) == False:
		output = open(output_nm, 'w')
		file_handler = open(input_nm)
		lines = file_handler.readlines()
		for line in lines:
			line = line.strip()
			if line.startswith('>'):
				header = line
			else:
				if len(line) >= min_length and len(line) <= max_length:
					seq = line
					output.write('%s\n%s\n'%(header,seq))
	return output_nm


	
def unique_reads(input_nm):
	print 'unique reads'
	output_nm = '%s_unique.fasta'%(input_nm[:-6])
	cmd1 = 'fastx_collapser -i %s -o %s'%(input_nm, output_nm) # only on meyers
	print cmd1
	if os.path.exists(input_nm) and os.path.exists(output_nm) == False:
			res1 = subprocess.check_call(cmd1, shell=True)
			print res1
			
			print 'file created: %s'%(output_nm)
	else:
		print 'file does not exist'
	print 'done'
	return output_nm

def bowtie_build(file_name, ref_name):
	if os.path.exists('%s.1.ebwt'%(ref_name)) == False:
		cmd = 'bowtie-build %s %s'%(file_name, ref_name)
		e = subprocess.check_call(cmd, shell=True)
		print e
	else: 
		print "index is already build"

def bowtie(num_mismatch, file_name_fastq, ref_name):
	print "Executing bowtie with %s mismatches"%(num_mismatch)
	file_name_fastq2 =  file_name_fastq.split('/')
	print '1', file_name_fastq2[-1]
	print '1.5', num_mismatch
	output_sam = file_name_fastq2[-1][:-6]+str(num_mismatch) + 'a.sam'
	print '2', output_sam
	if os.path.exists(file_name_fastq) and os.path.exists(output_sam) == False:
		#output_sam = file_name_fastq2[-1]+str(num_mismatch) + '.sam'
		print '3', output_sam
		cmd = 'bowtie -S -v %s -a %s -f %s %s 2> stats_%s_%s_a.txt'%(num_mismatch, ref_name, 
			file_name_fastq, output_sam, file_name_fastq2[-1], num_mismatch)
		res1 = subprocess.check_call(cmd, shell=True)
		print res1
	
	else:
		print 'file does not exist'
	return output_sam

def samtools_to_bam(sam_file):
	print 'samtools to bam'
	output_nm = '%s.bam'% (sam_file[:-4])
	cmd1 = 'samtools view -b -S %s > %s.bam'%(sam_file, sam_file[:-4])
	if os.path.exists(sam_file) and os.path.exists(output_nm) == False:
			res1 = subprocess.check_call(cmd1, shell=True)
			print res1
	else:
		print 'file does not exist'
		print 'done'
	return output_nm


def bamtofastq(file_name_bam):
	print 'bam to fastq'
	output_nm = '%s.fastq'%(file_name_bam[:-4])
	if os.path.exists(file_name_bam) and os.path.exists(output_nm) == False:
		cmd2 = 'bedtools bamtofastq -i %s -fq %s'%(file_name_bam,output_nm)
		e = subprocess.check_output(cmd2, shell=True)
		print e
	return output_nm

def filter_mapped_times(input_nm, max_mapping = 20):
	print 'filter mapped times'
	output_nm = '%s_filtered_%s.fasta'%(input_nm[:-6], max_mapping)
	header_true = 0
	if os.path.exists(output_nm) == False:
		output = open(output_nm, 'w')
		file_handler = open(input_nm)
		lines = file_handler.readlines()
		for line in lines:
			line = line.strip()
			if line.startswith('>'):
				header = line
				temp = header.split('-')
				
				if int(temp[1]) < max_mapping:
					header_true = 1
			else:
				if header_true == 1:
					seq = line
					output.write('%s\n%s\n'%(header,seq))
			
	return output_nm

if __name__ == "__main__":
	# get first only the mapped reads. with the bam to fastq script
	# map the reads back on botrytis (bowtiescript2.py)and filter for tRNA and rRNA (bedtools intersect)
	# get fastq sequences back bam to fastq
	# select unique reads
	# length filtering
	# 
	
	path = os.getcwd()
	dirs = os.listdir(path)
	counter = 1
	print dirs
	fasta_genome_name = 'NCBI_BcinB0510_revised11012015_2.fasta'
	ref_name = "B_cinB0510"
	bowtie_build(fasta_genome_name, ref_name)
	num_mismatch = 0
	for file_name in dirs:
		#print file_name
		if file_name[-11:] == 'clean.fastq':
			print 'ja'
			output_nm = unique_reads(file_name)
			file_name3 = length_filtering(output_nm)

			fasta_genome_name = 'NCBI_BcinB0510_revised11012015_2.fasta'
			ref_name = "B_cinB0510"

			output_sam = bowtie(num_mismatch,file_name3, ref_name)
			output_bam = samtools_to_bam(output_sam)
			output_fastq = bamtofastq(output_bam)
			output_unique = unique_reads(output_fastq) # how many times a read maps to botrytis genome.
			output_filtmap = filter_mapped_times(output_unique)

			fasta_genome_name = "S_lycopersicum_chromosomes.2.50.fa"
			ref_name = "S_lyn_2_50"

			output_final = bowtie(num_mismatch, output_filtmap, ref_name)
			output_final_bam = samtools_to_bam(output_final)

	


			
		counter += 1

	
	
