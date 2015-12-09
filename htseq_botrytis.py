#samtools

"""Htseq

Author: Mirna Baak
Last editted: 23-11-2015
"""
#import modules
from sys import argv
import os
import subprocess

def htseq(path, sam_file, path2, gff_file, id_attribute):
	""" hstseq 
	"""
	print "HtSeq"
	cmd1 = 'python -m HTSeq.scripts.count -i %s %s %s  > %s_counts.txt'%( id_attribute, 
		path+sam_file, 
		path2+gff_file, sam_file[:-4])
	print cmd1

	if os.path.exists(path+sam_file) and \
		os.path.exists('%s_counts.txt'%(sam_file[:-4])) == False:
		res1 = subprocess.check_call(cmd1, shell=True)
		print res1
		print 'htseq file created: %s_counts.txt'%(sam_file[:-4])
		
	else:
		print 'file does not exist'
	
	print 'done'


if __name__ == "__main__":

	path = "/mnt/scratch/baak009/hisat2/botrytis/"
	dirs = os.listdir(path)
	path2 = "/mnt/scratch/baak009/data/"
	gff_file = "BcinB0510_finalannotations_January2015B.michael.gtf"
	counter = 1
	id_attribute = 'gene_name'
	for file_name in dirs:
		if file_name[-4:] == ".sam" and counter == 1:
			htseq(path, file_name, path2, gff_file, id_attribute)
			#counter += 1
