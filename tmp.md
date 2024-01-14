

## Data

From Miguel dataseq: """We are using data from article with doi https://doi.org/10.1186/s12866-019-1572-x . This work analyzes the influence of soybean rhizosphere on bacterial communities both in agriculture and forest soil. 16S rRNA gene based bacteria profiling were accomplished with MiSeq 275 bp paired-end sequencing targeted V3-V4 regions, with forward primer 341F = 5′-CCTACGGGNGGCWGCAG-3′ (17bps) and reverse primer 785R = 5′-GACTACHVGGGTATCTAATCC-3 (21 bps). Amplicon size around 445 nts. Data was downlocdaded from BioProject PRJNA474716."""

The composition of microbes immediately after collection (__fresh soil__) and after 2 months in the greenhouse (__bulk soil__) were similar, indicating that the greenhouse environment and the time lapse did not largely alter microbial communities

I have follow [Qiime2 tutorial from Miguel Redondo](https://github.com/migred/metagenomics21/wiki/QIIME2-Brief-Tutorial)

### Qiime2 installation

Follow instructions from [Qiime2 manual](https://dev.qiime2.org/latest/quickstart/):

```bash
# Update and install wget
conda update conda
conda install wget
# Installing Qiime2
wget https://raw.githubusercontent.com/qiime2/distributions/dev/latest/passed/qiime2-amplicon-ubuntu-latest-conda.yml
conda env create -n qiime2 --file qiime2-amplicon-ubuntu-latest-conda.yml
rm qiime2-amplicon-ubuntu-latest-conda.yml
```

### Importing samples

**[Manifest file](https://github.com/qiime2/docs/blob/master/source/tutorials/importing.rst#fastq-manifest-formats)**

> Meter manifest

| [..] | [..] | [..] |

```bash
conda activate qiime2
qiime tools import --type 'SampleData[PairedEndSequencesWithQuality]' \
                   --input-path manifest.tsv \
                   --output-path paired-end-demux.qza \
                   --input-format PairedEndFastqManifestPhred33V2

# Data summary 
qiime demux summarize --i-data paired-end-demux.qza --o-visualization paired-end-demux.qzv
conda deactivate
```

### ASVs determination using DADA2

> metadata file

| [..] | [..] | [..] |

```bash
qiime dada2 denoise-paired \
  --i-demultiplexed-seqs paired-end-demux.qza \
  --p-trim-left-f 23 \
  --p-trunc-len-f 265 \
  --p-trim-left-r 21 \
  --p-trunc-len-r 220 \
  --o-representative-sequences rep-seqs.qza \
  --o-table table.qza \
  --o-denoising-stats stats.qza \
  --p-n-threads 2 \
  --p-n-reads-learn 15000
```

We can visualise the results by running the following commands:
```bash
qiime metadata tabulate \
  --m-input-file stats.qza \
  --o-visualization stats.qzv

qiime feature-table summarize \
  --i-table table.qza \
  --o-visualization table.qzv \
  --m-sample-metadata-file metadata

qiime feature-table tabulate-seqs \
  --i-data rep-seqs.qza \
  --o-visualization rep-seqs.qzv
````

> Minimun frequency: 21870 (cuff-off 1% of this frequency)

### Removal of singletons and low-frequency ASVs

```bash
qiime feature-table filter-features --i-table table.qza \
                                    --p-min-frequency 21 \
                                    --p-min-samples 1 \
                                    --o-filtered-table table_filt.qza
# Remove filtered ASVs from req-seq
qiime feature-table filter-seqs --i-data rep-seqs.qza \
                                --i-table table_filt.qza \
                                --o-filtered-data rep-seqs_filt.qza		
# Visualize summary
qiime feature-table summarize \
      --i-table table_filt.qza \
      --o-visualization table_filt.qzv
```

### Phylogenetic distances determination using MAFFT and FastTree

```bash
qiime phylogeny align-to-tree-mafft-fasttree \
                --i-sequences rep-seqs_filt.qza \
                --o-alignment aligned-rep-seqs.qza \
                --o-masked-alignment masked-aligned-rep-seqs.qza \
                --o-tree unrooted-tree.qza \
                --o-rooted-tree rooted-tree.qza
```

### Taxonomic assignment


#### Silva database

We are going to use RESCRIPt to download and curate database:
```bash
pip install git+https://github.com/bokulich-lab/RESCRIPt.git
````

```bash
# Download database
qiime rescript get-silva-data \
      --p-version '138' \
      --p-target 'SSURef_NR99' \
      --p-include-species-labels \
      --o-silva-sequences silva-138-ssu-nr99-seqs.qza \
      --o-silva-taxonomy silva-138-ssu-nr99-tax.qza

# Remove sequences with ambiguous bases
qiime rescript cull-seqs \
      --i-sequences silva-138-ssu-nr99-seqs.qza \
      --o-clean-sequences silva-138-ssu-nr99-seqs-cleaned.qza

# Remove bad sequences (not length math)
qiime rescript filter-seqs-length-by-taxon \
      --i-sequences silva-138-ssu-nr99-seqs-cleaned.qza \
      --i-taxonomy silva-138-ssu-nr99-tax.qza \
      --p-labels Archaea Bacteria Eukaryota \
      --p-min-lens 900 1200 1400 \
      --o-filtered-seqs silva-138-ssu-nr99-seqs-filt.qza \
      --o-discarded-seqs silva-138-ssu-nr99-seqs-discard.qza

# Dereplicate database
qiime rescript dereplicate \
      --i-sequences silva-138-ssu-nr99-seqs-filt.qza  \
      --i-taxa silva-138-ssu-nr99-tax.qza \
      --p-rank-handles 'silva' \
      --p-mode 'uniq' \
      --o-dereplicated-sequences silva-138-ssu-nr99-seqs-derep-uniq.qza \
      --o-dereplicated-taxa silva-138-ssu-nr99-tax-derep-uniq.qza

```

**ggpicrust2:** r package for picrust2 results visualizarion
https://github.com/cafferychen777/ggpicrust2