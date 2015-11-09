"""
bedtools intersect

bam to sorted bam
Mirna Baak
last edit: 5-10-2015
"""
from sys import argv
import os
import subprocess

def bedtools_intersect(file_A, file_B, file_C, output_name, path):
	""" Executing bedtools intersect 

	"""
	print 'executing bedtools intersect'
	if os.path.exists(file_A) and os.path.exists(file_B) and os.path.exists(output_name) == False: 
		cmd = "bedtools intersect -a %s -b %s %s -v > %s"%(file_A, file_B, file_C, output_name)
		res1 = subprocess.check_call(cmd,shell=True)
		print 'res1'
		print res1
    

def bam_to_bai(output_name):
	print 'from bam to bai in a second'
	print output_name
	if os.path.exists(output_name) and os.path.exists("%s.sorted.bam"%(output_name[:-4])) == False:
		cmd1 = "samtools sort %s %s.sorted"%(output_name, output_name[:-4])
		cmd2 = "samtools index %s.sorted.bam"%(output_name[:-4])
		res2 = subprocess.check_call(cmd1, shell = True)
		print 'res2', res2
		res3 = subprocess.check_call(cmd2, shell = True)
		print 'res3', res3


if __name__ == "__main__":
	path = os.getcwd()

	file_name_A =  argv[1]#".bam"
	file_name_B =  argv[2]#"trnas_Botrytis_default.bed"
	file_name_C =  argv[3]#"rrnas.bam"
	output_name =  argv[4]#".bam"
	bedtools_intersect(file_name_A, file_name_B, file_name_C, output_name, path)
	bam_to_bai(output_name)