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
	count = 500
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
			end = int(line[4]) + count
			descr = line[8]
			region_f = "%s\t%s\t%s\t%s\n"%(chrom,start,end, descr) # make right format
			output.write(region_f)
			#region_all = region_all + region_f
			
	#return region_all
def extract_UTRs_plus(lines, output_name):
	count = 500
	region_all = ""
	chrom_prev = ""
	output = open(output_name,'w')
	gene = None
	counter = 0
	count_five = 0
	count_three = 0
	for line in lines:
		line = line.strip().split()
		#print line
		if line[0].startswith('#'):
			continue
		# needed for the bcin gff file due to fasta sequences at the end
		if line[0].startswith('>'):
			continue
		if line[0].startswith('T'):
			continue
		if line[0].startswith('A'):
			continue
		if line[0].startswith('G'):
			continue
		if line[0].startswith('C'):
			continue
		elif 'gene' in line[2]: # extract UTRs if not 
			#gene = line
			if counter >= 3 and count_five > 0 and count_three > 0:
				gene = line
				counter = 1
				count_three =0
				count_five = 0
			elif (count_five < 1 and gene != None) or (count_three < 1 and gene != None):
				# if one of the UTRS are not available
				chrom = gene[0]
				if count_five == 0:
					if gene[6] == '+':
						#5primeUTR
						start = int(gene[3])-count
						if start < 0:
							start = 0
						end = int(gene[3]) # the start position of the gene
						
					else: 
						start = int(gene[4])
						if start < 0:
							start = 0
						end = int(gene[4]) + count
					descr = "ID=five_prime_UTR_s;" + str(gene[8])
					region_f = "%s\t%s\t%s\t%s\t.\t%s\n"%(chrom,start,end, descr, gene[6]) # make right format
					output.write(region_f)
					count_five = 0

				if count_three == 0:
					if gene[6] == '+':
						start = int(gene[4]) # end position of the gene
						end = int(gene[4]) + count # end position of the gene
					else:
						start = int(gene[3]) - count
						end = int(gene[3]) + count
					descr = "ID=three_prime_UTR_s;" + str(gene[8])
					region_f = "%s\t%s\t%s\t%s\t.\t%s\n"%(chrom,start,end, descr, gene[6]) # make right format
					output.write(region_f)
					count_three = 0

				gene = line
				counter = 1

			if gene == None:
				gene = line
				counter = 1
		#if UTR is defined
		elif 'UTR' in line[2] and (int(line[4]) - int(line[3])) != 0:
			if 'five' in line[2]:
				count_five += 1
			else: 
				count_three += 1
			chrom = line[0]
			start = int(line[3])
			end = int(line[4])
			descr = line[8]
			region_f = "%s\t%s\t%s\t%s\t.\t%s\n"%(chrom,start,end, descr, line[6]) # make right format
			output.write(region_f)
			counter += 1

	#for the last gene
	if (count_five < 1 and gene != None) or (count_three < 1 and gene != None):
		chrom = gene[0]
		if count_five == 0:
			if gene[6] == '+':
				#5primeUTR
				start = int(gene[3])-count
				end = int(gene[3]) # the start position of the gene
			
			else: 
				start = int(gene[4])
				end = int(gene[4]) + count
				descr = "ID=five_prime_UTR_s;" + str(gene[8])
				region_f = "%s\t%s\t%s\t%s\t.\t%s\n"%(chrom,start,end, descr, gene[6]) # make right format
				output.write(region_f)
				count_five = 0

			if count_three == 0:
				if gene[6] == '+':
					start = int(gene[4]) # end position of the gene
					end = int(gene[4]) + count # end position of the gene
				else:
					start = int(gene[3]) - count
					end = int(gene[3]) + count
				descr = "ID=three_prime_UTR_s;" + str(gene[8])
				region_f = "%s\t%s\t%s\t%s\t.\t%s\n"%(chrom,start,end, descr, gene[6]) # make right format
				output.write(region_f)
				count_three = 0
			gene = line
			counter = 1

	print 'UTRplus'		
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
	file_name = argv[1] #gff
	ref_genome = argv[2] # S_lycopersicum_chromosomes.2.50.fa
	file_handler  = open(file_name)
	lines = file_handler.readlines()

	#output_bed_nm = file_name[:-4] + 'UTR_t.bed'
	#output_bed_nm = file_name[:-4] + 'gene.bed'
	#output_fa_nm = file_name[:-4] + 'CDS_r500.fa'
	#output_cds_nm = file_name[:-4] + 'CDS_r500.bed'
	output_UTR_nm = file_name[:-4] + 'UTR_r500.bed'
	output_fa_nm = file_name[:-4] + 'UTR_r500.fa'
	#output_mRNA_nm = file_name[:-4] + 'mRNA.gff3'
	#extract_UTR(lines, output_bed_nm)
	#extract_genes(lines, output_bed_nm)
	#extract_CDS_plus_region(lines, output_cds_nm)
	extract_UTRs_plus(lines, output_UTR_nm)
	#extract_mRNA(lines, output_mRNA_nm)
	#getfasta(ref_genome, output_bed_nm, output_fa_nm)
	getfasta(ref_genome, output_UTR_nm, output_fa_nm)
	#faidx(ref_genome, region, output_name)
	#while True():
	# OSError: Argument list too long.... 

	#gff_change_chr_name(file_name, lines)
	#extract_gene__id_name(lines)
