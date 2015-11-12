"""mpileup  samtools
Create mpileup files of samtools,
extract positions with a coverage higher than x
group positions based on coverage

Author: Mirna Baak
email: mirna.baak@wur.nl
Last edited: 6-11-2015
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
	print 'group pos'
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
	
	#print coo_list
	print len(coo_list)
	return coo_list
	
def merge(coo_list,gap):
    print 'start merge'

    coo2_list = []
    temp = []
    new = []
    for item in coo_list:
    	#print 'item', item
        chrom = item[0]
        begin = int(item[1])
        end = int(item[2])
        if len(temp) == 0:
            temp = [chrom, begin, end]

        if chrom == temp[0] and (begin - temp[2] < gap):
            new = [chrom, temp[1], end]
                        
        else:
            coo2_list.append(temp)
            new = [chrom, begin, end]

        temp = new

        
    coo2_list.append(temp)
    #print coo2_list
    print len(coo2_list)
    return coo2_list

def to_gff(coo_list, length, cov, gap):
	print 'to gff file'
	output = open('coo_%s.gff'%(file_name[:6]), 'w')
	counter = 1
	source_2 = 'script_mpileup_l:%s,c:%s,g:%s'%(length,cov,gap)
	type3 = 'sRNA'
	
	score = '.'
	strand = '.'
	phase = '.'
	
	for item in coo_list:
		
		seqid = item[0]
		start = item[1]
		
		end = item[2]
		
		name = ('Name=B_%s;ID=%s:%s..%S'%(counter,seqid,start,stop))
		
		stringo = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(
			seqid, source_2, type3, start, end, score,strand,phase,name)
		
		counter += 1
		output.write(stringo)

        
	output.close()
	print 'done'

def write_output(coo_list, file_name, cov, length, gap):
	""" write output to file
	coo_list: list of coordinates of high expressed regions
	file_name: sorted bam file name
	cov: coverage (int)
	length: minimum lenght of fragment (int)
	"""
	#open output file
	output = open('coo_list_%s.txt'%(file_name[:6]), 'w')
	#write first line to output file with info
	output.write("minimum coverage: %s\nminimum length: %s\ngap: %s\n\n"%(cov, length, gap))
	#write coordinates to outputfile
	for item in coo_list:
                #print item
		output.write('%s\t%s\t%s\n'%(item[0], item[1], item[2]))

	output.close()
	
if __name__ == "__main__":
	"""Execute functions 
	"""
	#path = os.getcwd()
	path = "/mnt/scratch/baak009/bowtie/unique_botrytis/clean_t_R/"
	#path of directory with bam files
	#path = "/mnt/scratch/baak009/bowtie/unique_tomato/clean_t_r/"
	dirs = os.listdir(path)
	counter = 1
	length = 15 # minumum length of selected piece 
	cov = 5 # minimum number of reads
	gap = 5

	for file_name in dirs:
		#if file_name[-11:] == ".sorted.bam" and counter == 1:
		if file_name[-7:] == "_nn.bam" and counter == 1:	
			pileup_name = mpileup(file_name)
			list_pos = extract_pos(pileup_name, cov)
			coo_list = group_pos(list_pos, length)
			#coo_list = [['Bcin1', 1, 10],['Bcin1', 15, 20], ['Bcin1', 22, 30],['Bcin1', 34, 35]]
			coo2_list = merge(coo_list, gap)
			to_gff(coo2_list, length, cov, gap)
			write_output(coo2_list, file_name, cov, length, gap)
			#counter += 1

