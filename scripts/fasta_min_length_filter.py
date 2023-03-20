#!/usr/bin/env python
#-*- coding: UTF-8 -*-

##########################################################################################
"""
	------------------------------------------------------------------------------------------
	This script filters out sequences shorter that selected
	output will 
	------------------------------------------------------------------------------------------
"""
##########################################################################################

from __future__ import division
import sys
import argparse

def main():

	##########################################################################################
	#--Argument
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('fasta', type = str, help = 'input fasta file')
	parser.add_argument('min', type = int,  help = 'contig min len to keep')
	args = parser.parse_args()

	##########################################################################################
	output_name = args.fasta.split('.')[0] + '_' + str(args.min) + '.fasta'

	with open(output_name, 'w') as output:
		for name, seq in fastaRead(args.fasta):
			if len(seq) >= args.min:
				output.write(">{}\n{}\n".format(name, seq))

#--Sequence manipulation
def fastaRead(fasta, split_names=False):

	with open(fasta, 'r') as infile:

		seq = ''
		for line in infile:

			line = line.strip()

			if line.startswith(">"):
				
				if seq:

					yield name, seq
					seq = ''

				name = line[1:]
				if split_names: name = line.split()[0][1:]

			else:
				seq = seq + line

	#--Last sequence
	yield name, seq

##########################################################################################
if __name__ == "__main__":

	main()