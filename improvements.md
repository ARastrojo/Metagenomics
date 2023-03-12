### General
- Upload all datasets to oneDrive and create a link for download

### Unit 3
- Move quast cgi2html code upwards 

### Unit 4 
- Use Kraken2 instead of MEGAN (very high RAM consumption)

### Unit 5-6 

Merge both units
toy_example.fastq??? Ask Dani
Update to humann3 --> fail to install

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

Output in format: Requested package -> Available versionsThe following specifications were found to be incompatible with your system:

  - feature:/osx-64::__osx==10.16=0
  - metaphlan -> matplotlib-base -> __osx[version='>=10.11']

Your installed version is: 10.16


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


