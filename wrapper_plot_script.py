""" Wrapper plotScript
"""

from sys import argv
import os
import subprocess


def plotter(gene):
	""" Executing extractor

	"""
	print 'executing plotter'

	cmd = 'Rscript ~/gitrepos/botrytis/plotscript.R filtered_genes.csv %s'%(
		gene)
	res1 = subprocess.check_call(cmd,shell=True)
	print 'res1'
	print res1


if __name__ == "__main__":
	path = os.getcwd()
	#dirs = os.listdir(path)
	file_name = "out_merged_I_f_a_pileup_extractor_600_10_b_unique_filtered_R_r50_netwerk.txt"
	file_handler = open(file_name)
	lines = file_handler.readlines()
	for line in lines:
		line = line.strip().split('\t')
		gene = line[1]
		plotter(gene)


	