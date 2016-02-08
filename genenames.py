"""adding gene names to list of interesting genes.
input: ITAG2.4.genemodels.mRNA.gff3
sigI12I160.10.csv

wrapper: genenames_wrapper.py
"""
from collections import defaultdict
from sys import argv
import os
import subprocess
	
def dict_gene_terms(lines_itag):
    dict_gnm = {}
    for line in lines_itag:
        #print line
        line = line.strip().split()
        if line[0].startswith('#'):
            continue
        else:
            new_line = line[8]
            
            new_line = new_line.split(';')
            #print new_line[1:]
            dict_gnm[new_line[0][8:-2]] = new_line[1:]
            #print dict_gnm[new_line[0][8:-2]]

    #print dict_gnm      
    return dict_gnm

def dict_go_terms(lines_terms):

    dict_ggo = defaultdict(list)
    for line in lines_terms:
        line = line.strip().split('\t')
        if line[0].startswith('stable_id'):
            continue
        else:
            temp = [w.replace(',', ' ') for w in line[1:]]
            dict_ggo[line[0][:-2]].append(','.join(temp))
    #print dict_ggo
    return dict_ggo


def add_gene_names(lines_genes, dict_term, output_name):
    # using with the go terms file
    output = open(output_name,'w')
    
    for line in lines_genes:
        line_tmp = line.strip().split(',')
        if line_tmp[0].startswith('#') or line_tmp[0].startswith('""'):
            output.write("%s,GO_id,GO_term\n"%(line.strip()))
 
        else:
            if line_tmp[0].startswith('"gene'):
                gene = line_tmp[0][6:-1]
            elif line_tmp[0].startswith('"Bcin'):
                gene = line_tmp[0][1:-1]
            else:
                gene = line_tmp[0]
            if dict_term.has_key(str(gene)): #changed
                #print gene
                #print dict_term[gene]
                term = dict_term[str(gene)]
                term_p = ','.join(term)
                str_output = "%s,%s\n"%(line.strip(),term_p)
            else:
                #print gene
                term_p = "."
                str_output = "%s,%s\n"%(line.strip(),term_p)
            #print str_output
            output.write(str_output)
    output.close()

def add_gene_names3(lines_genes, dict_term, output_name):
    # using with the go terms file
    output = open(output_name,'w')
    
    for line in lines_genes:
        line_tmp = line.strip().split()
        print line_tmp
        if line_tmp[0].startswith('#') or line_tmp[0].startswith('""'):
            output.write("%s,GO_id,GO_term\n"%(line.strip()))
 
        else:
            if line_tmp[0].startswith('"gene'):
                gene = line_tmp[0][6:-1]
            elif line_tmp[0].startswith('"Bcin'):
                gene = line_tmp[0][1:-1]
            else:
                gene = line_tmp[1]
            print gene
            if dict_term.has_key(str(gene)): #changed
                print gene
                #print dict_term[gene]
                term = dict_term[str(gene)]
                term_p = ','.join(term)
                str_output = "%s,%s\n"%(line.strip(),term_p)
            else:
                #print gene
                term_p = "."
                str_output = "%s,%s\n"%(line.strip(),term_p)
            #print str_output
            output.write(str_output)
    output.close()

def add_gene_names2(lines_genes, dict_term, output_name):
    #using with the itag gene model file
    output = open(output_name,'w')
    print dict_term
    for line in lines_genes:
        line_tmp = line.strip().split(',')
        if line_tmp[0].startswith('#') or line_tmp[0].startswith('""'):
            output.write("%s,note,name, parent, additional\n"%(line.strip()))
            print 'ja'
        else:
            if line_tmp[0].startswith('"gene'):
                gene = line_tmp[0][6:-1]
            elif line_tmp[0].startswith('"Bcin'):
                gene = line_tmp[0][1:-1]
            else:
                gene = line_tmp[0] #
            if dict_term.has_key(str(gene)): #changed
                count = 0
                #print gene
                #print dict_term[gene]
                term = dict_term[str(gene)]
                name = '.'
                parent = '.'
                note = '.'
                rest = '.'
                for item in term:
                    if item.startswith('Name='):
                        name = item[5:]
                    elif item.startswith('Parent='):
                        parent = item[7:]
                    elif item.startswith('Note='):
                        note = item[5:]
                    else:
                        rest = "\trest:\t%s"%(item)

                str_output = "%s,%s,%s,%s,%s\n"%(line.strip(),note, name, parent, rest)
            else:
                #print gene
                term_p = "."
                str_output = "%s,%s\n"%(line.strip(),term_p)
            #print str_output
            output.write(str_output)
    output.close()

def add_gene_names4(lines_genes, dict_term, output_name):
    #using with the itag gene model file
    output = open(output_name,'w')
    print dict_term
    for line in lines_genes:
        line_tmp = line.strip().split()
        print line_tmp
        if line_tmp[0].startswith('#') or line_tmp[0].startswith('""'):
            output.write("%s,note,name, parent, additional\n"%(line.strip()))
            print 'ja'
        else:
            if line_tmp[0].startswith('"gene'):
                gene = line_tmp[0][6:-1]
            elif line_tmp[0].startswith('"Bcin'):
                gene = line_tmp[0][1:-1]
            else:
                gene = line_tmp[1] #
            if dict_term.has_key(str(gene)): #changed
                count = 0
                #print gene
                #print dict_term[gene]
                term = dict_term[str(gene)]
                name = '.'
                parent = '.'
                note = '.'
                rest = '.'
                for item in term:
                    if item.startswith('Name='):
                        name = item[5:]
                    elif item.startswith('Parent='):
                        parent = item[7:]
                    elif item.startswith('Note='):
                        note = item[5:]
                    else:
                        rest = "\trest:\t%s"%(item)

                str_output = "%s,%s,%s,%s,%s\n"%(line.strip(),note, name, parent, rest)
            else:
                #print gene
                term_p = "."
                str_output = "%s,%s\n"%(line.strip(),term_p)
            #print str_output
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
    print output_name
    print file_name
    if file_name[-4:] == '.txt': # go term botrytis
        print 'go terms botrytis'
        output_name = "%s_go.csv"%(genes_name[:-4])
        dict_term = dict_go_terms(lines_itag)
        #add_gene_names(lines_genes, dict_term, output_name)
        add_gene_names3(lines_genes, dict_term, output_name)
    else: # itag tomato
        print 'itag tomato'
        output_name = "%s_gene.csv"%(genes_name[:-4])
        dict_term = dict_gene_terms(lines_itag)
        #add_gene_names2(lines_genes, dict_term, output_name)
        add_gene_names4(lines_genes, dict_term, output_name)

