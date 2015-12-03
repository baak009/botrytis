"""GFF parser

"""

from sys import argv
import os
import subprocess

def gff_change_chr_name(lines, output_name):
	output = open(output_name, 'w')
	line_new = []
	line_temp = []
	string = ""
	string_temp = ""
	#print lines
	prefix = 'BCIN'
	counter = 0
	for x in range(len(lines)):
		#print counter
		line = lines[x]
		#print line
		line = line.strip().split()
		if line[0].startswith("#"):
			continue

		elif counter == 0:
			try:
				start = int(line[0])
				chrom = str(line[0])
				if len(chrom) == 1:
					chrom = '0'+chrom
				chrom_new = prefix + chrom
				source = str(lines[x+1]).strip(' ')
				source = source.strip('\n')
				#print 'source',source
				rest = lines[x+2]
				#print rest
				total = "%s\t%s%s"%(chrom_new, source, rest)
				#print 'total', total
				output.write(total)
				counter += 1
			except:
				continue
		elif counter == 1:
			counter += 1
		elif counter == 2:
			counter = 0
		else:
			print 'something wrong'
		
	    
if __name__ == "__main__":
	file_name = argv[1]
	#ref_genome = argv[2] # S_lycopersicum_chromosomes.2.50.fa
	output_name = argv[2]
	file_handler  = open(file_name)
	lines = file_handler.readlines()

	gff_change_chr_name(lines, output_name)