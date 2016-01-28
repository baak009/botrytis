"""GFF parser

"""

from sys import argv
import os
import subprocess
def gff_change_chr_name(file_name, lines): # only for botrytis
	output_nm  = "%s_new.gff3"%(file_name[:-5])
	output = open(output_nm, 'w')
	prefix = 'BCIN'
	for line in lines:
		if line.startswith("#"):
			#print line
			if len(line.strip()) == 3:
				continue
			else:
				output.write(line)
				#continue
		else:
			
			line = line.split('\t')
			
			chrom = str(line[0])
			#print len(chrom)
			if len(chrom) == 1:
				chrom_new = prefix + '0' + chrom
				#print chrom_new
			else:
				chrom_new = prefix + chrom
			line_new = "%s\t%s\t%s\n"%(chrom_new, ('\t'.join(line[1:-1])), line[-1])
			output.write(line_new)
			#print line_new
	output.close()


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
			descr = line[8]
			region_f = "%s\t%s\t%s\t%s\n"%(chrom,start,end, descr) # make right format
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

def extract_genes(lines, output_name):
	region_all = ""
	chrom_prev = ""
	output = open(output_name,'w')
	for line in lines:
		line = line.strip().split()
		if line[0].startswith('#'):
			continue
		elif 'gene' in line[2]:
			
			chrom = line[0]
			start = line[3]
			end = line[4]
			region_f = "%s\t%s\t%s\n"%(chrom,start,end) # make right format
			output.write(region_f)
			#region_all = region_all + region_f
			
	#return region_all
def extract_CDS(lines, output_name):
	region_all = ""
	chrom_prev = ""
	output = open(output_name,'w')
	for line in lines:
		line = line.strip().split()
		if line[0].startswith('#'):
			continue
		elif 'CDS' in line[2]:
			
			chrom = line[0]
			start = line[3]
			end = line[4]
			region_f = "%s\t%s\t%s\n"%(chrom,start,end) # make right format
			output.write(region_f)
			#region_all = region_all + region_f
			
	#return region_all

def extract_CDS_plus_region(lines, output_name):
	region_all = ""
	chrom_prev = ""
	output = open(output_name,'w')
	for line in lines:
		line = line.strip().split()
		if line[0].startswith('#'):
			continue
		elif 'CDS' in line[2]:
			
			chrom = line[0]
			start = int(line[3]) - count
			end = int(line[4]) - count
			region_f = "%s\t%s\t%s\n"%(chrom,start,end) # make right format
			output.write(region_f)
			#region_all = region_all + region_f
			
	#return region_all


def getfasta(ref_genome, bed_file, output):
	""" Executing bedtools getfasta with header name
	"""
	print 'executing bedtools getfasta'
	if os.path.exists(ref_genome): #and os.path.exists(output_name) == False: 
		# -s option: force strandedness. If the feature occupies the antisense strand,
		#the sequence will be reverse complemented. 
		cmd = "bedtools getfasta -s -name -fi %s -bed %s -fo %s"%(ref_genome, bed_file, output)
		res1 = subprocess.check_call(cmd,shell=True)
		print 'res1'
		print res1


def extract_gene__id_name(lines):
	for line in lines:
		line = line.strip().split()
		print line
		temp = line[-1]
		print temp
		temp = temp.split(';')
		print temp
		name = temp[0]
		id_name = temp[-1]
		print name, id_name

def extract_mRNA(lines, output_name):
        output = open(output_name,'w')
        for line in lines:
                line_temp = line.strip().split()
		if line_temp[0].startswith('#'):
			continue
		elif 'mRNA' in line_temp[2]:
			output.write(line)
			#region_all = region_all + region_f
                        
        output.close()
if __name__ == "__main__":
	file_name = argv[1]
	ref_genome = argv[2] # S_lycopersicum_chromosomes.2.50.fa
	file_handler  = open(file_name)
	lines = file_handler.readlines()

	output_bed_nm = file_name[:-4] + 'UTR_t.bed'
	#output_bed_nm = file_name[:-4] + 'gene.bed'
	output_fa_nm = file_name[:-4] + 'UTR_t.fa'
	#output_cds_nm = file_name[:-4] + 'CDS.bed'
	#output_mRNA_nm = file_name[:-4] + 'mRNA.gff3'
	extract_UTR(lines, output_bed_nm)
	#extract_genes(lines, output_bed_nm)
	#extract_CDS(lines, output_cds_nm)
	#extract_mRNA(lines, output_mRNA_nm)
	getfasta(ref_genome, output_bed_nm, output_fa_nm)
	#faidx(ref_genome, region, output_name)
	#while True():
	# OSError: Argument list too long.... 

	#gff_change_chr_name(file_name, lines)
	#extract_gene__id_name(lines)
