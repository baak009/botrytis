from sys import argv
import os
import subprocess


if __name__ == "__main__":
	path = '/mnt/scratch/baak009/bowtie/unique_tomato/'
	#path = os.getcwd()
	dirs = os.listdir(path)
	listnum = []
	x = 0
	for file_name in dirs:
		if file_name[-6:] == ".fastq":
			print file_name
			print os.getcwd()
			cmd = ('python ~/scripts/bowtiescript2.py /mnt/scratch/baak009/data/S_lycopersicum_chromosomes.2.50.fa S_lyn_2_50 %s 0'%(path+file_name))
			e = subprocess.check_output(cmd, shell=True)
			print e