"""adding gene names to list of interesting genes.
input: ITAG2.4.genemodels.mRNA.gff3
sigI12I160.10.csv

wrapper: genenames_wrapper.py
"""

from sys import argv
import os
import subprocess
	
def dict_gene_terms(lines_itag):
    dict_gnm = {}
    for line in lines_itag:
        line = line.strip().split()
        if line[0].startswith('#'):
            continue
        else:
            new_line = line[8]
            new_line = new_line.split(';')
            dict_gnm[new_line[0][8:-2]] = new_line[1:]

    #print dict_gnm      
    return dict_gnm

def add_gene_names(lines_genes, dict_gnm, output_name):
    output = open(output_name,'w')
    
    for line in lines_genes:
        line_tmp = line.strip().split(',')
	if line_tmp[0].startswith('#') or line_tmp[0].startswith('""'):
            output.write(line)
            continue
	else:
            if line_tmp[0].startswith('"gene'):
                gene = line_tmp[0][6:-1]
            else:
                gene = line_tmp[0]
 
            term = dict_gnm[str(gene)]
            term_p = ','.join(term)
            str_output = "%s,%s\n"%(line,term_p)
            
            output.write(str_output)
    output.close()

if __name__ == "__main__":
    file_name = argv[1] # ITAG.mRNA.gff3
    genes_name = argv[2] # sig.csv
    file_handler  = open(file_name)
    lines_itag = file_handler.readlines()	
    file_handler_genes = open(genes_name)
    lines_genes = file_handler_genes.readlines()
    output_name = "%s_gene.csv"%(genes_name[:-4])
  
    dict_gnm = dict_gene_terms(lines_itag)
    add_gene_names(lines_genes, dict_gnm, output_name)
