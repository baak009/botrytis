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
		
		line = line.strip().split()
		#print line
		if line[0].startswith("#"):
			#print line
			continue

		elif counter == 0:
			try:
				#print '2',line
				start = int(line[0])
				chrom = str(line[0])
				if len(chrom) == 1:
					chrom = '0'+chrom
				chrom_new = prefix + chrom
				source = str(line[1])
				feature = str(line[2])
				start = str(line[3])
				end = str(line[4])
				#print end
				score = str('.')
				#print score
				strand = str(line[5])
				#print strand
				if feature == 'CDS':
					frame = str(line[6])
				else:
					frame = str('.')
				#print frame
				#source = source.strip('\n')
				#print 'source',source
				attribute = line[-1]
				#print 'rest', attribute
				total = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(chrom_new, source, feature, 
					start, end, score, strand, frame, attribute)
				#print 'total', total
				output.write(total)
				
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
	#print lines
	gff_change_chr_name(lines, output_name)