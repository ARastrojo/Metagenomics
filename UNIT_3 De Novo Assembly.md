# _De Novo_ Assembly tutorial

To learn the basis of _de novo_ assembly we are going to use a small dataset to reduce computational requirements and to speed up the  process. Specifically, we are going to use a subset (50k paired reads) from the reads obtained in _Ectromelia virus_ genome sequencing. Therefore, in our example dataset we should expect a single genome, and hopefully a single contig/scaffold. 

## 1. Pre-processing

### 1.1. Download dataset

Download ECTV_reads.zip file from Moodle/Unit_3 or use this [link](https://dauam-my.sharepoint.com/:u:/g/personal/alberto_rastrojo_uam_es/EQVJCMSsshpPgNvSkDa1RSsBLcHijyDq3wpJSHZr-uCWLQ?e=LkuTYX):

```bash
mkdir -p /home/${USER}/Documents/unit_3
mv /home/${USER}/Downloads/ECTV_reads.zip /home/${USER}/Documents/unit_3
cd /home/${USER}/Documents/unit_3
unzip ECTV_reads.zip
```

### 1.2 Checking file integrity

It is very recomended to check the integrity of the files we have just downloaded. [MD5sum](https://en.wikipedia.org/wiki/Md5sum) and other more recent programs ([SHA1sum](https://en.wikipedia.org/wiki/Sha1sum)) are algorithms that ["transform"](https://en.wikipedia.org/wiki/Cryptographic_hash_function) the content of file to a short chain of  characters (hashes). Hashes do not change unless the content of the files were modified (the name of the file is not relevant). Therefore, it is very common that databases or sequencing facilities provide MD5 hashes to the users to allow for integrity checking. 

In the table below you can find the MD5 hashes of ECTV reads files:

| File | MD5 |
| - | - |
| ECTV_R1.fastq |fa3e37e336213d01d927df2a4f0aea12 |
| ECTV_R2.fastq |8a569dc04acc87067d33d3d58b26dd6d |

Execute the following commands to calculate MD5 hashes of the local files:
```bash
md5sum ECTV_R1.fastq 
md5sum ECTV_R1.fastq 
````

Or just:

```bash
md5sum *.fastq
```

Finally, just inspect the hashes by eye to check for any change. Usually, if files were broken for whatever reason, the md5 hash is completely different and just looking at the last 5-6 digits is going to show us if something went wrong. 

### 1.3 Counting the number of reads

Both file should have the same number of reads (Illumina paried-end reads). Is a good practice to check the number of reads in both files. Despite having checked the MD5 hashes, sometimes, database uploaded files are wrong (submitter may have uploaded truncated files rather than the original files). Additionally, knowing the number of reads would be useful for basis quality metrics (assembled/mapped reads or quality pass reads). 

Most sequencing reads are in [FASTQ format](https://en.wikipedia.org/wiki/FASTQ_format). Each sequence in FASTQ format in represented in four consecutive lines:

```
@HWUSI-EAS1752R:23:FC62KHPAAXX:6:3:3542:1008 1:N:0:GCCAAT
GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT
+
!''*((((***+))%%%++)(%%%%).1***-+*''))**55CCF>>>>>>CCCCCCC65
```

- First line, is the sequence name begining with "@". The name of the sequence usually contains information of the intrument, the number of run, the lane, etc.
- Second line is the sequence itselft.
- Third line is for comments (usually empty)
- Last line is the quality of the sequence code using [Phred scale](https://en.wikipedia.org/wiki/Phred_quality_score) (curently most sequencing platforms used Phred+33 scale)

So, the easy way of counting the number of reads in a file is using _wc_ linux command (_word count_):

```bash
wc -l ECTV_R1.fastq
wc -l ECTV_R2.fastq
```

_-l_ option is applied to count the number of lines. However, we have to divide by 4 to get the number of reads. To avoid this, we can apply some piping:

```bash
wc -l ECTV_R1.fastq | awk '{print $1/4}'
wc -l ECTV_R2.fastq | awk '{print $1/4}'
```

Or using a _for_ loop:

```bash
for file in *.fastq;
do
reads=`wc -l ${file} | awk '{print $1/4}'`
echo $file $reads
done
```

### 1.4. Check sequence quality with “fastqc”. 

This tool is already installed in your virtual machines (or you can use _conda_ to install it in your computer).

```bash
mkdir ECTV_Quality
fastqc ECTV_R1.fastq -o ECTV_Quality/
fastqc ECTV_R2.fastq -o ECTV_Quality/
```
We can use _-t_ options to increase the number of threads the program will use (not needed in this small dataset).

Open the html files to get information about the number of sequences, the length distribution, the %CGs content, the average quality, etc. 

**R1 quality plot**

![r1_quality](https://user-images.githubusercontent.com/13121779/162767027-92e2adeb-bec8-4571-8257-3196cd7de944.png)

**R2 quality plot**

![r2_quality](https://user-images.githubusercontent.com/13121779/162767078-d14e19d6-40a9-498a-828d-f3b65ebad31e.png)

### 1.5. Trimming of poor-quality ends and short sequences (Trimmomatic)

Take a look to [Trimmomatic manual](http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/TrimmomaticManual_V0.32.pdf) or use _trimmomatic -h_. 

```bash
trimmomatic PE -phred33 ECTV_R1.fastq ECTV_R2.fastq ECTV_R1_qf_paired.fq ECTV_R1_qf_unpaired.fq ECTV_R2_qf_paired.fq ECTV_R2_qf_unpaired.fq SLIDINGWINDOW:4:20 MINLEN:70
```
**Trimmomatic defaults parameters:** LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36

>Trimmomatic output:
>
>Multiple cores found: Using 2 threads
>
>Input Read Pairs: 50000 Both Surviving: 41996 (83.99%) Forward Only Surviving: 4107 (8.21%) Reverse Only Surviving: 1791 (3.58%) Dropped: 2106 (4.21%)
>
>TrimmomaticPE: Completed successfully

Let's take a look to some parameters:
- **SLIDINGWINDOW:** Performs a sliding window trimming approach. It starts scanning at the 5‟ end and clips the read once the average quality within the window falls below a threshold. 

- **MINLEN**: Drop the read if it is below a specified length. 

What do you think about the SLIDINGWINDOW clipping strategy?
Why do you think we have use 70 as MINLEN? How long are ECTV raw reads?

Now check the number of high-quality paired-end reads selected in this pre-processing step and compare their quality profile with that of the input:

```bash
mkdir ECTV_QF_Quality
fastqc ECTV_R1_qf_paired.fq -o ECTV_QF_Quality
fastqc ECTV_R2_qf_paired.fq -o ECTV_QF_Quality
```
**ECTV_R1_qf_paired quality plot**

![per_base_quality](https://user-images.githubusercontent.com/13121779/162787145-78f469bd-04fc-43c0-8ca6-2e4bc341462c.png)

**ECTV_R1_qf_paired quality plot**

![per_base_quality](https://user-images.githubusercontent.com/13121779/162787227-5bc4471d-100e-4737-b020-396f646be7b1.png)

General quality has improve specially at the end of the reads where quality was lower in raw sequences. 

> **NOTE:** We can count quality filtered reads by using _wc_ but Trimmomatic's output already have this information. However, it is important to write down this data to evaluate the general quality as the percentage of quality filtered reads.

### 1.6 Removal of reads aligning to the human and phiX174 genomes (Bowtie2)

phiX174 was the first genome to be sequence ([Sanger, F., Air, G., Barrell, B. et al. Nucleotide sequence of bacteriophage φX174 DNA. Nature 265, 687–695 (1977)](https://doi.org/10.1038/265687a0)). Since that, the viral genome is included as an spike by Illumina kits to control quality of the sequencing process and some contaminating reads could be left. 

In the other hand, human contamination is also very frequent, as humans prepare and manipulate the samples before being sequenced. In some cases, the genome of other organisms, such as mouse or monckey, should be used instead of human, depending on the experimental set. Imaging, for instance, that we are sequencing the genome of a virus grown in VERO cells (derived from monkey kidney fibroblast). In that case we should remove all reads mapping to the monkey genome that could be present in our raw data as a contamination. 

To perform short read alignment we are going to use [Bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml). There are other popular aligners such as [BWA](http://bio-bwa.sourceforge.net/), but Bowtie2 parameters are easy to understand and modify. Specially, as we are not really interested in aligned reads, those that mapped to the human or phiX174 genomes, by using Bowtie2 we have an option to extract not aligned reads. We can also extract unaligned reads from BWA alignment, but is not an straight way. 

Before preforming the alignment, Bowtie2 requires the preparation of an index containing the reference sequences to align against, in our case the human and phiX174 genomes. We can perform this decontamination process in two steps, by first removing human reads and then phiX174 reads. Pre-built human genome indexes can be downloaded from Bowtie2 webpage. However, as human genome is too big to run the alignment is a short time, we are going to use a smaller human reference sequence containing all coding sequence instead of the whole genome sequence. 

**Download data files**

The file containing all human coding sequences is already in the VM (~Documents/unit_3/GCF_000001405.39_GRCh38.p13_cds_from_genomic.fna), while phiX174 viral genome can be downloaded from Moodle (unit_3/phiX174.fasta).

GCF_000001405.39_GRCh38.p13_cds_from_genomic.fna is a multifasta file with the sequence of more than 120000 human coding sequences. These sequences contain line breaks every 60 nucleotides, while phiX174 sequence is broken every 70 nucleotides. Mixing both different format will cause problems during Bowtie2 index contructions. The easiest way to avoid this problem is to remove line breaks in the sequences:

```bash
awk '{if(/^>/) printf("\n%s\n",$0); else printf("%s",$0)} END {printf("\n")}' < GCF_000001405.39_GRCh38.p13_cds_from_genomic.fna > HumanGenome_ONELINE.fasta
awk '{if(/^>/) printf("\n%s\n",$0); else printf("%s",$0)} END {printf("\n")}' < phiX174.fasta > phiX174_genome_ONELINE.fasta
```

>Or you can write a small python script to do it ([refasta.py](https://github.com/ARastrojo/Metagenomics/blob/main/refasta.py))

Now, we are going to join both files:

```bash
cat HumanGenome_ONELINE.fasta phiX174_genome_ONELINE.fasta > Human-phiX174.fasta
```
Finally, we are ready to build Bowtie2 index:
```bash
bowtie2-build Human-phiX174.fasta human-phix174
```
>However, as the time to produce the index is also a little bit long (>30 minutes), we have built the index for you (~/Documents/unit_3/)

And align high quality ECTV reads against this index:

```bash
bowtie2 -x human-phix174 -1 ECTV_R1_qf_paired.fq -2 ECTV_R2_qf_paired.fq --un-conc ECTV_clean.fq -S tmp.sam
```

> _tmp.sam_ contains the aligned reads that we are not interested in, so we can remove this file. 
> 
> ECTV_clean.1.fq and ECTV_clean.2.fq contain not aligned reads, which are the target sequences.

Now we can count the clean reads:

```bash
wc -l *clean.* | awk '{print $1/4}'
```

> **NOTE:** Write down the remaining number of reads after decontamination.

## 2. De novo assembly with Spades

We are going to use [SPAdes](https://github.com/ablab/spades), one of the most popular _de Bruijn_ graph _de novo_ assemblers. Take a look to the [paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3342519/) describing the program.

SPAdes program has been already installed in the Virtual Machine. This assembler has specific assembly protocols for different experimental set (_--sc_, single cell data; _--meta_, metagenomics data; --isolate, a single genome sequencing or _--rna_, for RNA-seq) and sequencing platforms (Illumina, IonTorrent, Nanopore or PacBio). The program does not only make de novo assembly but also run an error correction tool for Illumina sequences. If we run the program with the flag --careful, SPAdes will also run MismatchCorrector, a post processing tool which uses BWA aligner. However, this flag is only recommended for assembly of small genomes and is not compatible with some other options such as single cell (_--sc_) or metagenomics (_--meta_).

Another important option is _-k_ flag with which we can define the kmer length to use in the assembly. If we do not provide a list of _kmers_, the program will select automatically three of them based on average reads length and perfoms a combined assembly. Nowadays, with this modern assembler it is better to allow the program to choose the best _kmers_, but at the beginning of the genomic era researches had to choose them by making multiple assemblies. As a general rule, _kmers_ have to be smaller than average read length and must be odd and less than 128 (althougth other assemblers can use longer _kmer_ sizes). 

### 2.1. Runing SPAdes 

As our dataset come from a single viral genome, the most adequate protocol should be _--isolate_, however in my experience, default assembly protocol with _--careful_ flag give us better results (based mainly on contig length). To check this, we are going to test both procotols:

```bash
spades.py --isolate -t 2 -1 ECTV_clean.1.fq -2 ECTV_clean.2.fq -o ECTV_isolate
spades.py --careful -t 2 -1 ECTV_clean.1.fq -2 ECTV_clean.2.fq -o ECTV_careful

```

### 2.2. Check the number of contigs and scaffolds:

We can take a look to the number of contigs/scaffold we have obtained from both assemblies:

```bash
grep -c '>' ./ECTV_isolate/*.fasta
```
>./ECTV_isolate/before_rr.fasta:22  
>./ECTV_isolate/contigs.fasta:11  
>./ECTV_isolate/scaffolds.fasta:9  

```bash
grep -c '>' ./ECTV_careful/*.fasta
```
>./ECTV_careful/before_rr.fasta:20  
>./ECTV_careful/contigs.fasta:8  
>./ECTV_careful/scaffolds.fasta:7  

_before_rr.fasta_ is just a intermediate file from SPAdes, so we do not care about it. 

Looking just at the number of contigs/scaffolds it seems that _--careful_ option is better, but the number of contigs/scaffolds is not everything. Let's look at the lengths and coverage of the contigs (fasta headers):

```bash
grep '>' -m 5 ./ECTV_careful/*.fasta
grep '>' -m 5 ./ECTV_isolate/*.fasta
```

| Isolate | Careful |
| - | - |
| >NODE_1_length_61911_cov_7.828683 | >NODE_1_length_61911_cov_7.996460 |
| >NODE_2_length_36053_cov_7.188705 | |
| | >NODE_2_length_61252_cov_7.070559 |
| >NODE_3_length_30550_cov_10.405148 | >NODE_3_length_30550_cov_10.598754 |
| >NODE_4_length_29611_cov_8.192245 | >NODE_4_length_29611_cov_8.358201 |
| >NODE_5_length_25623_cov_6.437265 | |
| >NODE_6_length_13405_cov_7.176180 | >NODE_5_length_13405_cov_7.334082  |
| >NODE_7_length_261_cov_1.072816 | |
| >NODE_8_length_228_cov_1.942197 | |
| >NODE_9_length_227_cov_0.610465 | >NODE_6_length_227_cov_0.610465 |
| >NODE_10_length_102_cov_4.340426 | >NODE_7_length_102_cov_4.595745 |
| >NODE_11_length_90_cov_11.514286 | >NODE_8_length_90_cov_11.685714 |

We can do the same for the scaffolds:

```bash
grep '>' ./ECTV_careful/scaffolds.fasta
grep '>' ./ECTV_isolate/scaffolds.fasta
```

| Isolate | Careful |
| - | - |
| >NODE_1_length_92471_cov_8.673347 | >NODE_1_length_92471_cov_8.849528 |
| >NODE_2_length_36053_cov_7.188705 | |
| | >NODE_2_length_61252_cov_7.070559 |
| >NODE_3_length_29611_cov_8.192245 | >NODE_3_length_29611_cov_8.358201 |
| >NODE_4_length_25623_cov_6.437265 | 
| >NODE_5_length_13643_cov_7.075213 | >NODE_4_length_13405_cov_7.334082 |
| >NODE_6_length_261_cov_1.072816 | |
| >NODE_7_length_227_cov_0.610465 | >NODE_5_length_227_cov_0.610465 |
| >NODE_8_length_102_cov_4.340426 | >NODE_6_length_102_cov_4.595745 |
| >NODE_9_length_90_cov_11.514286 | >NODE_7_length_90_cov_11.685714 |

OPTIONAL: I have writen an small Python script ([contigstats.py](https://github.com/ARastrojo/Metagenomics/blob/main/contigstats.py)) that can be use to obtain a quick view of the assembly stats. It calculates the number of sequences in a fasta file, the minimun/mean/maximun sequence length and [N50 parameter](https://en.wikipedia.org/wiki/N50,_L50,_and_related_statistics) (_Wikipedia: "Given a set of contigs, the N50 is defined as the sequence length of the shortest contig at 50% of the total genome length."_).

```bash
python contigstats.py ECTV_*/*.fasta
```

| sample | contigs | min | max | mean | n50 | bases | non_standard_bases |
| - | - | - | - | - | - | - | - |
| ECTV_careful/contigs.fasta | 8 | 90 | 61911 | 24644 | 61252 | 197148 | 0 |
| ECTV_careful/scaffolds.fasta | 7 | 90 | 92471 | 28165 | 61252 | 197158 | 10 |
| ECTV_default/contigs.fasta | 8 | 90 | 61911 | 24644 | 61252 | 197148 | 0 |
| ECTV_default/scaffolds.fasta | 7 | 90 | 92471 | 28165 | 61252 | 197158 | 10 |
| ECTV_isolate/contigs.fasta | 11 | 90 | 61911 | 18006 | 30550 | 198061 | 0 |
| ECTV_isolate/scaffolds.fasta | 9 | 90 | 92471 | 22009 | 36053 | 198081 | 20 |
| ECTV_sc/contigs.fasta | 12 | 79 | 92446 | 16567 | 61624 | 198808 | 0 |
| ECTV_sc/scaffolds.fasta | 9 | 79 | 92877 | 22102 | 75358 | 198919 | 111 |

> NOTE: I have remove _before_rr.fasta_ data from the table for simplicity.

## 3. Quast comparison of assembly strategies. 

A better and more complete way of making assemblies comparison is by using dedicated tools such [QUAST] (http://quast.sourceforge.net/quast.html). This tool provides different metrics of comparison among assemblies in pdf or html files and it can also be used [online] (http://cab.cc.spbu.ru/quast/). 

> **Advice** (This can be complete ignored): It is always better to use existing programs and/or tools, supported by publications, than writing your own (there is no need to reinvent the wheel). However, if your project goal is to develop a new algorithm/program, of course it is worth, but if your are working in the sequencing of a new species genome, why losing the time building a new assembler? This could be applied to every program/script... Moreover, reviewers are very picky with the use of _in house_ scripts/programs. 

> **IMPORTANT**: in my VM, that theoretically is identical to yours, QUAST is not installed. Therefore, we have to install it, and in the way I will show you an easy way to manage custom software (outsize of conda).

```bash
cd /home/bgm/
mkdir software
cd software # This folder will store download programs
wget https://downloads.sourceforge.net/project/quast/quast-5.0.2.tar.gz
tar -xzf quast-5.0.2.tar.gz
rm quast-5.0.2.tar.gz
cd quast-5.0.2
python setup.py install # for mac
cd /home/bgm/
mkdir bin
cd bin # This folder will store symbolic links to program executables
ln -s /home/bgm/software/quast-5.0.2/quast.py quast
# edit /home/bgm/.bashrc with _vim_ or _nano_ and add the following line
export PATH=/home/bgm/bin/:$PATH
# This way, all executable that you link in the bin folder will be in the system path
```
Now that we have QUAST, we must have all contigs/scaffolds from the different assemblies in the same folder, but instead of copying the data, to reduce redundancy and save a little bit of disk space, we are going to make use of symbolic links. 

> NOTE: saving a disk space is irrelevant in this case, but when you are working in a real metagenomic or other sequencing projects could be an important issue.

```bash
cd /home/bgm/Documents/unit_3/
mkdir quast
ln -rs ./ECTV_careful/contigs.fasta ./quast/contigs_careful.fasta 
ln -rs ./ECTV_careful/scaffolds.fasta ./quast/scaffolds_careful.fasta 
ln -rs ./ECTV_isolate/contigs.fasta ./quast/contigs_isolate.fasta 
ln -rs ./ECTV_isolate/scaffolds.fasta ./quast/scaffolds_isolate.fasta 
```
Additionally, in this single genome sequencing example we have a reference genome to compare our assemblies with (This is not possible for metagenomes). You can download the reference genome from Moodle (Unit 3/ECTV_reference_genome.fasta).

```bash
quast contigs* scaffolds* -R ECTV_reference_genome.fasta
```

> **IMPORTANT**: In my VM, there was an error when running QUAST (_"AttributeError: module 'cgi' has no attribute 'escape'"_). So I did what a good bioinformaticians must do... Copy and paste the error in google, :). To solver the problem we should modify one of the QUAST script by replacing the use of _cgi_ library for the _html_ one. To do that follow the next commands:

```bash
# Open a new terminal window/tab
cd /home/bgm/software/quast-5.0.2/quast_libs/site_packages/jsontemplate
# Always make a copy of the file you are going to modify
cp jsontemplate.py jsontemplate_original.py
sed s/cgi/html/g jsontemplate_original.py > jsontemplate.py
```

Take a look to the report.pdf/report.html (also report.txt):

![Cummulative length](https://user-images.githubusercontent.com/13121779/163284268-3b69abd3-dfe4-4ffc-9350-beb36f96f415.png)

**Assembly stats**

![Genome stats Screenshot](https://user-images.githubusercontent.com/13121779/163284470-d08f2ff8-4055-4dfe-9bad-09c036259e5e.png)

## 4. Homework

Repeat all the steps with a viral metagenome from a human saliva sample (Virome.zip in Unit 3 of Moodle). Compare different _de novo assemblies_ options (try _--meta--) or different _kmer_ values. You must perform at least 3 different assemblies. Write a brief summary describing the bioinformatic pipeline you have followed (trimming, decontamination, improve in quality, number of reads remove in each step, etc.). Compare different _de novo assemblies_ with QUAST and choose the best based on the obtained metrics (smaller number of contigs, higher N50, smaller L50, longest total assembly length, etc.). 

> NOTE: In the quality filtering step, modify the MINLEN argument considering the original read length. Consider that reads with a minimum of 50% of the average original size are ok for subsequent analyses.

> NOTE: Importantly, you do not have a reference genome for a metagenome.

| File name       | MD5                              |
|-----------------|----------------------------------|
| virome_R1.fastq | cd891dfc865f01c8f3923edd55dacde5 |
| virome_R2.fastq | 28f0d0ace9fb45af8b2595cbc78fa2bd |

> IMPORTANT: SPAdes uses a lot of RAM memory for the assembly and our the virtual machines only have 4 Gb of RAM. To avoid SPAdes to crash while trying different assemblies to should reduce de number on threads used by de assembler (-t 2) and the available amount of memory that SPAdes can used (-m 3).  

```bash
spades.py -t 2 -m 3 -1 R1.fastq -2 R2.fastq -o output_folder
```


Submit this document as a task to Moodle/Unit3 before 20th May.
