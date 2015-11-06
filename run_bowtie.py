from sys import argv
import os
import subprocess


if __name__ == "__main__":
	path = '/mnt/scratch/baak009/bowtie/unique_botrytis/clean_t_R/filtered/'
	#path = os.getcwd()
	dirs = os.listdir(path)
	listnum = []
	x = 0
	for file_name in dirs:
		if file_name[-6:] == ".fastq":
			print file_name
			print os.getcwd()
			cmd = ('python ~/scripts/bowtiescript2.py /mnt/scratch/baak009/data/NCBI_BcinB0510_revised11012015_2.fasta B_cinB0510 %s _0'%(path+file_name))
			e = subprocess.check_output(cmd, shell=True)
			print e