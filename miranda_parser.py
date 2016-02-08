"""Script to process miranda output

"""
from sys import argv
import os
import subprocess
from collections import defaultdict
import re
def extract_columns_filter(line, d):
	#one line at the time
	count = 1
	if line.startswith('>>'):
		line = line.strip().split()
		sub2 = line[1].split(';')
		target = sub2[1]
		score = float(line[4])
		energy = float(line[5])
		id_name = "sRNA_%s"%(count)
		#print energy
		print 'line[0]', line[0]
		key_temp = re.split('>>|:|-|\(', line[0])
		key = (key_temp[1], int(key_temp[2])+1, int(key_temp[3])) # plus 1 to make it 1 based again.
		if abs(energy) >= 20:
			d[key].append((target, score, energy)) #line[0]
			count += 1

	#print d
	return d
	#print d

def extract_genes(line,g):
	if line.startswith('>>'):
		line = line.strip().split()
		sub2 = line[1].split(';')
		target = sub2[0]
		score = float(line[4])
		energy = float(line[5])
		#print energy
		if abs(energy) >= 20 and target.startswith('ID=three'):
			g[target].append((line[0], score, energy))
	return g

def genes(lf_genes):
	list_genes = []
	for line in lf_genes:
		line = line.strip().split(',')
		list_genes.append(line[0][6:-1])
	#print list_genes
	return list_genes


def extract_diff_genes(line,f, list_genes):
	if line.startswith('>>'):
		line = line.strip().split()

		sub2 = line[1].split(';')
		#print sub2
		#construction for own extracted UTRS. in gff_parser.
		#print 'line', line
		#print 'sub2', sub2
		if sub2[0].startswith('ID=three_prime_UTR_s') or sub2[0].startswith('ID=five_prime_UTR_s'):
			if sub2[1].startswith('Alias'):
				sub3 = sub2[2].split(':')
			else:
				sub3 = sub2[1].split('=') # changed for the tomato thing. 
		else:
			sub3 = sub2[1].split(':')
		#print sub3
		#print line
		target_gene = sub3[1][:-2]
		score = float(line[4])
		energy = float(line[5])
		#print target_gene
		if abs(energy) >= 20 and target_gene in list_genes:
			f[line[0]].append((target_gene, score, energy))
	return f

def extract_number_target_genes(d, g, miranda_fnm):
	"""Count the number of genes that are targetted.
	"""
	output_nm = "%s_counts.txt"%(miranda_fnm[:-4])
	output = open(output_nm, 'w')
	output.write("miRNA\ttotal_target_genes\ttarget_genes_down\ttarget_genes\n")
	for key in d:
		if len(d[key]) > 0:
			#print key, len(d[key])
			output.write("%s\t%s\t%s\t%s\n"%(key, len(d[key]), 
				len(g[key]), str(g[key]).strip('[]')))

	output.close()

def extract_number_target_genes2(d, g, miranda_fnm):
	"""Count the number of genes that are targetted.
	"""
	print 'extract targets genes2'
	output_nm = "%s_counts2.txt"%(miranda_fnm[:-4])
	output = open(output_nm, 'w')
	output.write("miRNA\ttotal_target_genes\ttarget_genes_down\ttarget_genes\n")
	for key in d:
		if len(d[key]) > 0:
			#print key, len(d[key])
			output.write(">>%s\t%s\t%s\n"%(key, len(d[key]),len(g[key])))
			for gene in g[key]:
				#print gene
				output.write("%s\n"%(gene[0]))

	output.close()

def format_target_genes(d, g, miranda_fnm, id_dict):
	"""format the genes and target to sRNA/tgene"""
	print 'format target genes'
	output_nm = "%s_netwerk.txt"%(miranda_fnm[:-4])
	output = open(output_nm, 'w')
	#output.write("sRNA\ttotal_target_genes\ttarget_genes_down\ttarget_genes\n")
	for key in d:
		if len(d[key]) > 0:
			#print key, len(d[key])
			name = "sRNA_%s"%(count)
			#output.write(">>%s\t%s\t%s\n"%(key, len(d[key]),len(g[key])))
			for gene in g[key]:
				#print gene
				output.write("%s\t%s\t%s\n"%(id_dict[key], gene[0], key))

	output.close()

if __name__ == "__main__":
	print 'jajaja'
	miranda_fnm = argv[1] 
	genes_fnm= argv[2] 

	#extract_results

	file_handler_genes  = open(genes_fnm)
	lf_genes = file_handler_genes.readlines()
	list_genes = genes(lf_genes)


	file_handler = open(miranda_fnm, 'r')
	list_lines = []
	d = defaultdict(list)
	g = defaultdict(list)
	for line in file_handler:
		d = extract_columns_filter(line, d)
		#d = extract_genes(line, d)
		g = extract_diff_genes(line, g, list_genes)
	print len(d)
	
	id_dict = defaultdict(list)
	count = 1
	for key in d:
		#print key
		id_name = "sRNA_%s"%(count)
		id_dict[key] = id_name
		count += 1
	print id_dict
	extract_number_target_genes(d, g, miranda_fnm)
	extract_number_target_genes2(d,g,miranda_fnm)
	format_target_genes(d,g,miranda_fnm, id_dict)
