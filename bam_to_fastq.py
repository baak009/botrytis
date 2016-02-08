
from sys import argv
import os
import subprocess

def bam_to_fastq(bam_file):
	""" sam to  bam with samtools
	"""
	print "Converting sam to bam"
	fastq_fn = '%s.fastq'%(bam_file[:-4])
	cmd1 = 'bedtools bamtofastq -i %s -fq %s.fastq'%(bam_file, bam_file[:-4])
	

	if os.path.exists(bam_file) and os.path.exists('%s.fastq'% (bam_file[:-4])) == False:
			res1 = subprocess.check_call(cmd1, shell=True)
			print res1
			
			print 'fastqfile created: %s.fastq'%(bam_file[:-4])
	else:
		print 'file does not exist'
		print 'done'
	return fastq_fn

def bowtie_multimap(fastq_file):
	print "bowtie multimap"
	cmd1 = 'bowtie -p 4 -S -v 0 -a %s -q %s %s_a.sam 2> stats_%s_a.txt'%("S_lyn_2_50", 
		fastq_file, fastq_file[:-6], fastq_file[:-6])
	if os.path.exists(fastq_file) and os.path.exists('%s_a.sam'% (fastq_file[:-6])) == False:
			res1 = subprocess.check_call(cmd1, shell=True)
			print res1
			print 'sam created: %s.sam'%(fastq_file[:-6])
	else:
		print 'file does not exist'
		print 'done'

if __name__ == "__main__":
	#I16As_trimmed0.mapped0.un_mapped0_clean.sorted_f.bam 
	#path = "/mnt/scratch/baak009/hisat2/tomato/w_cuff"
	path = os.getcwd()
	dirs = os.listdir(path)
	counter = 1
	#file_name = "I12As_trimmed0.mapped0.un_mapped0_clean.sorted_f.mapped_a.sam"
	#file_name = argv[1]
	#sam_to_bam(file_name)
	#print dirs
	for file_name in dirs:
		print file_name[:5]
		if file_name[-12:] == "sorted_f.bam" and file_name[:5] != 'stats':
			print file_name
			fastq_fn = bam_to_fastq(file_name)
			bowtie_multimap(fastq_fn)


