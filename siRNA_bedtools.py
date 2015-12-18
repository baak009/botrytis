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

def bedtools_intersect(file_A, file_B, output_name, path):
	""" Executing bedtools intersect 

	"""
	print 'executing bedtools intersect'
	if os.path.exists(file_A) and os.path.exists(file_B) and os.path.exists(output_name) == False: 
		cmd = "bedtools intersect -a %s -b %s > %s"%(file_A, file_B, output_name)
		res1 = subprocess.check_call(cmd,shell=True)
		print 'res1'
		print res1
    



	


def get_region(lines, bam_file):
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
		samtools_view(bam_file, format, outputname)


def samtools_view(bam_file, format, outputname):
	print 'executing samtools view'
	
	if os.path.exists(bam_file) and os.path.exists(outputname) == False: 
		cmd = "samtools view -b %s %s > %s"%(bam_file, format, outputname)
		res1 = subprocess.check_call(cmd,shell=True)
		print 'res1'
		print res1

	else:
		print 'file already exists'
	bamtofastq(outputname)


def bamtofastq(file_name_bam):
	print 'bam to fastq'
	output_nm = '%s.fastq'%(file_name_bam[:-4])
	if os.path.exists(file_name_bam) and os.path.exists(output_nm) == False:
		cmd2 = 'bedtools bamtofastq -i %s -fq %s'%(file_name_bam,output_nm)
		e = subprocess.check_output(cmd2, shell=True)
		print e
	else:
		print 'bam to fastq not executed'

	unique_reads(output_nm)
	#return output_nm

def unique_reads(input_nm):
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
	top_reads(output_nm)

def top_reads(input_nm): # get only the reads that 

	unique_file_handler = open(input_nm)
	lines = unique_file_handler.readlines()
	counter = 0
	with open("topreads.txt", "a") as output:
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
	print '2', output_sam

	if os.path.exists(file_name_fasta) and os.path.exists(output_sam) == False:
		#output_sam = file_name_fastq2[-1]+str(num_mismatch) + '.sam'
		print '3', output_sam
		cmd = 'bowtie -S -v %s -a %s -f %s %s 2> stats_%s_%s_a.txt'%(num_mismatch, ref_name, 
			file_name_fasta, output_sam, file_name_fasta[:-4], num_mismatch)
		res1 = subprocess.check_call(cmd, shell=True)
		print cmd
		print res1
	
	else:
		print 'file does not exist'
	#return output_sam



if __name__ == "__main__":
	path = os.getcwd()

	file_name_A =  argv[1]#"coo.gff"
	file_name_B =  argv[2]#"merged I.bam"

	#output_name =  argv[3]#".bam"

	file_handler = open(file_name_A)
	lines = file_handler.readlines()
	get_region(lines, file_name_B)
	num_mismatch = 0 
	file_name_reads = 'topreads.txt'
	fasta_genome_name = "S_lycopersicum_chromosomes.2.50.fa"
	ref_name = "S_lyn_2_50"
	bowtie(num_mismatch, file_name_reads, ref_name)

	#bedtools_intersect(file_name_A, file_name_B, output_name, path)
	#output_nm = bamtofastq(output_name)
	#output_nm = unique_reads(output_nm)
	