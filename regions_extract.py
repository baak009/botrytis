"""
extract sequence from reference genome, coordinates 

Mirna Baak
last edit: 7-12-2015
"""
from sys import argv
import os
import subprocess
 

def regions(lines, expand, output_bed_nm):
	output = open(output_bed_nm,'w')
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
			#print line
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
			region_p = "%s:%s-%s "%(chrom,start,end) # make right format
			region_f = "%s\t%s\t%s\n"%(chrom,start,end)
			#region_all = region_all + region_p # add together to prepare for faidx
			output.write(region_f)

		counter += 1 # header will be skipped
	output.close()
	#print region_all
	#return region_all

def getfasta(ref_genome, bed_file, output):
	""" Executing bedtools getfasta ### COPPIED REGIONS_EXTRACTION!!!
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
	#file_name = argv[1] # upreg10_all_f_18_3_2.csv
	#ref_genome = argv[2] # NCBI_BcinB0510_revised11012015_2.fasta


	#file_handler = open(file_name)
	#lines = file_handler.readlines()
	#expand = 100
	#output_name = file_name[:-4] + '_' + str(expand) + '.fa'
	#output_bed_nm = file_name[:-4] + '_' + str(expand) + '.bed'
	#regions(lines, expand, output_bed_nm)
	
	#getfasta(ref_genome, output_bed_nm, output_name)
	ref_genome = argv[1] # NCBI_BcinB0510_revised11012015_2.fasta
	path = os.getcwd()
	#path of directory with bam files
	#path = "/mnt/scratch/baak009/bowtie/unique_tomato/clean_t_r/"
	dirs = os.listdir(path)
	for file_name in dirs:
		#if file_name[-11:] == ".sorted.bam" and counter == 1:
		if file_name[-4:] == ".csv":
			file_handler = open(file_name)
			lines = file_handler.readlines()
			expand = 200 #100
			output_name = file_name[:-4] + '_' + str(expand) + '.fa'
			output_bed_nm = file_name[:-4] + '_' + str(expand) + '.bed'
			regions(lines, expand, output_bed_nm)
			getfasta(ref_genome, output_bed_nm, output_name)
