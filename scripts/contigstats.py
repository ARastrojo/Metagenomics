#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################################################################
"""
	------------------------------------------------------------------------------------------
	------------------------------------------------------------------------------------------
"""

##########################################################################################
#--Imports
import sys
import os
import argparse

def main():
	
	##########################################################################################
	#--Argument
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('files', nargs="*", type = str, help = '.....')
	args = parser.parse_args()
	##########################################################################################
	
	print('{:50s}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format("sample", "contigs", "min", "max", "mean", "n50", "bases", "non_standard_bases"))
	for file in args.files:
		lengths = [len(seq) for name, seq in fastaRead(file)]
		non_standard_bases = [b for name, seq in fastaRead(file) for b in seq if b.upper() not in "ACGT" ]
		n50 = N50(lengths)
		print('{:50s}\t{}\t{}\t{}\t{:.0f}\t{}\t{}\t{}'.format(file, len(lengths), min(lengths), max(lengths), sum(lengths) / len(lengths), n50, sum(lengths), len(non_standard_bases)))



def N50(lengths):

	sorted_len = sorted(lengths, reverse = True)
	mid_total_lgth = sum(lengths) / 2
	n50 = 0
	acum_lgth = 0
	for lgth in sorted_len:
		acum_lgth = acum_lgth + lgth
		if acum_lgth < mid_total_lgth:
			continue
		else:
			n50 = lgth
			break

	return n50
			
def fastaRead(fasta):

	with open(fasta, 'r') as infile:
		
		seq = ''
		for line in infile:

			line = line.strip()

			if line.startswith(">"):
				
				if seq:

					yield name, seq
					seq = ''

				name = line

			else:
				seq = seq + line

	#--Last sequence
	yield name, seq


##########################################################################################
if __name__ == "__main__":

	main()


