## Taxonomy classification using DIAMONG+MEGAN

## 1. Pre-processing

### 1.1. Create a folder in /home/bgm/Documents/:

```bash
mkdir -p /home/${USER}/Documents/unit_4
cd /home/${USER}/Documents/unit_4
```
Download file Virome1.zip (from Moodle/Unit_4) and unzip it into Unit_4 folder.

### 1.2. Perform quality filtering and decontamination as in Unit_3

Here the example data (Virome1.fq) is a single-end read file, so commands are slightly different. 

```
#--FASTQ quality assessment
mkdir Virome1_fastqc
fastqc Virome1.fq -o Virome1_fastqc
#--Trimmomatic quality filtering
trimmomatic SE -phred33 Virome1.fq Virome1_QF.fq SLIDINGWINDOW:5:20 MINLEN:150
#--FASTQ quality assessment
mkdir Virome1_QF_fastqc
fastqc Virome1_QF.fq -o Virome1_QF_fastqc
#--Decontamination
for f in /home/bgm/Documents/unit_3/*bt2; do ln -s $f .; done
bowtie2 -x human-phix174 -q Virome1_QF.fq --un Virome1_QF_clean.fq -S tmp.sam
```

## 2.  Alignment of decontaminated high-quality reads with a viral protein database

### 2.1. Download RefSeq viral proteins available at NCBI and prepare the database for Diamond.

Download viral protein database files from NCBI: https://ftp.ncbi.nlm.nih.gov/refseq/release/viral/
* viral.1.protein.faa.gz
* viral.2.protein.faa.gz
* viral.3.protein.faa.gz
* viral.4.protein.faa.gz


![REFSEQ_VIRAL_SEQUENCES](https://user-images.githubusercontent.com/13121779/165115449-6a8145df-7c4c-489e-9c86-4e2af1b0aee3.png)


Move the files to Documentos/unit_4, extract the fasta files with “gunzip” and joined them into a single file:

```bash
mv /home/${USER}/Downloads/viral.*.protein.faa.gz /home/${USER}/Documents/unit_4
gunzip viral.*.protein.faa.gz
cat viral.*.protein.faa > viral.protein.faa
grep -c ">" *faa
```

### 2.2. Set up the reference database for Diamond

```
diamond makedb --in viral.protein.faa -d viralproteins
```

This will create a binary DIAMOND database file with the name: viralproteins.dmnd

<!--Sometimes this library is required: sudo apt install libnss-db-->

### 2.3. Then proceed with the alignment task using the blastx command:

```
diamond blastx -d viralproteins.dmnd -q Virome1_QF_clean.fq -o Virome1_QF_clean_vs_viralprotein.m8
```

> DIAMOND standard output
> Total time = 8.469s  
> Reported 23088 pairwise alignments, 23088 HSPs.  
> 5160 queries aligned.  

Take a look to the output file:

```
head Virome1_QF_clean_vs_viralprotein.m8
```

| 1      | 2              | 3     | 4   | 5 | 6 | 7   | 8   | 9   | 10  | 11      | 12    |
|--------|----------------|-------|-----|---|---|-----|-----|-----|-----|---------|-------|
| O-:1:1 | YP_009272703.1 | 100.0 | 62  | 0 | 0 | 187 | 2   | 31  | 92  | 1.7e-26 | 118.6 |
| O-:2:2 | YP_009272704.1 | 100.0 | 79  | 0 | 0 | 2   | 238 | 446 | 524 | 4.4e-39 | 161.4 |
| O-:2:2 | YP_009272706.1 | 100.0 | 79  | 0 | 0 | 2   | 238 | 268 | 346 | 4.4e-39 | 161.4 |
| O-:4:4 | YP_009272700.1 | 100.0 | 65  | 0 | 0 | 3   | 197 | 320 | 384 | 2.5e-33 | 141.4 |
| O-:6:6 | YP_009272699.1 | 100.0 | 50  | 0 | 0 | 3   | 152 | 21  | 70  | 1.4e-22 | 106.3 |
| O-:6:6 | YP_009272700.1 | 100.0 | 46  | 0 | 0 | 157 | 294 | 1   | 46  | 1.3e-17 | 89.7  |
| O-:7:7 | YP_009272699.1 | 100.0 | 61  | 0 | 0 | 184 | 2   | 1   | 61  | 1.1e-31 | 136.3 |
| O-:7:7 | YP_009272698.1 | 92.6  | 27  | 2 | 0 | 254 | 174 | 26  | 52  | 7.1e-07 | 53.9  |
| O-:8:8 | YP_009272700.1 | 100.0 | 113 | 0 | 0 | 3   | 341 | 62  | 174 | 2.0e-57 | 222.2 |

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
 
## 3. Parsing BLAST/DIAMOND tabular outputs with MEGAN6

MEGAN6 analyses the taxonomic content of a set of DNA reads aligned with a NCBI dataset and assigns reads into a taxonomy tree.

Additionally, we need to download the mapping file [prot_acc2tax-Jul2019X1.abin.zip](https://software-ab.informatik.uni-tuebingen.de/download/megan6/old.html) to provided taxonomic information of the database to MEGAN. Unzip mapping file (this will take a while).

To run MEGAN write MEGAN a in terminal window

### 3.1. Import Diamond/blast output files (ending in .m8.) to the MEGAN6 graphical user interface:

Click File --> Import From Blast

![ImportBlast](https://user-images.githubusercontent.com/13121779/165252122-9cbca60a-c9c9-4764-aef7-7df5332c6ea0.png)

To specify the BLAST output file, click on the folder at the right and in the new window (choose “All files” and select the
diamond blast tabular file ending in .m8). 

Choose the BlastTab format and the Blastx mode.

Load also the original reads (in fastq format) used for the Blastx.

Click on Next and Load the Accession mapping file (unzipped). 

![MappingFile](https://user-images.githubusercontent.com/13121779/165117918-aaf57afc-a942-4fec-8c94-53c88fe60243.png)

Then click on “Apply”


**Results**

![megan1](https://user-images.githubusercontent.com/13121779/165253205-f54ebf09-09b1-4461-8f32-74be2af90aaa.png)


Once you have the graphical overview of the taxomomic composition of the reads from the example virome we can explore MEGAN6 options:
1. Change the taxonomic level in “Rank” to Genera, Species or Family (Tree > Rank).
2. Expand or collapse the tree or change the tree format
3. In the Tree tab, choose “Show Number of Summarized”
4. We can copy data by clicking on Options/List Summary, paste de data in LibreOffice or Excel using “:” to divide data in columns.
5. Check the alignments from a specific taxon by clicking on that with the right
mouse button. Select “Inspect” option.
6. We can change LCA parameters in Options and increase the minimal score to 60 and low the max e-value allow to 10<sup>-10</sup> and the min complexity to 0.5 in order to reduce false positive alignments.

**Results: Family level and with the number of reads**

![megan2](https://user-images.githubusercontent.com/13121779/165253366-6b97baa5-436e-432f-a718-0c7e643e8bc8.png)

## 4. HOMEWORK

Follow the workflow of this tutorial for the taxonomic binning of the virome reads and contigs used as homework in the unit_3.

> Reads from unit_3 homework are paired_end reads. To perform this task you can do it in several ways; joining all decontaminated and QF reads and then run DIAMOND or run DIAMOND using both files and then join DIAMOND outputs, etc..

Write a brief summary describing the bioinformatic pipeline you have followed (trimming, decontamination, improve in quality, number of reads remove in each step, etc.) and the most relevant results (two figures maximun) with the taxonomy assessment of the virome at family level.

**Optional: run the same analysis but using the assembled contigs and try to compare the results using MEGAN (File/Compare and load both rma6 files created while making the individual analysis).

Deadline: 20th May.