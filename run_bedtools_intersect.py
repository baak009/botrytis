from sys import argv
import os
import subprocess


if __name__ == "__main__":
	path = '/mnt/scratch/baak009/bowtie/tomato_on_botrytis/'
	#path = os.getcwd()
	dirs = os.listdir(path)
	listnum = []
	x = 0
	for file_name in dirs:
		if file_name[-11:] == "mapped0.bam":
			print file_name
			print os.getcwd()
			cmd = 'python ~/scripts/bedtools_intersect.py %s /mnt/scratch/baak009/tRNA/trnas_Botrytis_default.bed /mnt/scratch/baak009/rRNA/botrytis_rRNA_chr4_9kb.bed %s_clean.bam'%\
			((path+file_name),file_name[:-4])
			e = subprocess.check_output(cmd, shell=True)
			print e