## Detailed Syllabus
UNIT 1. Introduction to metagenomics. Definitions. The great plate count anomaly. History. Microbial communities: the big picture. Shotgun vs. marker gene Next Generation Sequencing: Operational Taxonomic Units (OTUs) and contigs. The tree of life. The Human Microbiome Project. Pipelines. Major issues and bias in metagenomics. Functional annotation of contigs. Repositories and databases.
UNIT 2. Deep sequencing of maker genes. Beyond 16S. Choice of targeted variable regions in marker genes. DNA extraction and PCR amplification. Barcodes and parallel sequencing. Sequence pre-processing: quality filtering, chimeric reads, and more. Alignment and clustering into OTUs. Phylogenetic trees. Taxonomic binning. Who is there? Rarefaction curves and alpha diversity. Beta diversity.
UNIT 3. Shotgun NGS sequencing and de novo assembly. NGS strategies and coverage. Overlap Layout Consensus and De Brujin Graph assembly. Viral and bacterial full-length genome assembly. Contig scaffolding with paired-end reads. Assembly quality parameters.
UNIT 4. Metagenomic taxonomic composition. Binning. Based on sequence composition (kmer and %CGs) or based on sequence (blast, Diamond, BLAT,...).
Best hit or Lowest Common Ancestor.
UNIT 5. Functional composition in a microbial environment. What are they doing?. Categories. Databases: COG, SEED, PFAM, KEGG, and more. Annotation systems. Metabolic pathways.
UNIT 6. Metagenomes comparison. Exploratory methods: heat maps, dendograms, and more. Computing distances. Ordenation in reduced space: PCA, PCoA, NMDS, and more. Are two groups of metagenomes statistically different in their composition?. ANOSIM, PERMANOVA, PERMADIST, SIMPER.
UNIT 7. Functional composition inference from marker genes. PICRUSt.


### General
Upload all datasets to oneDrive and create a link for download

Unit 5 --> Functional composition explanation and metagenome comparison merge. Explain functional composition analysis with Humann, and then use STAMP for comparison (We cannot run humann in the computional resources we have)

Unit 6 --> pycrust + STAMP again


### Unit 3
Move quast cgi2html code upwards 

### Unit 4 
Use Kraken2 instead of MEGAN (very high RAM consumption)

### Unit 5-6 

Merge both units
toy_example.fastq??? Ask Dani
Update to humann3 --> fail to install on my mac

### Unit 7 

Update to picrust2??
Find a dataset for a task (ask Miguel if we can use unit 2 dataset)



***

### Conda Enviroment for testing

```bash
conda create -n metag python=3.7
```

#### Humann 3

[Official web](https://huttenhower.sph.harvard.edu/humann)

[Official tutorial](https://github.com/biobakery/biobakery/wiki/humann3)


**Installation**  

```bash
conda activate metag

pip install humann --no-binary :all:
# or (but It does not work in my mac) 
# conda config --add channels biobakery
# conda install humann -c biobakery

conda install metaphlan -c bioconda --> FAIL

# Output in format: Requested package -> Available versionsThe following specifications were found to be incompatible with your system:

#   - feature:/osx-64::__osx==10.16=0
#   - metaphlan -> matplotlib-base -> __osx[version='>=10.11']

# Your installed version is: 10.16


```

**Downloading databases**  

```bash
dbpath='/' # External HD disk?
humann_databases --download chocophlan full /path/to/databases --update-config yes
humann_databases --download uniref uniref90_diamond /path/to/databases --update-config yes
humann_databases --download utility_mapping full /path/to/databases --update-config yes
```


humann -i sample_reads.fastq -o sample_results

***


#### Simulate reads

https://github.com/HadrienG/InSilicoSeq

curl -O -J -L https://osf.io/thser/download  # download the example data
iss generate --genomes SRS121011.fasta --model miseq --output miseq_reads










