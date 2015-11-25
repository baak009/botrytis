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
	output_nm = 'outcl_%s'%(bam_nm[:-11])
	print "Converting cufflinks step 1"
	print bam_nm
	cmd1 = 'cufflinks -p %s -g %s -o %s %s'%(pros, gtf_nm, output_nm, bam_nm)
	
	if os.path.exists(bam_nm) and os.path.exists(output_nm) == False:
			res1 = subprocess.check_call(cmd1, shell=True)
			print res1
			
			print 'directory created: outcl_%s'%(bam_nm[:-11])
	else:
		print 'file does not exist'
	print 'done'

def cuffmerge(gtf_nm, ref_genome, assemblie):
	""" cuffmerge
	"""
	print "cuffmerge"
	cmd1 = 'cuffmerge -p 4 -g %s -s %s %s'%(gtf_nm, ref_genome, assemblie)
	print assemblie
	if os.path.exists(assemblie) and os.path.exists('merged_asm/merged.gtf') == False:
			res1 = subprocess.check_call(cmd1, shell=True)
			print res1
			
	else:
		print 'file does not exist'
	print 'done'
def cuffquant():
	print 'iets'

	
def cuffdiff(diff_name, ref_genome, sample_names, bam_files):
	""" cuff_diff
	"""
	output_nm = 'outdiff_%s'%(diff_name)
	print "cuffdiff"
	cmd1 = 'cuffdiff -p 4 -o %s -b %s -L %s -u merged_asm/merged.gtf %s'%(
		output_nm, ref_genome, sample_names, bam_files)
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
	pros = 4
	#file_name = 'M16Am_hisat2.sorted.bam'
	#file_name = 'M12Am_hisat2.sorted.bam'
	#print file_name
	gtf_name = '/mnt/scratch/baak009/data/ITAG2.4_gene_models.gtf'
	ref_genome  = '/mnt/scratch/baak009/data/S_lycopersicum_chromosomes.2.50.fa'
	#assemblie = 'assemblie_I_M.txt'
	#cufflinks(pros, file_name, gtf_name)
	assemblie = 'assemblie_M.txt'
	#diff_name = 'I_M_tomato'
	diff_name = 'M_tomato'
	#sample_names = 'M12,M16,M24,I12,I16,I24'
	sample_names = 'M12,M16,M24'
	#bam_files = './M12Am_hisat2.sorted.bam \
	#./M16Am_hisat2.sorted.bam \
	#./M24Am_hisat2.sorted.bam \
	#./I12Am_hisat2.sorted.bam,./I12Bm_hisat2.sorted.bam \
	#./I16Am_hisat2.sorted.bam,./I16Bm_hisat2.sorted.bam \
	#./I24Bm_hisat2.sorted.bam,./I24Dm_hisat2.sorted.bam'

	bam_files = './M12Am_hisat2.sorted.bam \
	./M16Am_hisat2.sorted.bam \
	./M24Am_hisat2.sorted.bam'

	'''
	for file_name in dirs:
		if file_name[-11:] == ".sorted.bam" and counter == 1:
			cufflinks(pros, file_name, gtf_name)

		#counter += 1
	'''
	cuffmerge(gtf_name, ref_genome, assemblie)
	cuffdiff(diff_name, ref_genome, sample_names, bam_files)
	