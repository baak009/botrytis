from sys import argv
import os
import subprocess

def bedtogff(gff_file_nm, type_f):
	print 'executing bedops gff to bed'
	if type_f == 0:
		output_name = "%s.bed"%(gff_file_nm[:-4])
	if type_f == 1:
		output_name = "%s.bed"%(gff_file_nm[:-5])

	if os.path.exists(gff_file_nm) and os.path.exists(output_name) == False: 
		cmd = "gff2bed < %s > %s"%(gff_file_nm, output_name)
		res1 = subprocess.check_call(cmd,shell=True)
		print 'res1'
		print res1
		return output_name
	else:
		print 'nothing happening'

def bedops_bedmap(range_of_interest_file, annotations_file):

	print 'executing bedops bedmap'
	output_name = "%s.annotated.bed"%(range_of_interest_file[:-4])
	if os.path.exists(range_of_interest_file):  
		cmd = "bedmap --fraction-ref 0.9 --echo --echo-map-id --delim '\t' %s %s > %s"%(
			range_of_interest_file, annotations_file, output_name)
		# --fraction-ref = procent of bases that must overlap the annotation file
		# --range = grab elements within int bp of ref-files element
		res1 = subprocess.check_call(cmd,shell=True)
		print 'res1'
		print res1
		return output_name
	else:
		print "nothing happening"


if __name__ == "__main__":
	#path = '/mnt/scratch/baak009/bowtie/unique_tomato/clean_t_r/'
	path = os.getcwd()
	dirs = os.listdir(path)
	annotations_file = argv[1]
	for file_name in dirs:
		if file_name[-4:] == ".gff":
			bedtogff(file_name, type_f = 0)
		elif file_name[-5:] == ".gff3":
			bedtogff(file_name, type_f = 1)
		else:
			continue
			

	dirs = os.listdir(path)
	for file_name_bed in dirs:
		if file_name_bed[-4:] == ".bed" and file_name_bed != str(annotations_file):
			print file_name_bed
			print annotations_file
			bedops_bedmap(file_name_bed, annotations_file)

 #python ~/scripts/read_count.py Botrytis_genome_sizes.txt 50 /mnt/scratch/baak009/bowtie/unique_botrytis/clean_t_R/I12As_trimmed0.mapped0.un_mapped0_clean.bam
#python ~/gitrepos/botrytis/genenames.py ITAG2.4_gene_models.mRNA.gff3 sigIM0.052.csv