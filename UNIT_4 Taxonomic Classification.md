# Taxonomy classification 

## 1. Pre-processing

- Create a folder and obtain reads:

```bash
cd /home/metag/Documents/
mkdir unit_4
```

As example, we are going to used the reads of *virome_1* used in _Unit 3b_. 
As we have already perform quality filtering and decontamination we only need to copy/link reads files here:

```bash
cd unit_4
ln -rs ../unit_3b/virome_1_qf_paired_nonHuman_nonPhix_R1.fq.gz ./virome_1_qf_R1.fq.gz
ln -rs ../unit_3b/virome_1_qf_paired_nonHuman_nonPhix_R1.fq.gz ./virome_1_qf_R2.fq.gz

# Note that we have "modify" the name of the files in the link, just for convinience
```

> _-r_ option does not exit in mac, take care creating symbolic link in mac with relative path, although it is possible to create, it is better to use absolute paths in mac. 

Addittionaly, we will used quality filtered reads from *virome_2* to compare taxonomic classification from both viromes:

```bash
ln -rs ../data/viromas/virome_2/virome_2_qf_R1.fq.gz .
ln -rs ../data/viromas/virome_2/virome_2_qf_R2.fq.gz .
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

However, although Diamond running time is not to high (~160k reads takes ~4 minutes), MEGAN, the program we are going to use for parsing Diamond hits and assign taxonomy to the reads, uses a <u>huge amount of RAM memory</u> and with large dataset many times it gets blocked. To avoid this, we are going to take  a **random subsample** using [seqtk](https://github.com/lh3/seqtk):

```bash
conda install -c bioconda seqtk -y

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

We can obtain a general view of the viromes. For instance, in virome 2 there are many bacteriophages (viruses than infect bacteria) from families _Myoviridae_, _Podoviridae_ and _Siphoviridae_ and viruses from the _Geminiviridae_ family, while in virome 1 in enriched in RNA virures (mainly unclassified). 


## Taxonomy using [Kraken2](https://ccb.jhu.edu/software/kraken2/)

Using the same dataset (virome_1 and virome_2) we are going to try another classification method. This time, instead of being an alignment-based program, we will use a _k-mer_ based program called [**Kraken2**](https://github.com/DerrickWood/kraken2). _K-mer_-based algorithms are much more faster than alignment-based, but usually they have a lower sentitivity. However, the high computation requirements of alignment-based programs are sometimes prohibitive and _k-mers_-based alternatives are the only choice. 

In our case, with low computational resources, as you have seen using MEGAN, we have had to reduce the number of reads, by subsampling, to perform the analysis, but using Kraken2 we will be able to analyse the whole dataset (and using paired reads). 

``` 
# Installing Kraken2
conda activate ngs
conda install -c bioconda kraken2
conda deactivate
```

As with alignment-based programs, here we also have to prepare an adequate database. It is possible to create a custom database for Kraken2 ([Kraken2 manual](https://github.com/DerrickWood/kraken2/blob/master/docs/MANUAL.markdown)). However, the developers of Kraken2 have already created several useful databases and we are going to download the pre-built viral database [Pre-built Databases](https://benlangmead.github.io/aws-indexes/k2):

```bash
# Download viral database
wget https://genome-idx.s3.amazonaws.com/kraken/k2_viral_20221209.tar.gz
mkdir k2_viral_20221209
tar -xzf k2_viral_20221209.tar.gz -C k2_viral_20221209
````

- **Running Kraken2**

```bash
# Virome 1
kraken2 -db k2_viral_20221209 --paired virome_1_qf_R1.fq.gz virome_1_qf_R2.fq.gz --report virome_1_report.txt > virome_1_k2_output.txt 
````

> Loading database information... done.  
> 79965 sequences (39.54 Mbp) processed in **8.468s** (566.6 Kseq/m, 280.12 Mbp/m).  
>   78469 sequences classified (98.13%)  
>   1496 sequences unclassified (1.87%)  

```bash
# Virome 2
kraken2 -db k2_viral_20221209 --paired virome_2_qf_R1.fq.gz virome_2_qf_R2.fq.gz --report virome_2_report.txt > virome_2_k2_output.txt 
```

> Loading database information... done.  
> 101345 sequences (60.42 Mbp) processed in **10.152s** (599.0 Kseq/m, 357.11 Mbp/m).  
>   96843 sequences classified (95.56%)  
>   4502 sequences unclassified (4.44%)  

- **Kraken2 output format**

| C/U | Read_name       | Assigned Taxid | Read lengths (paired) | Taxid:Assigned kmers                                        |
|-----|-----------------|----------------|----------------------|------------------------------------------------------------|
| C   | NC_048825.1_0_0 | 2656532        | 300\|301             | 2656532:71 2842796:5 2656532:2 2842796:16 2656532:34 [..]  |
| C   | NC_048825.1_1_0 | 2656532        | 300\|281             | 2656532:179 2842796:1 2656532:9 2842796:4 2656532:28 [..]  |
| C   | NC_048825.1_2_0 | 2656532        | 293\|299             | 0:14 2656532:5 0:14 2656532:1 0:6 2656532:37 0:1 [..]      |

> C/U: Classified/unclassified

As you can see, the output is difficult to used as it. 

- **Kraken2 report**

Kraken2 report shows a more hierarchical view:

<pre>
  4.50  4559    4559    U       0       unclassified
 95.50  96786   0       R       1       root
 95.50  96786   0       D       10239     Viruses
 39.09  39620   0       D1      2731341     Duplodnaviria
 39.09  39620   0       K       2731360       Heunggongvirae
 39.09  39620   0       P       2731618         Uroviricota
 39.09  39620   81      C       2731619           Caudoviricetes
  9.44  9563    1478    G       545932              Bruynoghevirus
  7.76  7866    0       S       2040657               Bruynoghevirus PAA2
  7.76  7866    7866    S1      1429758                 Pseudomonas phage phiIBB-PAA2
  0.05  54      0       G1      2562667               unclassified Bruynoghevirus
  0.05  54      54      S       1640969                 Pseudomonas phage DL54
  0.04  43      0       S       2040659               Bruynoghevirus PaP4
  0.04  43      43      S1      1273709                 Pseudomonas phage PaP4
  0.04  39      0       S       2040658               Bruynoghevirus TL
  0.04  39      39      S1      1406974                 Pseudomonas phage TL
  0.03  31      4       S       188350                Bruynoghevirus PaP3
  0.01  14      14      S1      1234701                 Pseudomonas phage vB_PaeP_p2-10_Or1
  0.01  13      13      S1      2905964                 Pseudomonas phage PaP3
  0.03  28      0       S       2040656               Bruynoghevirus Ab22
  0.03  28      28      S1      1548906                 Pseudomonas phage vB_PaeP_C2-10_Ab22
  0.02  19      19      S       484895                Bruynoghevirus LUZ24
  0.00  5       0       S       2040655               Bruynoghevirus CHU
  0.00  5       5       S1      1589273                 Pseudomonas phage PhiCHU
  8.77  8890    2143    G       1921407             Pakpunavirus
  6.54  6628    407     G1      2109910               unclassified Pakpunavirus
  6.13  6216    6216    S       1716042                 Pseudomonas phage PaoP5
  0.00  3       3       S       1735586                 Pseudomonas phage C11
  0.00  1       1       S       1716041                 Pseudomonas phage K8
  0.00  1       1       S       1777072                 Pseudomonas phage K5
  0.03  32      0       S       1921411               Pakpunavirus PAKP1
  0.03  32      32      S1      743813                  Pseudomonas phage PAK_P1
</pre>

But, it is still difficult to interpert. The columns of the report are described below:

1) Percentage of fragments covered by the clade rooted at this taxon
2) Number of fragments covered by the clade rooted at this taxon
3) Number of fragments assigned directly to this taxon
4) A rank code indicating (U)nclassified, (R)oot, (D)omain, (K)ingdom, (P)hylum, (C)lass, (O)rder, (F)amily, (G)enus, (S)pecies. Taxa that are not any of these 10 ranks have a rank code that is formed by using the rank code of the closest ancestor rank with a number indicating the distance from that rank. Ex. Pseudomonas phage phiIBB-PAA2 has a rank code of “S1” because it is a subspecies one step below Bruynoghevirus PAA2.
5) The Taxonomic ID number from NCBI
6) Indented Scientific Name

- **Visualization of Kraken2 results using [Pavian](https://github.com/fbreitwieser/pavian)**

Pavian can be used online, but a low memory limit. To use Pavian without memory limit with have to make use of the R package (open RStudio):

```R
# Installing Pavian
if (!require(remotes)) { install.packages("remotes") }
remotes::install_github("fbreitwieser/pavian")

# Run Pavian server
options(shiny.maxRequestSize=500*1024^2) # Increase max memory available
pavian::runApp(port=5000)
```

```bash
Manually installation of Pavian (compilling from source)

# R: 
install.packages("remotes")
remotes::install_github("fbreitwieser/shinyFileTree")
install.packages('shinydashboard')
install.packages('shinyjs')
install.packages('shinyWidgets')
install.packages('DT')
install.packages('plyr')
install.packages('RColorBrewer')
install.packages('colorspace')
install.packages('ggplot2')
install.packages('rhandsontable')

# Download from source:
cd /media/DiscoLocal/BioInformatica/
gdown https://github.com/fbreitwieser/pavian/archive/refs/tags/v1.0.zip
unzip v1.0.zip

# R: install.packages("/media/DiscoLocal/BioInformatica/pavian-1.0", repos = NULL, type="source")

```





Upload both reports to Pavian:

![pavian_upload](https://github.com/ARastrojo/Metagenomics/blob/5d53e3c500a8d9ee5208fa83a64c482ae8ea23f8/images/pavian_load.png)

Now, click on _"Samples"_ to see Sankey plots:

- **Virome_1**  

![Virome_1_sankey](https://github.com/ARastrojo/Metagenomics/blob/8be9189b60d7fc9e034a6c64e1f8d697790517c3/images/virome_1_sankey.png)
- **Virome_2**  

![Virome_2_sankey](https://github.com/ARastrojo/Metagenomics/blob/8be9189b60d7fc9e034a6c64e1f8d697790517c3/images/virome_2_snkey.png)

These plots can be configure in many ways. 

Finally, we can compare both viromes classifications by clicking in _"comparison"_:

![pavian_comparison](https://github.com/ARastrojo/Metagenomics/blob/8be9189b60d7fc9e034a6c64e1f8d697790517c3/images/pavian_comparison.png)

> A good paper with metagenomic comparison tools: _Terrón-Camero, L. C., Gordillo-González, F., Salas-Espejo, E., & Andrés-León, E. (2022). Comparison of Metagenomics and Metatranscriptomics Tools: A Guide to Making the Right Choice. Genes, 13(12). https://doi.org/10.3390/genes13122280_


## 4. HOMEWORK

Follow the workflow of this tutorial for the taxonomic binning and comparison of 2 viromes, the one used in unit_3 and another one  from [here](https://drive.google.com/drive/folders/1lzKVp_bkAkLcS5b2Sk5eeAYzzZU5s8R7?usp=sharing) (quality filtering should be performed). Choose one of the taxonomic binning methods described here (alignment-based or k-mer-based). 

Write a brief summary describing the bioinformatic pipeline you have followed (trimming, decontamination, improve in quality, number of reads remove in each step, etc.) and the most relevant results with the taxonomy assessment of the viromes and their comparison (use family level). Note that across with simulated virome files there is a file containing the viral genomes used for the simulation, their relative abundance and their taxonomy, therefore, the quality of the taxonomy binning can be assessed, at least qualitatively.

Deadline: 20th May.

