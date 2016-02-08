""" Wrapper siRNA pipeline
"""

from sys import argv
import os
import subprocess


def extractor(pileup_file, output_nm, cov_b, cov_e):
	""" Executing extractor

	"""
	print 'executing bedtools getfasta'
	if os.path.exists(pileup_file): 
		cmd = 'python ~/gitrepos/botrytis/miRNA_extractor2.py %s %s %s %s'%(
			pileup_file, output_nm, cov_b, cov_e)
		res1 = subprocess.check_call(cmd,shell=True)
		print 'res1'
		print res1

def validation(validation_file):
	""" Executing validation
	validation file bedfile
	"""
	print 'executing validation'
	if os.path.exists(validation_file): 
		cmd = 'python ~/gitrepos/botrytis/bedops_bedmap_validation.py %s'%(
			validation_file)
		res1 = subprocess.check_call(cmd,shell=True)
		print 'res1'
		print res1

def convert_fasta(reference_fasta, bed_file, output_fa):
	""" Executing get fasta sequences
	
	"""
	print 'executing convert to fasta'
	if os.path.exists(reference_fasta) and os.path.exists(bed_file): 
		cmd = 'python ~/gitrepos/botrytis/get_fasta_region.py %s %s %s'%(
			reference_fasta, bed_file, output_fa)
		res1 = subprocess.check_call(cmd,shell=True)
		print 'res1'
		print res1

def multimapping(reference_fasta, ref_name, input_fa, num_mismatch):
	""" bowtie multimapping
	
	"""
	print 'executing multimapping'
	if os.path.exists(reference_fasta) and os.path.exists(bed_file): 
		cmd = 'python ~/gitrepos/botrytis/bowtiescript3.py %s %s %s %s '%(
			reference_fasta, ref_name, input_fa, num_mismatch)
		res1 = subprocess.check_call(cmd,shell=True)
		print 'res1'
		print res1

def siRNA_bedtools(bed_file, gff_file, bam_file):
	""" siRNA bedtools
	for filtering and 
	
	"""
	print 'executing siRNA_bedtools'
	if os.path.exists(reference_fasta) and os.path.exists(bed_file): 
		cmd = 'python ~/gitrepos/botrytis/siRNA_bedtools.py %s %s %s '%(
			bed_file, gff_file, bam_file)
		res1 = subprocess.check_call(cmd,shell=True)
		print 'res1'
		print res1

if __name__ == "__main__":
	path = os.getcwd()
	#dirs = os.listdir(path)

	pileup_file = argv[1] #merged_I_f_a_pileup.txt
	output_nm = argv[2] #out_merged_I_f_a_pileup_extractor_300_10_t.gff
	cov_b = argv[3]
	cov_e = argv[4]
	extractor(pileup_file, output_nm, cov_b, cov_e)
	
	validation_file = argv[5] #weiberg_siRNA_a_best.sorted.bed
	validation(validation_file)
	
	reference_fasta = argv[6] #/mnt/scratch/baak009/data/NCBI_BcinB0510_revised11012015_2.fasta 
	bed_file = "%s_unique.bed"%(output_nm[:-4])
	output_fa = "%s_unique.fa"%(output_nm[:-4])
	convert_fasta(reference_fasta, bed_file, output_fa)

	reference_fasta2 = argv[7]
	reference_name2 = argv[8]
	num_mismatch = argv[9]
	multimapping(reference_fasta2, reference_name2, output_fa, num_mismatch)
	
	output_bam = output_fa[:-4] +str(num_mismatch) + 'a.bam'
	bed_file2 = argv[10]
	gff_file2 = argv[11]
	siRNA_bedtools(bed_file2, gff_file2, output_bam)
	#bed_file = "ITAG2.4_gene_models.gene.bed"
	#gff_file = "ITAG2.4_gene_models.gff3"


	#file_name = argv[1] #"NCBI_BcinB0510_revised11012015_2.fasta"
	#file_name = "S_lycopersicum_chromosomes.2.50.fa"
	#ref_name = argv[2] # "B_cinB0510"
	#ref_name = "S_lyn_2_50"
	#bowtie_build(file_name, ref_name)
	#path2 = "/mnt/scratch/baak009/trimmed_adapt_reads/"
	

	
	#file_name_fasta = argv[3] #"I12As_S23_R1_001_trimmed.fastq"
	#file_name_fastq = "B16Bs_S19_h400.fastq"


	#num_mismatch = argv[-1] #0
	#print '4', num_mismatch
	#running bowtie
	#output_sam = bowtie(num_mismatch,file_name_fasta ,ref_name)
	#output_sam = 'I12As_S23_R1_001_trimmed0.sam' 
	#sam_to_bam(output_sam)