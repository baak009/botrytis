from sys import argv
import os
import subprocess

def bedtools_multicov(file_names, gff_file_nm):
	"""execute multicov bedtools

	file_name: sorted bam file 
	"""
	print 'bedtools multicov'
	#create outputname of mpileup file
	print gff_file_nm
	temp_out = gff_file_nm.split('/')
	print temp_out
	output_name = 'cov_%s.txt'%(temp_out[-1][:-4])
	stats_multicov = open('stats_%s.txt'%(temp_out[-1][:-4]),'w')
	print output_name
	#check if output already exists, if not execute mpileup
	if os.path.exists('%s'%(output_name)) == False:
		cmd = 'bedtools multicov -bams %s -bed %s > %s'%(file_names,
		gff_file_nm, output_name) # bed file path moet nog anders
		print cmd 
		e = subprocess.check_call(cmd, shell=True)
		print e
	else: 
		print "multicov file already exist"

	stats_multicov.write(string_files)
	stats_multicov.close()
	return output_name
	'dit nog maken'

def bam_index(path, bam_file):
	""" sam to  bam with samtools
	"""
	
	cmd3 = 'samtools index %s'%(path+bam_file)
	print cmd3
	print os.getcwd()
	if os.path.exists(path+bam_file) and os.path.exists('%s.bai'% (path+bam_file[:-4])) == False:
			res3 = subprocess.check_call(cmd3, shell=True)
			print res3
			
	else:
		print 'file does not exist'
		print 'done'

if __name__ == "__main__":
	"""Execute functions 
	"""
	#path = os.getcwd()
	path = "/mnt/scratch/baak009/bowtie/unique_botrytis/clean_t_R/"
	#path of directory with bam files
	#path = "/mnt/scratch/baak009/bowtie/unique_tomato/clean_t_r/"
	dirs = os.listdir(path)
	gff_file_nm = argv[1]
	counter = 1
	length = 18 # minumum length of selected piece 
	#cov = 3 # botrytis
	cov = 7500 # minimum number of reads tomato
	gap = 2
	print 'length',length, 'cov',cov, 'gap', gap
	#file_name = 'merged_all_f_I.bam' # define
	string_files = ""
	list_files = []
	for bam_name in dirs:

		if bam_name[-12:] == "sorted_f.bam" and bam_name[:5] != "stats" and counter == 1:

			list_files.append(path+bam_name)
			if os.path.exists(path+bam_name + '.bai') == False:
				bam_index(path,bam_name)

	list_file = list_files.sort()
	print list_files

	string_files = ' '.join(list_files)
	bedtools_multicov(string_files, gff_file_nm)