"""sam parser for regions to get the unique reads 
of the regions with their coordinates.

baak009@myers:/mnt/scratch/baak009/miRNA/botrytis/validation$ python ~/gitrepos/botrytis/sam_region_parser.py coo_merged_all_f_I_18_600_2.bed  test600.sam

"""
from collections import defaultdict
from collections import Counter
from sys import argv
import os
import subprocess
	

def dict_pos(lines_region): #dit moet nog een beetje anders
    dict_t = defaultdict(list)
    for line in lines_region:
        line = line.strip().split('\t')
        chrom = line[0]
        begin = int(line[1])
        begin_adj = int(line[1])
        end = int(line[2])
        dict_t[(chrom, begin_adj, end)] = []
    #print dict_t
    return dict_t

def extractor(dict_t, lines_sam):
    list_keys = list(dict_t.keys())
    #print list_keys

    for line in lines_sam:
        line = line.strip().split('\t')
        chrom = line[2]
        begin = int(line[3])
        end = int(line[3]) + int(line[5][:-1])
        seq = str(line[9])
        for key in list_keys:
            #print key[0]
            if chrom == key[0]:
                #print chrom
                #print begin, key[1]
                if begin >= (key[1]-1) and begin <= key[2]:
                    dict_t[key].append((begin,seq))


    #print dict_t
    return dict_t

def writer(dict_t, output_name):
    #klopt nog niet door niet super sorted.
    output_name2 = "%s_filtered.txt"%(output_name[:-4])
    output = open(output_name, 'w')
    output2 = open(output_name2, 'w')
    seq = ""
    b_temp = ""
    s_temp = ""
    c = 1
    #print dict_t
    for key in dict_t:
        values = dict_t[key]
        #print values
        counter = 1
        v_prev = ""
        temp_list = []
        for k,v in Counter(values).most_common():
            #print k, v
            output.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(
                key[0],key[1],key[2],v,k[0], k[0]+len(k[1]), k[1]))
            
            length = int(key[2])- int(key[1])
            if length > 25: # regions spanning more than 25 nt
                if v > 100: # more than 100 reads
                    if k[0] in temp_list or (k[0] + 1) in temp_list or \
                    (k[0] + 2) in temp_list or (k[0] + 3) in temp_list :
                        continue # in range of 3 positions

                    elif k[0] in temp_list or (k[0] - 1) in temp_list or \
                    (k[0] - 2) in temp_list or (k[0] - 3) in temp_list :
                        continue # in range of minus 3 positions
                    else: #write region + start and sequence
                        temp_list.append(k[0])
                        output2.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(
                        key[0],key[1],key[2],v,k[0],k[0]+len(k[1]), k[1]))
            


            else: #regions shorter than 25 nt
                if counter == 1: # take only the read with the largest appearence. 
                    output2.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(
                        key[0],key[1],key[2],v,k[0], k[0]+len(k[1]), k[1]))
                    counter += 1
            
    output.close()
    output2.close()
    """
        for x in range(len(values)):

            b = values[x][0]
            s = values[x][1]

            if b == b_temp and s == s_temp:
                #b = b_prev
                #s = s_prev
                c+= 1
            elif x == 0:
                #output.write("%s\t%s\t%s\t%s\n"%(key, c, b_temp, s_temp))
                b_temp = b
                s_temp = s 
                c = 1
            else:
                output.write("%s\t%s\t%s\t%s\t%s\t%s\n"%(
                    key[0],key[1],key[2], c, b_temp, s_temp))
                b_temp = b
                s_temp = s 
                c = 1
        output.write("%s\t%s\t%s\t%s\t%s\t%s\n"%(
            key[0],key[1],key[2], c, b_temp, s_temp))
"""
                    



if __name__ == "__main__":
    region_f= argv[1] # coo_merged_all_f_I_18_600.bed
    sam_f = argv[2] # test600.sam
    file_handler  = open(region_f)
    lines_region = file_handler.readlines()	
    file_handler_go = open(sam_f)
    lines_sam = file_handler_go.readlines()
    output_name = "%s_seq.txt"%region_f[:-4]
    print output_name
    print region_f
        
    dict_t = dict_pos(lines_region)
    dict_t = extractor(dict_t, lines_sam)
    writer(dict_t, output_name)