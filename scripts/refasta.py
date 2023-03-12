#!/usr/bin/env python

##########################################################################################
"""
	------------------------------------------------------------------------------------------
	This script convert fasta or multifasta files with sequences in several lines
	into single line fasta or multifasta files. 
	------------------------------------------------------------------------------------------
"""

##########################################################################################
#--Imports
import sys
import argparse 

def main():
	
	##########################################################################################
	#--Argument
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('fasta', type = str, help = 'fasta file')
	args = parser.parse_args()
	
	##########################################################################################
	with open(args.fasta.split('.')[0] + '_new.fa', 'w') as output:
		for name, seq in fastaRead(args.fasta):
			output.write('{}\n{}\n'.format(name,seq))

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