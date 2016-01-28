"""Get fasta sequence of region defined in bed file
by: Mirna Baak
last updated:jan 22 2016
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


if __name__ == "__main__":
	ref_genome = argv[1] # NCBI_BcinB0510_revised11012015_2.fasta
	bed_f_nm= argv[2] # out_merged_all_f_I_pileup_extractor.annotated.bed
	output_nm = argv[3]
	getfasta(ref_genome, bed_f_nm, output_nm)