#!/bin/bash

#--Argument control
if [[ $# -ne 3 ]]
        then
        echo '--------------------------------------------------------------------------------------------------------------'
        echo 'Usage: decontaminate.sh <R1.fastq.gz><R2.fastq.gz><output>'
        echo '--------------------------------------------------------------------------------------------------------------'
        exit
fi

#--Variables
r1=$1
r2=$2
output=$3

if [ ! -d ./human_cds_index ]
then
        gdown --folder https://drive.google.com/drive/folders/1ames4k0NYqKlkxObuGbjJLDh2-UwHVdH
fi

#--Human decontamination
bowtie2 -x human_cds_index/human_cds -1 $r1 -2 $r2 --un-conc-gz ${output}_non_human_R%.fq.gz -S tmp.sam
rm -fr tmp.sam

#--PhiX174 decontamination
wget https://ftp.ncbi.nlm.nih.gov/genomes/refseq/viral/Sinsheimervirus_phiX174/latest_assembly_versions/GCF_000819615.1_ViralProj14015/GCF_000819615.1_ViralProj14015_genomic.fna.gz
gunzip GCF_000819615.1_ViralProj14015_genomic.fna.gz
bowtie2-build GCF_000819615.1_ViralProj14015_genomic.fna phix

# Aligning human decontaminated reads against PhiX174 index
bowtie2 -x phix -1 ${output}_non_human_R1.fq.gz -2 ${output}_non_human_R2.fq.gz --un-conc-gz ${output}_non_human_nonPhiX_R%.fq.gz -S tmp.sam
rm -fr tmp.sam


