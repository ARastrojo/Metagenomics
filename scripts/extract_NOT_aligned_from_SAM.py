#!/usr/bin/env python

##########################################################################################
"""
------------------------------------------------------------------------------------------
Extracts only not aligned reads from a sam file.
If one of the paired reads aligns both are discarded

Require:
pysam v0.20.0
samtools v1.11
------------------------------------------------------------------------------------------
"""
##########################################################################################

#--Imports
import argparse
import pysam
import os
import re
import gzip
import subprocess

__author__ = "Alberto Rastrojo"
__version_info__ = ('1','0','0')
__version__ = '.'.join(__version_info__)


def main():

	##########################################################################################
	#--Argument
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('sam', type = str, help = 'aligment file (sam) ')
	parser.add_argument('output', type = str, help = 'output prefix. Include percentage symbol were 1/2 reads must be included')
	parser.add_argument('-n', dest = 'remove', action='store_false', default = True, help = 'Remove temporal files. Default: True')
	parser.add_argument('-v', '--version', action='version', version=__file__ + ' Version ' + __version__)
	args = parser.parse_args()
	##########################################################################################

	#--Converting sam to bam, sorting reads by name and indexing
	subprocess.call(f'samtools view -bS {args.sam} > {args.output}.bam', shell=True)
	subprocess.call(f'samtools sort -n {args.output}.bam  -o {args.output}_sorted.bam', shell=True)
	subprocess.call(f'samtools view -h {args.output}_sorted.bam > {args.output}_sorted.sam', shell=True)

	#--Reading alignment file
	alignmet = pysam.AlignmentFile(args.output + '_sorted.sam', "r")
	mapped = {read.query_name:1 for read in alignmet if read.is_mapped}
	alignmet.close()

	#--Writing unmampped reads
	if "%" in args.output:
		output_1 = re.sub('%', '1', args.output)
		output_2 = re.sub('%', '2', args.output)
	else:
		output_1 = f'{args.output}_R1'
		output_2 = f'{args.output}_R2'

	r1 = gzip.open(f"{output_1}.fq.gz", 'wb')
	r2 = gzip.open(f"{output_2}.fq.gz", 'wb')
	alignmet = pysam.AlignmentFile(args.output + '_sorted.sam', "r")
	for read in alignmet:
		if mapped.get(read.query_name):
			continue
		else:
			if read.is_read1:
				r1.write(('@{}\n{}\n+\n{}\n'.format(read.query_name, read.query_sequence,read.qual)).encode())
			else: #--Read_2
				r2.write(('@{}\n{}\n+\n{}\n'.format(read.query_name, read.query_sequence,read.qual)).encode())
	r1.close()
	r2.close()

	#--Remove temporal files
	if args.remove:
		os.remove(args.output + '.bam')
		os.remove(args.output + '_sorted.bam')
		os.remove(args.output + '_sorted.sam')

##########################################################################################
if __name__ == "__main__":

	main()
