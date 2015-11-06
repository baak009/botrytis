"""mpileup  samtools
Create mpileup files of samtools,
extract positions with a coverage higher than x
group positions based on coverage

Author: Mirna Baak
Last editted: 6-11-2015
"""
#import modules
from sys import argv
import os
import subprocess


def mpileup(file_name):
	"""execute mpileup command sam file

	file_name: sorted bam file 
	"""
	#create outputname of mpileup file
	output_name = file_name[:5] + '_pileup.txt'
	print output_name
	#check if output already exists, if not execute mpileup
	if os.path.exists('%s'%(output_name)) == False:
		cmd = 'samtools mpileup ../%s > %s'%(file_name, output_name)
		e = subprocess.check_call(cmd, shell=True)
		print e
	else: 
		print "pileup file already exist"

	return output_name

def extract_pos(pileup_name, cov):
	"""extract positions of pileup file where 
	coverage is higher than: cov
	
	pileup_name: name of output of mpileup
	cov: number of coverage (int)

	list_new = list of positions with coverage higher than cov
	"""
	print 'start extract_pos'

	#read file lines
	file_handler  = open(pileup_name)
	list_file = file_handler.readlines()
	count = 0
	#create empty list
	list_new = []
	# loop through list and find positions with a higher coverage than cov
	for line in list_file:
		line_new = line.split()
	
		if int(line_new[3]) > cov:
			count += 1
			list_new.append(line_new)
	#print count

	return list_new

def group_pos(list_pos, length):
	"""make groups of positions, who are laying together.
	Write only to file, ones that are longer than: length

	list_pos: list of positions with coverage higher than cov
	length: minimum length of group sequence (int)

	coo_list: list of coordinates of high expressed regions
	"""
	#create emtylists
	coo_list = []
	temp_list = []
	temp2_list	= []
	#loop over positions
	for x in list_pos:

		start_pos = int(x[1]) 
		chromosome = x[0]
		# extract positions that follow up previous position, 
		#or create a new group
		if len(temp_list) == 0:
			temp_list.append(start_pos)
			temp2_list.append(chromosome)

		elif start_pos == (int(temp_list[-1]) + 1):
			temp_list.append(start_pos)
			temp2_list.append(chromosome)
		#create coordinates list with length of region is above length(int)
		else:
			if (temp_list[-1] - temp_list[0]) > length:
				coo_list.append([temp2_list[0],temp_list[0], temp_list[-1]])
			temp_list = []
			temp2_list = []
			temp_list.append(start_pos)
			temp2_list.append(chromosome)
	return coo_list
	#print coo_list
	print len(coo_list)

def write_output(coo_list, file_name, cov, length):
	""" write output to file
	coo_list: list of coordinates of high expressed regions
	file_name: sorted bam file name
	cov: coverage (int)
	length: minimum lenght of fragment (int)
	"""
	#open output file
	output = open('coo_list_%s.txt'%(file_name[:6]), 'w')
	#write first line to output file with info
	output.write("minimum coverage: %s\nminimum length: %s\n\n"%(cov, length))
	#write coordinates to outputfile
	for item in coo_list:
		output.write('%s\t%s\t%s\n'%(item[0], item[1], item[2]))

	output.close()
	
if __name__ == "__main__":
	"""Execute functions 
	"""
	#path = os.getcwd()
	#path = "/mnt/scratch/baak009/bowtie/unique_botrytis/clean_t_R/"
	#path of directory with bam files
	path = "/mnt/scratch/baak009/bowtie/unique_tomato/clean_t_r/"
	dirs = os.listdir(path)
	counter = 1
	length = 15 # minumum length of selected piece 
	cov = 5 # minimum number of reads
	for file_name in dirs:
		if file_name[-11:] == ".sorted.bam" and counter == 1:
			pileup_name = mpileup(file_name)
			#list_pos = extract_pos(pileup_name, cov)
			#coo_list = group_pos(list_pos, length)
			#write_output(coo_list, file_name, cov, length)
			#counter += 1

