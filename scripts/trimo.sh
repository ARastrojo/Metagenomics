#!/bin/bash
hostname

#--Argument control
if [[ $# -ne 5 ]]
        then
        echo '--------------------------------------------------------------------------------------------------------------'
        echo 'Usage: trimo.sh <R1.fastq.gz><R2.fastq.gz><minQ><minL><cores>'
        echo '--------------------------------------------------------------------------------------------------------------'
        exit
fi

#--Variables
r1=$1
r2=$2
minq=$3
minl=$4
out1=`echo ${1} | awk -F '.' '{print $1}'`
out2=`echo ${2} | awk -F '.' '{print $1}'`
cores=$5

#--Runnning program
trimmomatic PE -phred33 -threads $cores $r1 $r2 \
        $out1'_qf.fastq.gz' $out1'_qf_unpaired.fastq.gz' \
        $out2'_qf.fastq.gz' $out2'_qf-unpaired.fastq.gz' \
        LEADING:$minq TRAILING:$minq MINLEN:$minl AVGQUAL:$minq


################################################################
# Defaults
# ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 \
# LEADING:3 \
# TRAILING:3 \
# SLIDINGWINDOW:4:15 \
# MINLEN:36

################################################################
# ILLUMINACLIP: Cut adapter and other illumina-specific sequences from the read.
# SLIDINGWINDOW: Performs a sliding window trimming approach. It starts scanning at the 5‟ end and clips the read once the average quality within the window falls below a threshold.
# MAXINFO: An adaptive quality trimmer which balances read length and error rate to maximise the value of each read
# LEADING: Cut bases off the start of a read, if below a threshold quality
# TRAILING: Cut bases off the end of a read, if below a threshold quality
# CROP: Cut the read to a specified length by removing bases from the end
# HEADCROP: Cut the specified number of bases from the start of the read
# MINLEN: Drop the read if it is below a specified length
# AVGQUAL: Drop the read if the average quality is below the specified level
# TOPHRED33: Convert quality scores to Phred-33
# TOPHRED64: Convert quality scores to Phred-64
################################################################
