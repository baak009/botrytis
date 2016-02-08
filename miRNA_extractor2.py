"""Mirna baak
miRNA extractor
use a pileup file
calculate the number of start en stop of reads per position. 

"""

from sys import argv
import os
import subprocess
import re

def read_pileup(pileup_fnm):
	"""Loop through pileup file to extract the number of starts
	and ends of reads at a position

	pileup_fnm = pileup file name

	l_n_begin = list of number of starts per position on positive strand
	l_n_end = list of number of ends per position on positive strand
	l_n_begin_r = = list of number of starts per position on negative strand
	l_n_end_r = list of number of ends per position on negative strand
	l_chr = list of the chromosome per position
	l_b_pos = list of begin positions
	"""

	print 'read pileup file'
	file_handler = open(pileup_fnm, 'r')
	l_chr = []
	l_b_pos = []
	l_cov = []
	l_n_begin = []
	l_n_end = []
	l_n_begin_r = []
	l_n_end_r = []
	for line in file_handler:
		#print line
		line = line.strip().split()
		l_chr.append(line[0])
		l_b_pos.append(line[1])
		l_cov.append(line[3])
		#print line[3]
		if int(line[3]) != 0:
			p_sentence = line[4]
			count_begin = len(re.findall('\^.\.', p_sentence))
			count_end = len(re.findall('\$\.', p_sentence))
			count_begin_r = len(re.findall('\^.\,', p_sentence))
			count_end_r = len(re.findall('\$\,', p_sentence))
		else:
			count_begin = 0
			count_end = 0
			count_begin_r = 0
			count_end_r = 0
		l_n_begin.append(count_begin)
		l_n_end.append(count_end)
		l_n_begin_r.append(count_begin_r)
		l_n_end_r.append(count_end_r)
	file_handler.close()
	return l_n_begin, l_n_end, l_n_begin_r, l_n_end_r, l_chr, l_b_pos

def extract_pos(l_n_begin, l_n_end, l_chr, l_b_pos, output_nm, thr_begin, thr_end, sign):
	""" Take the positions above the threshold and get the sRNAs
		 start and end positions

	l_n_begin = list of number of starts per position 
	l_n_end = list of number of ends per position 
	l_chr = list of the chromosome per position
	l_b_pos = list of begin positions
	output_nm = name of the gff outputfile produced in this function
	thr_begin = threshold of number of starts of a read
	thr_end = threshold of number of ends of a read
	sign = + or - depending of positive or negative strand

	temp_list = list with tuples with positions of sRNAs that are above threshold
	 consisting of (chromsome, begin position, end positions, sign, number of starts,
	 number of ends, length of sequence.)
	"""
	
	print 'extract positions '+ sign + ' strand'
	output = open(output_nm, 'w')

	threshold = int(thr_begin) # 300
	temp = []
	temp_list = []

	for x in range(len(l_n_begin)):
		if l_n_begin[x] > threshold:
			end_temp = None
			for y in range(19,24): # is length 20 till 24
				try:
					end_p = l_n_end[x+y]
					if end_temp < end_p:
						end_temp = end_p
						pos_end_temp = x+y
				except:
					continue

			if int(end_temp) > int(thr_end): #10
				end_position = int(l_b_pos[x]) + (pos_end_temp - x)

				output.write("%s\tmiRNA_extractor.py\tsRNA\t%s\t%s\t.\t%s\t.\t%s,%s,%s\n"%
					(l_chr[x],(int(l_b_pos[x])), end_position, sign,l_n_begin[x],
						end_temp,(int(end_position)- int(l_b_pos[x]) +1)))
				temp_list.append((l_chr[x],(int(l_b_pos[x])), end_position, sign,l_n_begin[x],
						end_temp,(int(end_position)- int(l_b_pos[x]) +1)))
			else:
				print 'for %s\t%s position, starting reads:%s no end position in range is found.'%(
					l_chr[x],l_b_pos[x], l_n_begin[x])

	output.close()
	return temp_list	

"""
def extract_pos_reverse_comp(l_n_begin_r, l_n_end_r, l_chr, l_b_pos, output_nm, thr_begin, thr_end):
	
	print 'extract positions reverse strand'
	output = open(output_nm, 'w')
	#output.write("Chr\tbegin\tend\tnm_reads_begin\tnm_reads_end\n")
	threshold = int(thr_begin)#
	temp = []
	temp_list = []
	for x in range(len(l_n_end_r)):
		#print l_n_end_r[x]
		if l_n_end_r[x] > int(threshold):
			begin_temp = None
			for y in range(19,24): # is length 20 till 24
				try:
					if y <= x:
						begin_p = l_n_begin_r[x-y]
						#print 'begin_p', begin_p
						if begin_temp <= begin_p:
							begin_temp = begin_p
							pos_begin_temp = x-y
				except:
					continue

			if begin_temp > int(thr_end):
				#print begin_temp
				begin_position = l_b_pos[pos_begin_temp]
				output.write("%s\tmiRNA_extractor.py\tmiRNA\t%s\t%s\t.\t-\t.\t%s,%s,%s\n"%
					(l_chr[x],begin_position, l_b_pos[x], 
						begin_temp, l_n_end_r[x],
						(abs(int(l_b_pos[x]) - int(begin_position)) +1)))
				temp_list.append(l_chr[x],begin_position, l_b_pos[x], 
						begin_temp, l_n_end_r[x],
						(abs(int(l_b_pos[x]) - int(begin_position)) +1))
			else:
				print 'for %s\t%s position, starting reads:%s no end position in range is found.'%(
					l_chr[x],l_b_pos[x], l_n_begin[x])
				
	#temp = temp.sort()
	
	output.close()
	return temp_list
	#print temp
"""

def filter_file(temp_list, output_nm_filter):
	"""filter file that if end position is the same one sRNA will remain.
	take the longest sequence with same end position

	temp_list = list with tuples with positions of sRNAs that are above threshold
	 consisting of (chromsome, begin position, end positions, sign, number of starts,
	 number of ends, length of sequence.)
	output_nm_filter = file name of output
	"""
	print 'filter positions'
	#output = open(output_nm_filter, 'w')
	#output.write("Chr\tbegin\tend\tnm_reads_begin\tnm_reads_end\n")
	with open(output_nm_filter, 'a') as output:
		temp_end = 0
		for x in temp_list:
			#print 'x', x
			end = x[2]
			if temp_end != end:
				#print x
				temp_end = end

				output.write("%s\tmiRNA_extractor.py\tsRNA\t%s\t%s\t.\t%s\t.\t%s,%s,%s\n"%
							(x[0],x[1], x[2], 
								x[3], x[4], x[5], x[6]))

					

	#output.close()
	#print temp

def unique_pos(temp_list, note_ls, output_nm_unique):
	"""extract only unique positions. If you use the multimapping files. 

	temp_list = list with tuples with positions of sRNAs that are above threshold
	 consisting of (chromsome, begin position, end positions, sign, number of starts,
	 number of ends, length of sequence.)
	note_ls = list of number of number of start, end en length of sRNAs

	"""
	print 'unique positions'
	#rint temp_list
	#output = open(output_nm_filter, 'w')
	#output.write("Chr\tbegin\tend\tnm_reads_begin\tnm_reads_end\n")
	with open(output_nm_unique, 'a') as output:
		temp_end = 0
		for x in temp_list:
			#print 'x', x
			note = (x[4],x[5],x[6])
			#print note
			if note not in note_ls:
				#print x
				note_ls.append(note)
				output.write("%s\tmiRNA_extractor.py\tsRNA\t%s\t%s\t.\t%s\t.\t%s,%s,%s\n"%
							(x[0],x[1], x[2], 
								x[3], x[4], x[5], x[6]))
	#print note_ls

	return note_ls

if __name__ == "__main__":

	pileup_fnm = argv[1] #"pileupI24BsBCIN141707990_1708042.txt"
	output_nm = argv[2] #"pileupI24BsBCIN141707990_1708042_extract.gff"
	thr_begin = argv[3]
	thr_end = argv[4]
	note_ls = []
	print 'threshold start', thr_begin
	print 'threshold end', thr_end

	# remove already existing files
	if os.path.exists("%s_filter.gff"%(output_nm[:-4])): 
		cmd = 'rm %s_filter.gff'%(output_nm[:-4])
		res1 = subprocess.check_call(cmd, shell=True)
		print res1
	
	if os.path.exists("%s_unique.gff"%(output_nm[:-4])): 
		cmd = 'rm %s_unique.gff'%(output_nm[:-4])
		res1 = subprocess.check_call(cmd, shell=True)
		print res1


	l_n_begin, l_n_end, l_n_begin_r, l_n_end_r, l_chr, l_b_pos = read_pileup(pileup_fnm)
	#output_nm_rev = "%s_rev.gff"%(output_nm[:-4]) #"pileupI24BsBCIN141707990_1708042_extract.gff"
	# positive strand
	sign = '+'
	temp_list = extract_pos(l_n_begin, l_n_end, l_chr, l_b_pos, output_nm, thr_begin, thr_end, sign)
	output_nm_filter = "%s_filter.gff"%(output_nm[:-4])
	output_nm_unique = "%s_unique.gff"%(output_nm[:-4]) 
	filter_file(temp_list, output_nm_filter)
	note_ls = unique_pos(temp_list, note_ls, output_nm_unique)
	
	#negative strand
	sign = '-'
	output_nm_rev = "%s_rev.gff"%(output_nm[:-4]) 
	temp_list = extract_pos(l_n_begin_r, l_n_end_r, l_chr, l_b_pos, output_nm_rev, thr_begin, thr_end, sign)
	#output_nm_filter_rev = "%s_rev_filter.gff"%(output_nm[:-4]) 
	filter_file(temp_list, output_nm_filter)
	note_ls = unique_pos(temp_list, note_ls, output_nm_unique)

	#output_nm_rev_comp = "%s_rev_comp.gff"%(output_nm[:-4]) 
	#temp_list = extract_pos_reverse_comp(l_n_begin_r, l_n_end_r, l_chr, l_b_pos, output_nm_rev_comp, thr_begin, thr_end)

	#path = '/mnt/scratch/baak009/bowtie/unique_tomato/clean_t_r/'
	#path = os.getcwd()
	#dirs = os.listdir(path)
	
