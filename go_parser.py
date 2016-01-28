"""Go terms parser
input: ITAG2.4.go.csv
Go.terms_alt_ids.txt


"""
from collections import defaultdict
from sys import argv
import os
import subprocess
	
def dict_go_terms(lines_go_terms):
    dict_gnm = {}
    for line in lines_go_terms:
        line = line.strip().split()
        if line[0].startswith('!'):
            continue
        else:
            temp = []
            for x in range(len(line)):
                if not line[x].startswith("GO:"):
                    temp.append(line[x])



            dict_gnm[line[0]] = temp
            temp = []

    print dict_gnm      
    return dict_gnm


def gene_ID_go_term(lines_genes, dict_gnm, output_name):
    output = open(output_name,'w')
    
    for line in lines_genes:
        line_tmp = line.strip().split()
        if line_tmp[0].startswith('GeneID'):
            continue
        else:
            gene = line_tmp[0]
            GO = line_tmp[1]
           
            if dict_gnm.has_key(str(GO)):
                #print gene
                #print dict_term[gene]
                term = dict_gnm[str(GO)]
                term_p = ' '.join(term)
                str_output = "%s\t%s\t%s\n"%(gene, GO,term_p)
            else:
                #print gene
                term_p = "."
                str_output = "%s\t%s\t%s\n"%(gene,GO,term_p)
            #print str_output
            output.write(str_output)
    output.close()

if __name__ == "__main__":
    file_name = argv[1] # ITAG2.4.go.csv
    go_name = argv[2] #GO.term_alt_ids.txt
    file_handler  = open(file_name)
    lines_genes = file_handler.readlines()	
    file_handler_go = open(go_name)
    lines_go = file_handler_go.readlines()
    output_name = "%s_term.txt"%file_name[:-4]
    print output_name
    print file_name
        
    dict_gnm = dict_go_terms(lines_go)
    gene_ID_go_term(lines_genes, dict_gnm, output_name)
