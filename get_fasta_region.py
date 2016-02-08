"""Get fasta sequence of region defined in bed file
by: Mirna Baak
last updated:feb 1 2016
"""
from sys import argv
import os
import subprocess

def getfasta(ref_genome, bed_file, output):
	""" Executing bedtools getfasta,
	uses a bedfile with coordinates and a reference genome bed_file
	to create a fasta file with header coordinates followed by sequence.
	"""
	print 'executing bedtools getfasta'
	if os.path.exists(ref_genome): #and os.path.exists(output_name) == False: 
		# -s option: force strandedness. If the feature occupies the antisense strand,
		#the sequence will be reverse complemented. 
		cmd = "bedtools getfasta -s -fi %s -bed %s -fo %s"%(ref_genome, bed_file, output)
		res1 = subprocess.check_call(cmd,shell=True)
		print 'res1'
		print res1


def filteroption(fasta_file):
	"""Filters the sRNAs, based on sequence identity
	So when the same sequence is found, only the first one is kept.
	"""
	print 'filter op unique sequences'
	#open file
	file_handler = open(fasta_file)
	lines = file_handler.readlines()
	output = open("%s_filtered.fa"%fasta_file[:-3], 'w')
	list_sequences = [] # list with sequences
	list_header = [] # list with headers of sequences
	#loop through lines
	for line in lines:
		# save headers in temp
		if line.startswith('>'):
			temp = line.strip()
		#check if sequence already exist, if not write to output
		else:
			line_s = line.strip()
			if line_s not in list_sequences:
				output.write("%s\n%s\n"%(temp, line_s))
				list_sequences.append(line_s)
				list_header.append(temp)
				temp = ""

	output.close()

if __name__ == "__main__":
	ref_genome = argv[1] # NCBI_BcinB0510_revised11012015_2.fasta
	bed_f_nm= argv[2] # out_merged_all_f_I_pileup_extractor.annotated.bed
	output_nm = argv[3]
	getfasta(ref_genome, bed_f_nm, output_nm)
	filteroption(output_nm)