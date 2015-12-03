"""GFF parser

"""

from sys import argv
import os
import subprocess
def gff_change_chr_name(lines):
	print lines
	prefix = 'BCIN'
	for line in lines:
		if line.startswith("#"):
			continue
		else:
			print line
			line = line.split()
			print line
			chrom = str(line[0])
			chrom_new = prefix + chrom
			line_new = "%s\t%s"%(chrom_new, (line[1:]))
			#print line_new

def extract_UTR(lines, output_name):
	region_all = ""
	chrom_prev = ""
	output = open(output_name,'w')
	for line in lines:
		line = line.strip().split()
		if line[0].startswith('#'):
			continue
		elif 'UTR' in line[2]:
			
			chrom = line[0]
			start = line[3]
			end = line[4]
			region_f = "%s\t%s\t%s\n"%(chrom,start,end) # make right format
			output.write(region_f)
			region_all = region_all + region_f
			"""
			if chrom != chrom_prev and chrom_prev != "":
				print 'region_f', region_f
				output_name = file_name[:-4] + '_'+ chrom + '_UTR.fa'
				faidx(ref_genome, region_all, output_name)
				region_all = ""
			chrom_prev = chrom
			"""
	#return region_all

def getfasta(ref_genome, bed_file, output):
	""" Executing samtools faidx ### COPPIED OF REGIONS_EXTRACTION!!!
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
	file_name = argv[1]
	#ref_genome = argv[2] # S_lycopersicum_chromosomes.2.50.fa
	file_handler  = open(file_name)
	lines = file_handler.readlines()

	#output_bed_nm = file_name[:-4] + 'UTR.bed'
	#output_fa_nm = file_name[:-4] + 'UTR.fa'
	#extract_UTR(lines, output_bed_nm)
	#getfasta(ref_genome, output_bed_nm, output_fa_nm)
	#faidx(ref_genome, region, output_name)
	#while True():
	# OSError: Argument list too long.... 

	gff_change_chr_name(lines)