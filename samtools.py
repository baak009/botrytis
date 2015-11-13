#samtools

"""samtools view, sort and index
Sam to bam, sorted bam and bai

Author: Mirna Baak
Last editted: 9-11-2015
"""
#import modules
from sys import argv
import os
import subprocess

def sam_to_bam(sam_file):
	""" sam to  bam with samtools
	"""
	print "Converting sam to bam"
	cmd1 = 'samtools view -b -S %s > %s.bam'%(sam_file, sam_file[:-4])
	print cmd1
	cmd2 = 'samtools sort %s.bam %s.sorted'%(sam_file[:-4], sam_file[:-4])
	print cmd2
	cmd3 = 'samtools index %s.sorted.bam'%(sam_file[:-4])
	print cmd3

	if os.path.exists(sam_file) and os.path.exists('%s.bam'% (sam_file[:-4])) == False:
			res1 = subprocess.check_call(cmd1, shell=True)
			print res1
			res2 = subprocess.check_call(cmd2, shell=True)
			print res2
			res3 = subprocess.check_call(cmd3, shell=True)
			print res3
			print 'bam file created: %s.bam'%(sam_file[:-4])
	else:
		print 'file does not exist'
		print 'done'


if __name__ == "__main__":

	#path = "/mnt/scratch/baak009/hisat2/tomato/w_cuff"
	path = os.getcwd()
	dirs = os.listdir(path)
	counter = 1

	for file_name in dirs:
		if file_name[-4:] == ".sam" and counter == 1:
			sam_to_bam(file_name)


