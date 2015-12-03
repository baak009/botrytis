"""
extract sequence from reference genome, coordinates 
bam to sorted bam
Mirna Baak
last edit: 5-10-2015
"""
from sys import argv
import os
import subprocess
 

def regions(lines, expand):
	counter = 0
	region_all = ""
	for line in lines:
		line2 = line.strip().split(',') # split line
		if counter != 0:
			x = line2[0]
			x = x.split('=') # get part with genomic coordinates
			region = x[2]
			region_sep = region.split(':') # get chromosome name
			chrom = region_sep[0]
			coo  = region_sep[1].strip('"').split('..')# get start and end position
			print line
			start = int(coo[0])
			end = int(coo[1])
			if start < end:
				start = start - expand
				end = end + expand
			elif start > end:
				start = start + expand
				end = end - expand
			else:
				print "Error"
			region_f = "%s:%s-%s "%(chrom,start,end) # make right format
			region_all = region_all + region_f # add together to prepare for faidx

		counter += 1 # header will be skipped
	print region_all
	return region_all

def faidx(ref_genome, region, output_name):
	""" Executing samtools faidx
	"""
	print 'executing samtools faidx'
	if os.path.exists(ref_genome): #and os.path.exists(output_name) == False: 
		cmd = "samtools faidx %s %s > %s"%(ref_genome, region, output_name)
		res1 = subprocess.check_call(cmd,shell=True)
		print 'res1'
		print res1

if __name__ == "__main__":
	file_name = argv[1] # upreg10_all_f_18_3_2.csv
	ref_genome = argv[2] # NCBI_BcinB0510_revised11012015_2.fasta
	file_handler = open(file_name)
	lines = file_handler.readlines()
	expand = 100
	output_name = file_name[:-4] + '_' + str(expand) + '.fa'
	region_all = regions(lines, expand)
	faidx(ref_genome, region_all, output_name)
