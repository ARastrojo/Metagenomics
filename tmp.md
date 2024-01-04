#!/bin/bash


source ~/.bash_profile
conda activate ngs

# Link reads
ln -s /home/metag/Documents/data/viromas/virome_1.tar.gz .
tar -xzf virome_1.tar.gz

# Raw reads quality  assessment
mkdir quality
fastqc virome_1_R1.fastq.gz -o quality
fastqc virome_1_R2.fastq.gz -o quality

# Quality filtering
trimmomatic PE -phred33 virome_1_R1.fastq.gz virome_1_R2.fastq.gz \
    virome_1_R1_qf_paired.fq.gz virome_1_R1_qf_unpaired.fq.gz \
    virome_1_R2_qf_paired.fq.gz virome_1_R2_qf_unpaired.fq.gz \
    SLIDINGWINDOW:4:20 MINLEN:150 LEADING:20 TRAILING:20 AVGQUAL:20

# QF reads quality assessment
fastqc virome_1_R1_qf_paired.fq.gz -o quality
fastqc virome_1_R2_qf_paired.fq.gz -o quality

# Decontaminating human reads
bowtie2 -x ../unit_3/human_cds -1 virome_1_R1_qf_paired.fq.gz -2 virome_1_R2_qf_paired.fq.gz --un-conc-gz virome_1_qf_paired_nonHuman_R%.fq.gz -S tmp.sam

# Decontaminating PhiX174 reads
bowtie2 -x ../unit_3/phix -1 virome_1_qf_paired_nonHuman_R1.fq.gz -2 virome_1_qf_paired_nonHuman_R2.fq.gz --un-conc-gz virome_1_qf_paired_nonHuman_nonPhix_R%.fq.gz -S tmp.sam

# Assembly
spades.py -t 4 --careful -1 virome_1_qf_paired_nonHuman_nonPhix_R1.fq.gz -2 virome_1_qf_paired_nonHuman_nonPhix_R2.fq.gz -o virome_1_careful
spades.py -t 4 --meta    -1 virome_1_qf_paired_nonHuman_nonPhix_R1.fq.gz -2 virome_1_qf_paired_nonHuman_nonPhix_R2.fq.gz -o virome_1_meta
spades.py -t 4 --sc      -1 virome_1_qf_paired_nonHuman_nonPhix_R1.fq.gz -2 virome_1_qf_paired_nonHuman_nonPhix_R2.fq.gz -o virome_1_sc

# Assembly analysis
conda deactivate
conda activate quast
mkdir quast
ln -rs ./virome_1_careful/contigs.fasta   ./quast/virome_1_contigs_careful.fasta
ln -rs ./virome_1_careful/scaffolds.fasta ./quast/virome_1_scaffolds_careful.fasta
ln -rs ./virome_1_meta/contigs.fasta      ./quast/virome_1_contigs_meta.fasta
ln -rs ./virome_1_meta/scaffolds.fasta    ./quast/virome_1_scaffolds_meta.fasta
ln -rs ./virome_1_sc/contigs.fasta        ./quast/virome_1_contigs_sc.fasta
ln -rs ./virome_1_sc/scaffolds.fasta      ./quast/virome_1_scaffolds_sc.fasta
ln -rs ./virome_1_genomes.fasta          ./quast/virome_1_genomes.fasta
cd quast
quast.py virome_1_contigs_careful.fasta virome_1_contigs_meta.fasta virome_1_contigs_sc.fasta virome_1_scaffolds_careful.fasta virome_1_scaffolds_meta.fasta virome_1_scaffolds_sc.fasta -R virome_1_genomes.fasta
conda deactivate

