"""mpileup  samtools
Create mpileup files of samtools,
extract positions with a coverage higher than x
group positions based on coverage

Author: Mirna Baak
email: mirna.baak@wur.nl
Last edited: 8-12-2015

change the directory pileup, create it 

run in clean_t_R/pileup
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
	output_name = file_name[:-4] + '_pileup.txt'
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
	output_gff_nm = 'coo_%s_%s_%s_%s.gff'%(file_name[:-4],length,cov,gap)
	if os.path.exists(output_gff_nm) == False:
		output = open(output_gff_nm, 'w')
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
			
			name = ('Name=B_%s;ID=%s:%s..%s'%(counter,seqid,start,end))
			
			stringo = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(
				seqid, source_2, type3, start, end, score,strand,phase,name)
			
			counter += 1
			output.write(stringo)

	        
		output.close()
		print 'done'
	else:
		print 'output_gff already exists'

def write_output(coo_list, file_name, cov, length, gap):
	""" write output to file
	coo_list: list of coordinates of high expressed regions
	file_name: sorted bam file name
	cov: coverage (int)
	length: minimum lenght of fragment (int)
	"""
	#open output file
	output_list_nm = 'coo_list_%s_%s_%s_%s.txt'%(file_name[:-4],length,cov,gap)
	if os.path.exists(output_list_nm) == False:
		output = open(output_list_nm, 'w')
		#write first line to output file with info
		output.write("minimum coverage: %s\nminimum length: %s\ngap: %s\n\n"%(cov, length, gap))
		#write coordinates to outputfile
		for item in coo_list:
	                #print item
			output.write('%s\t%s\t%s\n'%(item[0], item[1], item[2]))

		output.close()
	else:
		print 'coo_list already exists'

def bedtools_multicov(file_names, gff_file_nm, cov, length, gap):
	"""execute multicov bedtools

	file_name: sorted bam file 
	"""
	print 'bedtools multicov'
	#create outputname of mpileup file
	output_name = 'cov_%s_%s_%s_%s.txt'%(file_name[:-4], cov,length,gap)
	stats_multicov = open(('stats_%s_%s_%s_%s.txt'%(file_name[:-4], length,cov,gap)), 'w')
	print output_name
	#check if output already exists, if not execute mpileup
	if os.path.exists('%s'%(output_name)) == False:
		cmd = 'cd ..; bedtools multicov -bams %s -bed ./pileup/%s > %s'%(file_names,
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
	#path = "/mnt/scratch/baak009/bowtie/unique_botrytis/clean_t_R/"
	#path of directory with bam files
	path = "/mnt/scratch/baak009/bowtie/unique_tomato/clean_t_r/"
	dirs = os.listdir(path)
	
	counter = 1
	length = 18 # minumum length of selected piece 
	#cov = 3 # botrytis
	cov = 5000 # minimum number of reads tomato
	gap = 2
	print 'length',length, 'cov',cov, 'gap', gap
	file_name = 'merged_all_f_I.bam' # define
	#file_name = 'merged_all_f_AF.bam'
	#file_name = 'merged_all_f_bam.bam'
	#file_name = 'merged_all_nn.bam'
	gff_file_nm = 'coo_%s_%s_%s_%s.gff'%(file_name[:-4],length,cov,gap)
	pileup_name = mpileup(file_name)
	list_pos = extract_pos(pileup_name, cov)
	coo_list = group_pos(list_pos, length)
	coo2_list = merge(coo_list, gap)
	to_gff(coo2_list, length, cov, gap)
	write_output(coo2_list, file_name, cov, length, gap)

	string_files = ""
	list_files = []
	for bam_name in dirs:
		#print file_name
		#if file_name[-11:] == ".sorted.bam" and counter == 1:
		if bam_name[-12:] == "sorted_f.bam" and bam_name[:5] != "stats" and counter == 1:
			#print file_name
			list_files.append(bam_name)
			if os.path.exists(path+bam_name + '.bai') == False:
				bam_index(path,bam_name)
			#string_files = "%s %s "%(string_files, file_name)
	#print list_files
	list_file = list_files.sort()
	#print list_files

	string_files = ' '.join(list_files)
	bedtools_multicov(string_files, gff_file_nm, cov, length, gap)

	'''		#counter += 1
	for file_name in dirs:
		#if file_name[-11:] == ".sorted.bam" and counter == 1:
		if file_name[-9:] == "f_bam.bam" and counter == 1:
			print file_name	
			pileup_name = mpileup(file_name)
			list_pos = extract_pos(pileup_name, cov)
			coo_list = group_pos(list_pos, length)
			#coo_list = [['Bcin1', 1, 10],['Bcin1', 15, 20], ['Bcin1', 22, 30],['Bcin1', 34, 35]]
			coo2_list = merge(coo_list, gap)
			to_gff(coo2_list, length, cov, gap)
			write_output(coo2_list, file_name, cov, length, gap)
			#counter += 1
	''' 