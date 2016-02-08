""" Wrapper sRNA pipeline
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
	print validation_file
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
	print reference_fasta
	print bed_file
	if os.path.exists(reference_fasta): 
		cmd = 'python ~/gitrepos/botrytis/get_fasta_region.py %s %s %s'%(
			reference_fasta, bed_file, output_fa)
		res1 = subprocess.check_call(cmd,shell=True)
		print 'res1'
		print res1

def miranda(sRNA_fasta, target_fa, output_nm):
	"""Executing miranda
	"""
	print 'executing miranda'
	if os.path.exists(sRNA_fasta) and os.path.exists(target_fa): 
		cmd = 'miranda %s %s -out %s'%(sRNA_fasta, target_fa, output_nm)
		res1 = subprocess.check_call(cmd,shell=True)
		print 'res1'
		print res1

def miranda_parser(miranda_output ,genes_filtered):
	"""Executing miranda parser
	"""
	print 'executing miranda parser'
	if os.path.exists(miranda_output) and os.path.exists(genes_filtered):
		cmd = 'python ~/gitrepos/botrytis/miranda_parser.py %s %s'%(
			miranda_output, genes_filtered)
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
	#extractor(pileup_file, output_nm, cov_b, cov_e)
	
	validation_file = argv[5] #weiberg_siRNA_a_best.sorted.bed
	#validation(validation_file)
	
	reference_fasta = argv[6] #/mnt/scratch/baak009/data/NCBI_BcinB0510_revised11012015_2.fasta 
	bed_file = "%s_unique.bed"%(output_nm[:-4])
	output_fa = "%s_unique.fa"%(output_nm[:-4])
	#convert_fasta(reference_fasta, bed_file, output_fa)

	sRNA_fasta = "%s_unique_filtered.fa"%(output_nm[:-4])
	target_fa = argv[7] #../data/ITAG2.4_gene_models.UTR_r500.fa
	output_miranda = "%s_unique_filtered_%s.txt"%(output_nm[:-4], target_fa[-9:-3]) # changed to txt on 3-2
	#miranda(sRNA_fasta, target_fa, output_miranda)

	genes_filtered = argv[8] # filtered_genes.csv
	miranda_parser(output_miranda, genes_filtered)