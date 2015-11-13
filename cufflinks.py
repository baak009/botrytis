#cufflinks

"""cufflinks

Author: Mirna Baak
Last editted: 13-11-2015
"""
#import modules
from sys import argv
import os
import subprocess

def cufflinks(pros, bam_nm, gtf_nm):
	""" cufflinks 
	"""
	output_nm = 'outcl_%s'%(bam_nm[:-4])
	print "Converting cufflinks step 1"
	cmd1 = 'cufflinks -p %s -g %s -o %s %s'%(pros, gtf_nm, output_nm, bam_nm)
	
	if os.path.exists(bam_nm) and os.path.exists('outcl_%s'%(bam_nm[:-4])) == False:
			res1 = subprocess.check_call(cmd1, shell=True)
			print res1
			
			print 'directory created: outcl_%s'%(bam_nm[:-4])
	else:
		print 'file does not exist'
	print 'done'

def cuffmerge(gtf_nm, ref_genome, assemblie):
	""" cuffmerge
	"""
	print "cuffmerge"
	cmd1 = 'cuffmerge -g %s -s %s %s'%(gtf_nm, ref_genome, assemblie)

	if os.path.exists(assemblie) and os.path.exists('merged_asm/merged.gtf') == False:
			res1 = subprocess.check_call(cmd1, shell=True)
			print res1
			
	else:
		print 'file does not exist'
	print 'done'

def cuffdiff(diff_name, ref_genome, sample_names, bam_files):
	""" cuff_diff
	"""
	output_nm = 'outdiff_%s'%(diff_name)
	print "cuffdiff"

	cmd1 = 'cuffdiff -o %s -b %s -L %s -u merged_asm/merged.gtf %s'(output_nm, ref_genome, sample_names, bam_files)
    print cmd1
	if os.path.exists('merged_asm/merged.gtf') and os.path.exists(output_nm) == False:
			res1 = subprocess.check_call(cmd1, shell=True)
			print res1
			
	else:
		print 'file does not exist'
	print 'done'	

if __name__ == "__main__":

	#path = "/mnt/scratch/baak009/hisat2/tomato/w_cuff"
	path = os.getcwd()
	dirs = os.listdir(path)
	counter = 1
	pros = 2
	file_name = 'M16Am_hisat2.sorted.bam'
	gtf_name = '/mnt/scratch/baak009/data/ITAG2.4_gene_models.gtf'
	ref_genome  = '/mnt/scratch/baak009/data/S_lycopersicum_chromosomes.2.50.fa'
	assemblie = 'assemblies.txt'
	cufflinks(pros, file_name, gtf_name)

	diff_name = 'testt'
	sample_names = 'M12Am, M16Am'
	bam_files = './M12Am_hisat2.sorted.bam, ./M16Am_hisat2.sorted.bam'
	'''
	for file_name in dirs:
		if file_name[-11:] == ".sorted.bam" and counter == 1:
			cufflinks(pros, file_name)

		counter += 1
	'''