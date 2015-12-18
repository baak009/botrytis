"""
size_selection of bam 
BBmap and samtools required 
Author: Mirna Baak
Last editted: 7-12-2015
"""
#import modules
from sys import argv
import os
import subprocess

def size_selection(input_nm, minlength, maxlength):
	""" size selection with bbmap reformat
	"""
	print "size selection"
	output_nm = '%s_f.bam'%(input_nm[:-4])
	cmd1 = 'reformat.sh in=%s out=%s minlength=%s maxlength=%s 2>stats_%s'%(
		input_nm, output_nm, minlength, maxlength,output_nm)



	if os.path.exists(input_nm) and os.path.exists(output_nm) == False:
			res1 = subprocess.check_call(cmd1, shell=True)
			print res1
			
			print 'bam file created: %s'%(output_nm)
	else:
		print 'file does not exist'
	print 'done'


if __name__ == "__main__":

	path = os.getcwd()
	dirs = os.listdir(path)
	counter = 1
	minlength = 16
	maxlength = 30
	for file_name in dirs:
		if file_name[-10:] == "sorted.bam" and counter == 1:
			size_selection(file_name, minlength, maxlength)
			#counter += 1

