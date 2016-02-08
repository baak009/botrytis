"""Go terms parser
input: Botrytis_cinerea_GO_annotation_EBI_june2015.txt


"""
from collections import defaultdict
from sys import argv
import os
import subprocess
	
def dict_go_terms(lines_go_terms):

    dict_gnm = defaultdict(list)
    for line in lines_go_terms:
        line = line.strip().split()
        if line[0].startswith('stable'):
            continue
        else:
            dict_gnm[line[0]].append(line[1].strip("'"))

    #print dict_gnm      
    return dict_gnm


def gene_ID_go_term(dict_gnm, output_name):
    output = open(output_name,'w')
    for key in dict_gnm:
        str_output = "%s\t%s\n"%(key[:-2], (', '.join(dict_gnm[key])))
        output.write(str_output)
    output.close()

def dict_go_terms_tomato(lines_go_terms):

    dict_gnm = defaultdict(list)
    for line in lines_go_terms:
        line = line.strip().split()
        if line[0].startswith('GeneID'):
            continue
        else:
            dict_gnm["gene:"+line[0]].append(line[1].strip("'"))

    print dict_gnm      
    return dict_gnm
if __name__ == "__main__":
    file_name = argv[1] 
    file_handler  = open(file_name)
    lines = file_handler.readlines()	
    
    output_name = "%s_topgo.txt"%file_name[:-4]
    print output_name
    print file_name
        
    dict_gnm = dict_go_terms(lines)
    dict_gnm = dict_go_terms_tomato(lines)
    gene_ID_go_term(dict_gnm, output_name)
