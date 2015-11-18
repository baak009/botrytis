"""Bowtie mapping script
Mirna Baak
last edited: 14-10-2015
includes function bowtie -a (multimapping)
"""
import os
import subprocess
from sys import argv

def bowtie_build(file_name, ref_name):
	if os.path.exists('%s.1.ebwt'%(ref_name)) == False:
		cmd = 'bowtie-build %s %s'%(file_name, ref_name)
		e = subprocess.check_call(cmd, shell=True)
		print e
	else: 
		print "index is already build"

def bowtie(num_mismatch, file_name_fastq):
	print "Executing bowtie with %s mismatches"%(num_mismatch)
	file_name_fastq2 =  file_name_fastq.split('/')
	print '1', file_name_fastq2[-1]
	print '1.5', num_mismatch
	output_sam = file_name_fastq2[-1][:-6]+str(num_mismatch) + 'a.sam'
	print '2', output_sam
	if os.path.exists(file_name_fastq) and os.path.exists(output_sam) == False:
		#output_sam = file_name_fastq2[-1]+str(num_mismatch) + '.sam'
		print '3', output_sam
		cmd = 'bowtie -S -v %s -a %s %s %s 2> stats_%s_%s_a.txt'%(num_mismatch, ref_name, 
			file_name_fastq, output_sam, file_name_fastq2[-1], num_mismatch)
		res1 = subprocess.check_call(cmd, shell=True)
		print res1
	
	else:
		print 'file does not exist'
	return output_sam

def sam_to_bam(sam_file):
	""" sam to  bam with samtools
	"""
	print "Converting sam to bam"
	#view -b -S I12As_S23_R1_001_trimmed0.sam > I12As_S23_R1_001_trimmed0.bam
	cmd1 = 'samtools view -b -S %s > %s.bam'%(sam_file, sam_file[:-4])
	print cmd1
	#cmd2 = 'samtools sort %s.bam %s.sorted'%(sam_file[:-4], sam_file[:-4])
	#print cmd2
	#cmd3 = 'samtools index %s.sorted.bam'%(sam_file[:-4])
	#print cmd3

	
	if os.path.exists(sam_file):
		res1 = subprocess.check_call(cmd1, shell=True)
		print res1
		#res2 = subprocess.check_call(cmd2, shell=True)
		#print res2
		#res3 = subprocess.check_call(cmd3, shell=True)
		#print res3
	else:
		print 'file does not exist'
	print 'bam file created: %s.bam'%(sam_file[:-4])
	print 'done'




if __name__ == "__main__":
	#path = "/mnt/scratch/baak009/data/"
	file_name = argv[1] #"NCBI_BcinB0510_revised11012015_2.fasta"
	#file_name = "S_lycopersicum_chromosomes.2.50.fa"
	ref_name = argv[2] # "B_cinB0510"
	#ref_name = "S_lyn_2_50"
	#bowtie_build(file_name, ref_name)
	#path2 = "/mnt/scratch/baak009/trimmed_adapt_reads/"
	

	
	file_name_fastq = argv[3] #"I12As_S23_R1_001_trimmed.fastq"
	#file_name_fastq = "B16Bs_S19_h400.fastq"


	num_mismatch = argv[-1] #0
	print '4', num_mismatch
	#running bowtie
	output_sam = bowtie(num_mismatch,file_name_fastq)
	#output_sam = 'I12As_S23_R1_001_trimmed0.sam' 
	#sam_to_bam(output_sam)