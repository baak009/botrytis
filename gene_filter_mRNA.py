"""Gfilterer for genes that are matching your criteria. 

"""

from sys import argv
import os
import subprocess

def genes(lf_genes):
	list_genes = []
	for line in lf_genes:
		line = line.strip().split(',')
		list_genes.append(line[0][6:-1])
	#print list_genes
	return list_genes


def filterer(list_genes, l_fasta, output_name):
	output = open(output_name, 'w')
	counter = 0
	for line_or in l_fasta:
		if line_or.startswith('>'):
			line = line_or.strip().split(';')
			idt = line[0]
			idt = idt.split(':')
			name = idt[1][:-4]
			if name in list_genes:
				output.write(line_or)
				counter = 1
		elif counter == 1:
			output.write(line_or)
			counter = 0
		else:
			continue
			

	output.close()
     
if __name__ == "__main__":
	file_name_genes = argv[1]
	file_name_fasta = argv[2] # S_lycopersicum_chromosomes.2.50.fa
	output_name = argv[3]
	file_handler_genes  = open(file_name_genes)
	file_handler_fasta = open(file_name_fasta)
	lf_genes = file_handler_genes.readlines()
	l_fasta= file_handler_fasta.readlines()
	list_genes = genes(lf_genes)

	filterer(list_genes, l_fasta, output_name)

	