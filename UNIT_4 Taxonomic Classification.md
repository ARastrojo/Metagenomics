# Taxonomy classification 

## 1. Pre-processing

- Create a folder and obtain reads:

```bash
cd /media/DiscoLocal/BioInformatica/
mkdir unit_4
```

As example, we are going to used the reads of *virome_1* used in _Unit 3_. 
As we have already perform quality filtering and decontamination we only need to copy/link reads files here:

```bash
cd unit_4
ln -rs ../unit_3b/virome_1_qf_paired_nonHuman_nonPhix_R1.fq.gz ./virome_1_qf_R1.fq.gz
ln -rs ../unit_3b/virome_1_qf_paired_nonHuman_nonPhix_R1.fq.gz ./virome_1_qf_R2.fq.gz

# Note that we have "modify" the name of the files in the link, just for convinience
```

> _-r_ option does not exit in mac, take care creating symbolic link in mac with relative path, although it is possible to create, it is better to use absolute paths in mac. 

Addittionaly, we are going to download quality filtered reads from *virome_2* to compare taxonomic classification from both viromes:

```bash
conda activate ngs
gdown https://drive.google.com/uc?id=11xOf45e5aIIKLTc1pEKsUCHpYyC-84NF
gdown https://drive.google.com/uc?id=1TuTyun2dlmUMvsF6N9LK6zAySI3xvqtx

# MD5
# 7c508583dbda80b948b5f88eb879ae16  virome_2_qf_R1.fq.gz
# d1894eec561128bc29e4a3050e0eafaa  virome_2_qf_R2.fq.gz
```

> Take a look to scripts _trimo.sh_ and _decontaminate.sh_ under script folder in github. 

## 2. Taxonomy using [Diamond and MEGAN ](https://currentprotocols.onlinelibrary.wiley.com/doi/10.1002/cpz1.59)

<!--Compare 2 viromes-->

- **Installing DIAMOND**
```bash
conda activate ngs
conda install -c bioconda diamond -y
````

- **Download viral protein database files from [NCBI]( https://ftp.ncbi.nlm.nih.gov/refseq/release/viral/)**
```bash
wget https://ftp.ncbi.nlm.nih.gov/refseq/release/viral/viral.1.protein.faa.gz
gunzip viral.1.protein.faa.gz
```

> How many viral proteins contain the database?

- **Set up the reference database for Diamond**

```
diamond makedb --in viral.1.protein.faa -d viralproteins
```

This will create a binary DIAMOND database file with the name: viralproteins.dmnd

<!--Sometimes this library is required: sudo apt install libnss-db-->

- **Align reads using blastx-like command:**

As we have paired reads, and Diamond cannot handle them, we can run Diamond for each pair and then merge the outputs or we can merge paired reads in a single file and run Diamond just once. 

```bash
# This is just an example, DO NOT RUN
zcat virome_1_qf_R1.fq.gz virome_1_qf_R2.fq.gz > virome_1.fq
diamond blastx -d viralproteins.dmnd -q virome_1.fq -o virome_1_vs_viralprotein.m8

# DIAMOND standard output  
# Total time = 214.286s ~ 4 minutes
# Reported 1458220 pairwise alignments, 1468652 HSPs.  
# 152252 queries aligned.  
```

However, although Diamond running time is not to high (~160k reads takes ~4 minutes ), MEGAN, the program we are going to use for parsing Diamond hits and assign taxonomy to the reads, uses a <u>huge amount of RAM memory</u> and with large dataset many times it gets blocked. To avoid this, we are going to take  a **random subsample** using [seqtk](https://github.com/lh3/seqtk):

```bash
conda install -c bioconda seqtk

# Virome_1
seqtk sample -s 123 virome_1_qf_R1.fq.gz 5000 > virome_1_10k.fq
seqtk sample -s 123 virome_1_qf_R2.fq.gz 5000 >> virome_1_10k.fq

# Virome_2
seqtk sample -s 123 virome_2_qf_R1.fq.gz 5000 > virome_2_10k.fq
seqtk sample -s 123 virome_2_qf_R2.fq.gz 5000 >> virome_2_10k.fq

# Note the ">>" in the second subsample for each virome
```

> Important: *-s 123* is the seed for random number generation, so if we always use the same seed (and same parameters) to extract a subsample for the same file we are going to obtain the same subsample. Using the same seed is important when testing new analysis/pipeline to get reproducible results. [Why subsample? ](https://onestopdataanalysis.com/subsample-paired-fastq-fasta/)

```bash
# Running diamond on both viromes
diamond blastx -d viralproteins.dmnd -q virome_1_10k.fq -o virome_1_10k.m8
diamond blastx -d viralproteins.dmnd -q virome_2_10k.fq -o virome_2_10k.m8
```

Take a look to the output file:

```bash
head virome_1_10k.m8
```

| 1                   | 2              | 3    | 4  | 5  | 6 | 7  | 8   | 9   | 10  | 11       | 12    |
|---------------------|----------------|------|----|----|---|----|-----|-----|-----|----------|-------|
| NC_002198.2_704_1/1 | NP_054687.1    | 98.1 | 54 | 1  | 0 | 80 | 241 | 235 | 288 | 5.80E-25 | 114   |
| NC_002198.2_704_1/1 | NP_840025.2    | 90.7 | 54 | 5  | 0 | 80 | 241 | 236 | 289 | 2.40E-23 | 108.6 |
| NC_002198.2_704_1/1 | YP_003029840.1 | 75.9 | 54 | 13 | 0 | 80 | 241 | 230 | 283 | 3.60E-19 | 94.7  |
| NC_002198.2_704_1/1 | NP_563611.1    | 56.6 | 53 | 23 | 0 | 80 | 238 | 229 | 281 | 3.10E-10 | 65.1  |
| NC_002198.2_704_1/1 | NP_620480.1    | 56   | 50 | 22 | 0 | 83 | 232 | 227 | 276 | 6.90E-10 | 63.9  |
| NC_002198.2_704_1/1 | NP_620487.1    | 56   | 50 | 22 | 0 | 83 | 232 | 227 | 276 | 6.90E-10 | 63.9  |
| NC_002198.2_704_1/1 | NP_840098.1    | 56   | 50 | 22 | 0 | 83 | 232 | 227 | 276 | 6.90E-10 | 63.9  |
| NC_002198.2_704_1/1 | YP_010086857.1 | 56   | 50 | 22 | 0 | 83 | 232 | 227 | 276 | 6.90E-10 | 63.9  |
| NC_002198.2_704_1/1 | NP_114364.2    | 55.1 | 49 | 22 | 0 | 86 | 232 | 228 | 276 | 3.40E-09 | 61.6  |
| NC_002198.2_704_1/1 | YP_001949738.1 | 48.1 | 52 | 27 | 0 | 83 | 238 | 249 | 300 | 5.10E-05 | 47.8  |
| NC_002198.2_704_1/1 | YP_001931932.1 | 39.2 | 51 | 31 | 0 | 80 | 232 | 231 | 281 | 9.60E-04 | 43.5  |
| NC_026648.1_621_0/1 | YP_009126928.1 | 100  | 81 | 0  | 0 | 3  | 245 | 47  | 127 | 3.20E-39 | 161.4 |


> This is the meaning of the 12 columns:  
> 1.-qseqid means Query Seq-id  
> 2.-sseqid means Subject Seq-id  
> 3.-pident means Percentage of identical matches  
> 4.-length means Alignment length  
> 5.-mismatch means Number of mismatches  
> 6.-gapopen means Number of gap openings  
> 7.-qstart means Start of alignment in query  
> 8.-qend means End of alignment in query  
> 9.-sstart means Start of alignment in subject  
> 10.-send means End of alignment in subject  
> 11.-evalue means Expect value  
> 12.-bitscore means Bit score  

We can take the accession number of one of the hits (column 2) and paste in NCBI and look at the taxonomy of this sequences. Then you can repeat this step one by one several thousand times to have a taxonomic profile of these metagenomes. Alternatively, you can use a specific program which take the comparison output of Blast or Diamond and gives you back the result for all the matches together in a graph (see the next step of the tutorial).
 
- **Parsing BLAST/DIAMOND tabular outputs with MEGAN6**

MEGAN6 analyses the taxonomic content of a set of DNA reads aligned with a NCBI dataset and assigns reads into a taxonomy tree.

MEGAN6 can be installed as GUI-based in Windows/Mac or can be installed through conda (in fact, MEGAN6 is nos available through conda in mac):

```bash
conda activate ngs
conda install -c bioconda megan -y
```

Additionally, we need to download the mapping file [megan-map-Feb2022-ue.db.zip](https://software-ab.cs.uni-tuebingen.de/download/megan6/megan-map-Feb2022-ue.db.zip) to provide taxonomic information of the database to MEGAN. 

<!--https://software-ab.cs.uni-tuebingen.de/download/megan6/megan-map-Feb2022.db.zip-->

```bash
wget https://software-ab.cs.uni-tuebingen.de/download/megan6/megan-map-Feb2022-ue.db.zip

# Unzip mapping file (this will take a while...)
unzip megan-map-Feb2022-ue.db.zip
```

To run MEGAN write MEGAN a in terminal window (from _ngs_ environment).

- **Import Diamond/blast output files (ending in .m8.) to the MEGAN6 graphical user interface**

Click File --> Import From Blast

![ImportBlast](https://github.com/ARastrojo/Metagenomics/blob/9c692607b39e7a8cbfd7b839e261d74c67034cb9/images/megan_import.png)

To specify the BLAST output file, click on the folder at the right and in the new window (choose “All files” and select the diamond blast tabular file ending in .m8). 

Choose the <u>BlastTab format</u> and the <u>Blastx mode</u>.

Load also the original reads (in fastq format) used for the Blastx (sometimes MEGAN detect automatically the fastq read file from the folder).

Click on Next and Load the Accession mapping file (unzipped). 

![MappingFile](https://github.com/ARastrojo/Metagenomics/blob/9c692607b39e7a8cbfd7b839e261d74c67034cb9/images/megan_mapping_file.png)

Then click on “Apply” (and wait.....)

> Although we have reduce the number of input reads to dicrease memory consumption, in the virtual machine (4 Gb of RAM) the analysis can get blocked or sometimes the program suddenly gets close...

**Results: Family level and with the number of reads**

![megan_results](https://github.com/ARastrojo/Metagenomics/blob/9dbe55d2e92d8a92b4cdcd292077fc320a2c809b/images/megan_results.png)

Once you have the graphical overview of the taxomomic composition of the reads from the example virome we can explore MEGAN6 options (optinal):
1. Change the taxonomic level in “Rank” to Genera, Species or Family (Tree > Rank).
2. Expand or collapse the tree or change the tree format
3. In the Tree tab, choose “Show Number of Summarized”
4. We can copy data by clicking on Options/List Summary, paste de data in LibreOffice or Excel using “:” to divide data in columns.
5. Check the alignments from a specific taxon by clicking on that with the right
mouse button. Select “Inspect” option.
6. We can change LCA parameters in Options and increase the minimal score to 60 and reduce the max e-value allow to 10<sup>-10</sup> and the min complexity to 0.5 in order to reduce false positive alignments.


> MEGAN results are stored in a file called *virome_1_10k.rma6* created in the same folder than input files.

- **Repeat the process for virome 2**

![megan_virome_2](https://github.com/ARastrojo/Metagenomics/blob/1473360499fcdc629f34a824b29bbb976223ef6a/images/megan_results_2.png)

- **Compare viromes with MEGAN**

Now, we can compare the results from the taxonomic classification of both viromes. Close previous MEGAN windows, and click in "no" when MEGAN ask you to quit the program. 

Now click in _File --> Compare_

In the new windows import both *.rma6* files. Then choose "Use Absolute counts" and disable "Ignore all unassigned reads". 

> Usually we are going to use the default options "Use Normalized count", to reduce differences cause by different sequencing depth, however, we have subsample both viromes to the same depth and to some extent we have already normalized the samples. 

![megan_compare](https://github.com/ARastrojo/Metagenomics/blob/65aa0988d0817c2470482b463d9569adcd1d1e1c/images/megan_compare.png)

- **Comparison results**

![megan_compare_results](https://github.com/ARastrojo/Metagenomics/blob/65aa0988d0817c2470482b463d9569adcd1d1e1c/images/megan_compare_2.png)

We can obtain a general view of the viromes. For instance, in virome 2 there are many bacteriophages (viruses than infect bacteria) from families _Myoviridae_, _Podoviridae_ and _Siphoviridae_ and viruses from the _Geminiviridae family, while in virome 1 in enriched in RNA virures (mainly unclassified). 


<!--

## Taxonomy using [Kraken2]()

Can we compare 2 viromes with Kraken2 (Pavian?)



## 4. HOMEWORK

Follow the workflow of this tutorial for the taxonomic binning of the virome reads and contigs used as homework in the unit_3.

> Reads from unit_3 homework are paired_end reads. To perform this task you can do it in several ways; joining all decontaminated and QF reads and then run DIAMOND or run DIAMOND using both files and then join DIAMOND outputs, etc..

Write a brief summary describing the bioinformatic pipeline you have followed (trimming, decontamination, improve in quality, number of reads remove in each step, etc.) and the most relevant results (two figures maximun) with the taxonomy assessment of the virome at family level.

**Optional: run the same analysis but using the assembled contigs and try to compare the results using MEGAN (File/Compare and load both rma6 files created while making the individual analysis).

Deadline: 20th May.

-->