"""
perform emboss einverted 

Mirna Baak
last edit: 7-12-2015
"""
from sys import argv
import os
import subprocess

def einverted(input_file, gap, threshold, match, mismatch, outfile, outseq):
	""" Executing emboss einverted
	"""
	print 'executing einverted'
	if os.path.exists(input_file) and os.path.exists(outfile) == False: #and os.path.exists(output_name) == False: 
		# -s option: force strandedness. If the feature occupies the antisense strand,
		#the sequence will be reverse complemented. 
		cmd = "einverted %s -gap %s -threshold %s -match %s -mismatch %s \
		-outfile %s -outseq %s"%(input_file, gap, threshold, match, mismatch, outfile, outseq)
		res1 = subprocess.check_call(cmd,shell=True)
		print 'res1'
		print res1
	else:
		print 'file problem'

def change_name_seq(file_name):
	output_name = file_name[:-3] + '_c.fa'
	if os.path.exists(file_name) and os.path.exists(output_name) == False:
		cmd = "sed 's/:/_/'< %s > %s"%(file_name, output_name)
		print cmd
		res1 = subprocess.check_call(cmd,shell=True)
		print res1
	else:
		print 'problem'
	return output_name
if __name__ == "__main__":
	#file_name = argv[1] # upreg10_all_f_18_3_2.csv
	#ref_genome = argv[2] # NCBI_BcinB0510_revised11012015_2.fasta
	path = os.getcwd()
	dirs = os.listdir(path)
	gap = 12
	threshold = 10
	match = 3
	mismatch = -4
	for file_name in dirs:
		#if file_name[-11:] == ".sorted.bam" and counter == 1:
		if file_name[-3:] == ".fa":
			
			file_name = change_name_seq(file_name)
			outfile = "%s_einverted.txt"%(file_name[:-3])
			outseq= "seq_%s_einverted.txt"%(file_name[:-3])
			print file_name 
			einverted(file_name,gap, threshold, match, mismatch, outfile, outseq)
