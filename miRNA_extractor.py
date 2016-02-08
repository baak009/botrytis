"""Mirna baak
miRNA extractor
use a pileup file
calculate the number of start en stop of reads per position. 

build in per chromosome
"""

from sys import argv
import os
import subprocess

def read_pileup(pileup_fnm):
	print 'read pileup file'
	file_handler = open(pileup_fnm, 'r')
	l_chr = []
	l_b_pos = []
	l_cov = []
	l_n_begin = []
	l_n_end = []
	for line in file_handler:
		#print line
		line = line.strip().split()
		l_chr.append(line[0])
		l_b_pos.append(line[1])
		l_cov.append(line[3])
		#print line[3]
		if int(line[3]) != 0:
			p_sentence = line[4]
			count_begin = p_sentence.count('^')
			count_end = p_sentence.count('$')
		else:
			count_begin = 0
			count_end = 0
		l_n_begin.append(count_begin)
		l_n_end.append(count_end)

		#print 'begin', count_begin
		#print 'end', count_end
	#print l_n_begin
	#print l_n_end
	#print l_b_pos
	return l_n_begin, l_n_end, l_chr, l_b_pos

def extract_pos(l_n_begin, l_n_end, l_chr, l_b_pos, output_nm):
	"""check if numbering start position is correct -1 or +1
	"""
	print 'extract positions'
	output = open(output_nm, 'w')
	#output.write("Chr\tbegin\tend\tnm_reads_begin\tnm_reads_end\n")
	threshold = 300
	temp = []
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
			if end_temp > 10:
				end_position = int(l_b_pos[x]) + (pos_end_temp - x)
				#str_all = (l_chr[x],l_b_pos[x], end_position, l_n_begin[x],end_temp, x,pos_end_temp)
				#temp.append(str_all)

				output.write("%s\tmiRNA_extractor.py\tmiRNA\t%s\t%s\t.\t+\t.\t%s %s %s\n"%
					(l_chr[x],l_b_pos[x], end_position, l_n_begin[x],
						end_temp,(int(end_position)- int(l_b_pos[x]) +1)))
			else:
				print 'for %s\t%s position, starting reads:%s no end position in range is found.'%(
					l_chr[x],l_b_pos[x], l_n_begin[x])
				
	#temp = temp.sort()

	output.close()
	#print temp
def extract_pos_reverse(l_n_begin, l_n_end, l_chr, l_b_pos, output_nm):
	"""check if numbering start position is correct -1 or +1
	"""
	print 'extract positions'
	output = open(output_nm, 'w')
	#output.write("Chr\tbegin\tend\tnm_reads_begin\tnm_reads_end\n")
	threshold = 300
	temp = []
	for x in range(len(l_n_begin)):
		if l_n_begin[x] > threshold:
			end_temp = None
			for y in range(19,24): # is length 20 till 24
				try:
					end_p = l_n_end[x-y]
					if end_temp < end_p:
						end_temp = end_p
						pos_end_temp = x-y
				except:
					continue

			if end_temp > 10:
				end_position = int(l_b_pos[x]) + (pos_end_temp - x)
				#str_all = (l_chr[x],l_b_pos[x], end_position, l_n_begin[x],end_temp, x,pos_end_temp)
				#temp.append(str_all)

				output.write("%s\tmiRNA_extractor.py\tmiRNA\t%s\t%s\t.\t+\t.\t%s %s %s\n"%
					(l_chr[x],l_b_pos[x], end_position, l_n_begin[x],
						end_temp,(abs(int(l_b_pos[x]) - int(end_position)) +1)))
			else:
				print 'for %s\t%s position, starting reads:%s no end position in range is found.'%(
					l_chr[x],l_b_pos[x], l_n_begin[x])
				
	#temp = temp.sort()

	output.close()
	#print temp




if __name__ == "__main__":

	pileup_fnm = argv[1] #"pileupI24BsBCIN141707990_1708042.txt"
	output_nm = argv[2] #"pileupI24BsBCIN141707990_1708042_extract.gff"
	l_n_begin, l_n_end, l_chr, l_b_pos = read_pileup(pileup_fnm)

	extract_pos(l_n_begin, l_n_end, l_chr, l_b_pos, output_nm)
	#extract_pos_reverse(l_n_begin, l_n_end, l_chr, l_b_pos, output_nm)
	#path = '/mnt/scratch/baak009/bowtie/unique_tomato/clean_t_r/'
	#path = os.getcwd()
	#dirs = os.listdir(path)
	
