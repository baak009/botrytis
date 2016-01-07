"""
bedtools intersect for siRNA
Author: Mirna Baak
Last editted: 16-12-2015


baak009@myers:/mnt/scratch/baak009/bowtie/tomato_on_botrytis/overlap_reads_clean_bot_ref/pileup$

"""
#import modules
from sys import argv
import os
import subprocess


def get_region(lines, bam_file, file_name_reads):
	#print lines
	for line in lines:
		#print line
		line = line.strip().split()
		#print line
		chrom = line[0]
		start = line[3]
		end = line[4]
		format = "%s:%s-%s"%(chrom,start,end)
		outputname = "reads_%s_%s_%s.bam"%(chrom,start,end)
		samtools_view(bam_file, format, outputname, file_name_reads)


def samtools_view(bam_file, format, outputname, file_name_reads):
	print 'executing samtools view'
	
	if os.path.exists(bam_file) and os.path.exists(outputname) == False: 
		cmd = "samtools view -b %s %s > %s"%(bam_file, format, outputname)
		res1 = subprocess.check_call(cmd,shell=True)
		print 'res1'
		print res1

	else:
		print 'file already exists'
	bamtofastq(outputname, file_name_reads)


def bamtofastq(file_name_bam, file_name_reads):
	print 'bam to fastq'
	output_nm = '%s.fastq'%(file_name_bam[:-4])
	if os.path.exists(file_name_bam) and os.path.exists(output_nm) == False:
		cmd2 = 'bedtools bamtofastq -i %s -fq %s'%(file_name_bam,output_nm)
		e = subprocess.check_output(cmd2, shell=True)
		print e
		cmd3 = 'rm %s'%(file_name_bam)
		f = subprocess.check_output(cmd3, shell=True)
		print f
	else:
		print 'bam to fastq not executed'

	unique_reads(output_nm, file_name_reads)
	#return output_nm

def unique_reads(input_nm,file_name_reads):
	print 'unique reads'
	output_nm = '%s_unique.fasta'%(input_nm[:-6])
	cmd1 = 'fastx_collapser -i %s -o %s'%(input_nm, output_nm) # only on meyers
	print cmd1
	if os.path.exists(input_nm) and os.path.exists(output_nm) == False:
			res1 = subprocess.check_call(cmd1, shell=True)
			print res1
			
			print 'file created: %s'%(output_nm)
	else:
		print 'file already created or not existing'
	print 'done'
	top_reads(output_nm, file_name_reads)

def top_reads(input_nm, file_name_reads): # get only the reads that 

	unique_file_handler = open(input_nm)
	lines = unique_file_handler.readlines()
	counter = 0
	
	#with open("topreads2.txt", "a") as output: # moet nog anders
	with open(file_name_reads, "a") as output: # moet nog anders	
		#output.write(input_nm + '\n') 
		for line in lines:
			if counter == 0:
				name = ">%s-%s"%(input_nm[6:-13], line[1:])
				output.write(name)
				counter += 1
			elif counter < 2:
				output.write(line)
				counter += 1

def bowtie(num_mismatch, file_name_fasta, ref_name): # we zijn hier
	print "Executing bowtie with %s mismatches"%(num_mismatch)

	output_sam = file_name_fasta[:-4] +str(num_mismatch) + 'a.sam'
	output_bam = file_name_fasta[:-4] +str(num_mismatch) + 'a.bam'
	print '2', output_sam

	if os.path.exists(file_name_fasta): #and os.path.exists(output_sam) == False:
		#output_sam = file_name_fastq2[-1]+str(num_mismatch) + '.sam'
		print '3', output_sam
		cmd = 'bowtie -S -v %s -a %s -f %s %s 2> stats_%s_%s_a.txt'%(num_mismatch, ref_name, 
			file_name_fasta, output_sam, file_name_fasta[:-4], num_mismatch)
		res1 = subprocess.check_call(cmd, shell=True)
		print cmd
		print res1
		cmd2 = 'samtools view -b -S %s > %s.bam'%(output_sam, output_sam[:-4])
		print cmd2
		res2 = subprocess.check_call(cmd2,shell=True)
		
		print res2
	
	else:
		print 'file does not exist'
	return output_bam

def bedtools_intersect(bed_file, bam_file):
	""" Executing bedtools intersect 

	"""
	print 'executing bedtools intersect'
	output_name = "%s.filtered.bam"%(bam_file[:-4])
	if os.path.exists(bed_file) and os.path.exists(bam_file):  #and os.path.exists(output_name) == False: 
		cmd = "bedtools intersect -a %s -b %s > %s"%(bam_file, bed_file, output_name)
		res1 = subprocess.check_call(cmd,shell=True)
		print 'res1'
		print res1
		cmd2 = 'samtools view -h %s > %s.sam'%(output_name, output_name[:-4])
		res2 = subprocess.check_call(cmd2,shell=True)
		print cmd2
		print res2
    
def bedtools_intersect2(gff_file, bam_file):
	""" Executing bedtools intersect getting the gff file contents matching your query

	"""
	print 'executing bedtools intersect'
	output_name = "%s.filtered.bed"%(bam_file[:-4])
	if os.path.exists(bed_file) and os.path.exists(bam_file):  #and os.path.exists(output_name) == False: 
		cmd = "bedtools intersect -wb -a %s -b %s > %s"%(gff_file, bam_file, output_name)
		res1 = subprocess.check_call(cmd,shell=True)
		print 'res1'
		print res1
		#cmd2 = 'samtools view -h %s > %s.sam'%(output_name, output_name[:-4])
		#res2 = subprocess.check_call(cmd2,shell=True)
		#print cmd2
		#print res2
		return output_name

def parser_cleaner(input_bedintersect):
	"""Select only the lines with CDS and UTR in it. 
	"""
	cmd = "cat %s |grep 'UTR\|CDS' > %s.utr_cds.txt"%(input_bedintersect, input_bedintersect[:-4])
	res1 = subprocess.check_call(cmd,shell=True)
	print 'res1'
	print res1



if __name__ == "__main__":
	path = os.getcwd()

	file_name_A =  argv[1]#"coo.gff"
	file_name_B =  argv[2]#"merged I.bam"

	#output_name =  argv[3]#".bam"

	file_handler = open(file_name_A)
	lines = file_handler.readlines()
	file_name_reads = '%s_topreads.txt'%(file_name_A[:-4])
	get_region(lines, file_name_B, file_name_reads)
	num_mismatch = 0 
	
	fasta_genome_name = "S_lycopersicum_chromosomes.2.50.fa"
	ref_name = "S_lyn_2_50"
	output_bam = bowtie(num_mismatch, file_name_reads, ref_name)
	bed_file = "ITAG2.4_gene_models.gene.bed"
	gff_file = "ITAG2.4_gene_models.gff3"
	bedtools_intersect(bed_file,output_bam)
	input_bedintersect = bedtools_intersect2(gff_file,output_bam)
	parser_cleaner(input_bedintersect)

	#bedtools_intersect(file_name_A, file_name_B, output_name, path)
	#output_nm = bamtofastq(output_name)
	#output_nm = unique_reads(output_nm)
	