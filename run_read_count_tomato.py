from sys import argv
import os
import subprocess


if __name__ == "__main__":
	path = '/mnt/scratch/baak009/bowtie/unique_tomato/clean_t_r/'
	#path = os.getcwd()
	dirs = os.listdir(path)
	for file_name in dirs:
		if file_name[-4:] == ".bam":
			print file_name
			print os.getcwd()
			cmd = ('python ~/scripts/read_count.py tomato_genome_sizes.txt 50 %s'%(path+file_name))
			print cmd
			e = subprocess.check_output(cmd, shell=True)
			print e

 #python ~/scripts/read_count.py Botrytis_genome_sizes.txt 50 /mnt/scratch/baak009/bowtie/unique_botrytis/clean_t_R/I12As_trimmed0.mapped0.un_mapped0_clean.bam
