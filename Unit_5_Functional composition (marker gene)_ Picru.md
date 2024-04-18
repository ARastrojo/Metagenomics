## Data

From Miguel dataseq: """We are using data from article with doi https://doi.org/10.1186/s12866-019-1572-x . This work analyzes the influence of soybean rhizosphere on bacterial communities both in agriculture and forest soil. 16S rRNA gene based bacteria profiling were accomplished with MiSeq 275 bp paired-end sequencing targeted V3-V4 regions, with forward primer 341F = 5′-CCTACGGGNGGCWGCAG-3′ (17bps) and reverse primer 785R = 5′-GACTACHVGGGTATCTAATCC-3 (21 bps). Amplicon size around 445 nts. Data was downlocdaded from BioProject PRJNA474716."""

The composition of microbes immediately after collection (**fresh soil**) and after 2 months in the greenhouse (**bulk soil**) were similar, indicating that the greenhouse environment and the time lapse did not largely alter microbial communities from the soil.

I have follow [Qiime2 tutorial from Miguel Redondo](https://github.com/migred/metagenomics21/wiki/QIIME2-Brief-Tutorial)

### Qiime2 installation

Follow instructions from [Qiime2 manual](https://dev.qiime2.org/latest/quickstart/):

```bash
# Update and install wget
conda update conda
conda install wget
# Installing Qiime2
wget https://data.qiime2.org/distro/core/qiime2-2023.2-py38-osx-conda.yml
conda env create -n qiime2 --file qiime2-2023.2-py38-osx-conda.yml
conda activate qiime2


# RSCRIPT seems to work in the last version
wget https://data.qiime2.org/distro/amplicon/qiime2-amplicon-2024.2-py38-osx-conda.yml
conda env create -n qiime2-amplicon-2024.2 --file qiime2-amplicon-2024.2-py38-osx-conda.yml
conda activate qiime2
```

### Importing samples

**manifest.tsv**

See [Manifest file](https://github.com/qiime2/docs/blob/master/source/tutorials/importing.rst#fastq-manifest-formats) for more details.

| sample-id | forward-absolute-filepath | reverse-absolute-filepath |
| --- | --- | --- |
| Ag_soil_1 | $PWD/raw_reads/SRR7265233_1.fastq.gz | $PWD/raw_reads/SRR7265233_2.fastq.gz |
| Ag_soil_2 | $PWD/raw_reads/SRR7265228_1.fastq.gz | $PWD/raw_reads/SRR7265228_2.fastq.gz |
| Ag_soil_3 | $PWD/raw_reads/SRR7265227_1.fastq.gz | $PWD/raw_reads/SRR7265227_2.fastq.gz |
| Ag_soil_4 | $PWD/raw_reads/SRR7265230_1.fastq.gz | $PWD/raw_reads/SRR7265230_2.fastq.gz |
| Ag_soil_5 | $PWD/raw_reads/SRR7265229_1.fastq.gz | $PWD/raw_reads/SRR7265229_2.fastq.gz |
| Ag_rhizo_1 | $PWD/raw_reads/SRR7265256_1.fastq.gz | $PWD/raw_reads/SRR7265256_2.fastq.gz |
| Ag_rhizo_2 | $PWD/raw_reads/SRR7265340_1.fastq.gz | $PWD/raw_reads/SRR7265340_2.fastq.gz |
| Ag_rhizo_3 | $PWD/raw_reads/SRR7265345_1.fastq.gz | $PWD/raw_reads/SRR7265345_2.fastq.gz |
| Ag_rhizo_4 | $PWD/raw_reads/SRR7265346_1.fastq.gz | $PWD/raw_reads/SRR7265346_2.fastq.gz |
| Ag_rhizo_5 | $PWD/raw_reads/SRR7265347_1.fastq.gz | $PWD/raw_reads/SRR7265347_2.fastq.gz |
| For_soil_1 | $PWD/raw_reads/SRR7265341_1.fastq.gz | $PWD/raw_reads/SRR7265341_2.fastq.gz |
| For_soil_2 | $PWD/raw_reads/SRR7265338_1.fastq.gz | $PWD/raw_reads/SRR7265338_2.fastq.gz |
| For_soil_3 | $PWD/raw_reads/SRR7265339_1.fastq.gz | $PWD/raw_reads/SRR7265339_2.fastq.gz |
| For_soil_4 | $PWD/raw_reads/SRR7265336_1.fastq.gz | $PWD/raw_reads/SRR7265336_2.fastq.gz |
| For_soil_5 | $PWD/raw_reads/SRR7265337_1.fastq.gz | $PWD/raw_reads/SRR7265337_2.fastq.gz |
| For_rhizo_1 | $PWD/raw_reads/SRR7265259_1.fastq.gz | $PWD/raw_reads/SRR7265259_2.fastq.gz |
| For_rhizo_2 | $PWD/raw_reads/SRR7265260_1.fastq.gz | $PWD/raw_reads/SRR7265260_2.fastq.gz |
| For_rhizo_3 | $PWD/raw_reads/SRR7265265_1.fastq.gz | $PWD/raw_reads/SRR7265265_2.fastq.gz |
| For_rhizo_4 | $PWD/raw_reads/SRR7265266_1.fastq.gz | $PWD/raw_reads/SRR7265266_2.fastq.gz |
| For_rhizo_5 | $PWD/raw_reads/SRR7265358_1.fastq.gz | $PWD/raw_reads/SRR7265358_2.fastq.gz |

```bash
qiime tools import --type 'SampleData[PairedEndSequencesWithQuality]' \
                   --input-path manifest.tsv \
                   --output-path paired-end-demux.qza \
                   --input-format PairedEndFastqManifestPhred33V2
```

### ASVs determination using DADA2

> metadata file

| sample-id | soil | type | replicate |
| --- | --- | --- | --- |
| Ag_soil_1 | Ag  | soil | 1   |
| Ag_soil_2 | Ag  | soil | 2   |
| Ag_soil_3 | Ag  | soil | 3   |
| Ag_soil_4 | Ag  | soil | 4   |
| Ag_soil_5 | Ag  | soil | 5   |
| Ag_rhizo_1 | Ag  | rhizo | 1   |
| Ag_rhizo_2 | Ag  | rhizo | 2   |
| Ag_rhizo_3 | Ag  | rhizo | 3   |
| Ag_rhizo_4 | Ag  | rhizo | 4   |
| Ag_rhizo_5 | Ag  | rhizo | 5   |
| For_soil_1 | For | soil | 1   |
| For_soil_2 | For | soil | 2   |
| For_soil_3 | For | soil | 3   |
| For_soil_4 | For | soil | 4   |
| For_soil_5 | For | soil | 5   |
| For_rhizo_1 | For | rhizo | 1   |
| For_rhizo_2 | For | rhizo | 2   |
| For_rhizo_3 | For | rhizo | 3   |
| For_rhizo_4 | For | rhizo | 4   |
| For_rhizo_5 | For | rhizo | 5   |

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

We can visualize the results by running the following commands:

```bash
# qiime metadata tabulate \
#  --m-input-file stats.qza \
#  --o-visualization stats.qzv

# Extract minimum number of sequence to define cut-off
qiime feature-table summarize \
  --i-table table.qza \
 --o-visualization table.qzv \
  --m-sample-metadata-file metadata

# qiime feature-table tabulate-seqs \
#  --i-data rep-seqs.qza \
#  --o-visualization rep-seqs.qzv
```

> Minimum frequency: 21870 (cut-off 0.1% of this frequency)

### Removal of singletons and low-frequency ASVs

```bash
qiime feature-table filter-features --i-table table.qza \
                                    --p-min-frequency 21 \
                                    --p-min-samples 2 \
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

#### Running Picrust2 from Qiime2

[Manual](https://github.com/picrust/picrust2/wiki/q2-picrust2-Tutorial)

- Installing q2-picrust2 Qiime2 plugin:

```bash
mamba install q2-picrust2 \
-c conda-forge \
-c bioconda \
-c gavinmdouglas 
```

- Running Picrust2

```bash
qiime picrust2 full-pipeline \
   --i-table table_filt.qza \
   --i-seq rep-seqs_filt.qza \
   --output-dir q2-picrust2_output \
   --p-placement-tool sepp \
   --p-threads 2 \
   --p-hsp-method pic \
   --p-max-nsti 2 \
   --verbose

# Using Qiime to analyses dataset based on pathways (optional)
qiime feature-table summarize \
   --i-table q2-picrust2_output/pathway_abundance.qza \
   --o-visualization q2-picrust2_output/pathway_abundance.qzv

## Minimum depth > 3285476 for above
## Pathways based diversity
qiime diversity core-metrics \
   --i-table q2-picrust2_output/pathway_abundance.qza \
   --p-sampling-depth 3285476 \
   --m-metadata-file metadata \
   --output-dir pathways_core_metrics_out \
   --p-n-jobs 1

# The same can be perfomed based on KO or EC
```

- Export Picrust2 results:

```bash
qiime tools export \
   --input-path q2-picrust2_output/pathway_abundance.qza \
   --output-path picrust_pahtways

biom convert \
   -i picrust_pahtways/feature-table.biom \
   -o picrust_pahtways/pathways.biom.tsv \
   --to-tsv

qiime tools export \
   --input-path q2-picrust2_output/ko_metagenome.qza \
   --output-path picrust_kos

biom convert \
   -i picrust_kos/feature-table.biom \
   -o picrust_kos/kos.biom.tsv \
   --to-tsv

qiime tools export \
   --input-path q2-picrust2_output/ec_metagenome.qza \
   --output-path picrust_ec

biom convert \
   -i picrust_ec/feature-table.biom \
   -o picrust_ec/ec.biom.tsv \
   --to-tsv

```

#### Performing Picrust2 outside of Qiime2

For running Picrust2 outside Qiime2 we need to have a table (tsv or biom format) with the ASV or OTU obtained and the corresponding sequences in fasta format.

- Export ASV/OTU table to biom or *tsv* format from Qiime2 artifact:

```
qiime tools export \
  --input-path table_filt.qza \
  --output-path qiime2_output

# Optional
# biom convert -i ./qiime2_output/feature-table.biom -o ./qiime2_output/asv-table.tsv --to-tsv

qiime tools export \
  --input-path rep-seqs_filt.qza \
  --output-path qiime2_output

```

- Install picrust2 with *conda/mamba*:

```bash
mamba create -n picrust2 -c bioconda -c conda-forge picrust2=2.5.2
```

- **Running Picrust2**

```bash
cd qiime2_output
picrust2_pipeline.py -s dna-sequences.fasta -i feature-table.biom -o ../picrust2_output -p 2

# This will take a while, as this new version of picrust do not used a precomputed database of known taxa, but contrast, it has to align our ASV/OTU againts the whole database to assign the taxa.


# Warning - 19 input sequences aligned poorly to reference sequences (--min_align option specified a minimum proportion of 0.8 aligning to reference sequences). These input sequences will not be placed and will be excluded from downstream steps.

# This is the set of poorly aligned input sequences to be excluded: 45558c14bfb0c9396acb617c54bdd2fe, fb533b558cae60b8d533612239ac8989, 345d5913bb54e2f487601319de81d254, 340c1f0ca763b64e046dc68132d7f9dd, 35396a18cc1c6c9e26e2a40e042d06e5, 4703cbfcc50f5f462ee71ed61335016e, 7871ce6f17e85156d27f0a958ef46f3b, 1b20d755ba39660ca6949f8769167ccf, f6066de72298d20ea9f50d239a369e76, b015d15264dec4b1e253d81d717b0e8e, 8710f6f0af3601a99bf555d62f4287e6, dce31756a536d7a9ee911d33ab36efe3, b2ccda821eca74ee807fab6f0f310442, 6b5d2912c055df0fd3dcf18a1a2cc0b1, 3875d32a87c723bc473335803b2321de, 05b22ee0ceeb88477546916c6cfaaeff, 41890dc12a7cbda3364857d49c024d12, 7f3c24ff80de28b187460cae0bba67a1, b2ef6a4aa5fd9db7e64fd730e1f11475

# 39 of 7547 ASVs were above the max NSTI cut-off of 2.0 and were removed from the downstream analyses.


# In my Mac (2 cores, 8 Gb of RAM) took ~2.5 hours
```

#### Visualizing Picrust2 results with ggPicrust2 in R

[ggPicrust2](https://github.com/cafferychen777/ggpicrust2) is a dedicated package to analysis the output from picrust2.

- Installing ggPicrust2:
```R
install.packages("ggpicrust2")
# Although it is suppose that R install all dependencies, some of them have to be install separately
install.packages("tidyverse")
install.packages("devtools")
devtools::install_github("dieterich-lab/LINDA", build_vignettes = FALSE)
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
BiocManager::install("KEGGREST")
```

Although it sounds easy to install, many times installation fails. After trying several methods (see [here](https://cafferychen777.github.io/ggpicrust2/#installation) for more details), I was able to install the packages in a clean R4.3.3 installation (removing all temporal files from previous R installations). 

- Running ggPicrust2:
```R
# Loading packages
library(readr)
library(ggpicrust2)
library(tibble)
library(tidyverse)
library(ggprism)
library(patchwork)
library(LinDA)

# Reading metadata
setwd("/Users/arastrojo/Library/CloudStorage/OneDrive-UAM/Metag/datos/soy_soil/")
metadata <- read_delim(
  "metadata",
  delim = "\t",
  escape_double = FALSE,
  trim_ws = TRUE
)

## KEGG Differrential Analysis by soil type (DA)
setwd("/Users/arastrojo/Library/CloudStorage/OneDrive-UAM/Metag/datos/soy_soil/picrust2_output/")
# We have to first decompress pred_metagenome_unstrat.tsv.gz file
kegg_abundance <- ko2kegg_abundance( "./KO_metagenome_out/pred_metagenome_unstrat.tsv") 
daa_results_df <- pathway_daa(abundance = kegg_abundance, metadata = metadata, group = "type", daa_method = "LinDA", select = NULL, p.adjust = "BH", reference = NULL) 
daa_annotated_results_df <- pathway_annotation(pathway = "KO", daa_results_df = daa_results_df, ko_to_kegg = TRUE)
df <- apply(daa_annotated_results_df,2,as.character)
write.csv(df, "KEGG_DA.csv")

```

- KO DA results:
| feature | method | group1 | group2 | p_values | adj_method | p_adjust | pathway_name                                            | pathway_description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | pathway_class                                                    | pathway_map                                             |
|---------|--------|--------|--------|----------|------------|----------|---------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|---------------------------------------------------------|
| ko01056 | LinDA  | rhizo  | soil   | 3.29E-15 | BH         | 8.68E-13 | Biosynthesis of type II polyketide backbone             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Metabolism; Metabolism of terpenoids and polyketides             | Biosynthesis of type II polyketide backbone             |
| ko00909 | LinDA  | rhizo  | soil   | 1.90E-11 | BH         | 2.51E-09 | Sesquiterpenoid and triterpenoid biosynthesis           | Sesquiterpenoids (C15 terpenoids) are a group of terpenoids consisting of three isoprene units. They are derive from farnesyl diphosphate (FPP) and can be cyclized to produce various skeletal structures. Sesquiterpenoid biosynthesis begins with the loss of diphosphate from FPP under the action of sesquiterpene synthesis enzymes, generating an allylic cation that is highly susceptible to intramolecular attacks. Cyclization of the farnesyl cation may take place onto either of the remaining double bonds with the result that 6-, 10-, or 11-membered rings may be formed. Many sesquiterpenoids have been isolated from plants, fungi, marine organisms, and Streptomyces species. This map shows a few examples of acyclic and cyclic sesquiterpenoids.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Metabolism; Metabolism of terpenoids and polyketides             | Sesquiterpenoid and triterpenoid biosynthesis           |
| ko03050 | LinDA  | rhizo  | soil   | 9.25E-11 | BH         | 8.14E-09 | Proteasome                                              | The proteasome is a protein-destroying apparatus involved in many essential cellular functions, such as regulation of cell cycle, cell differentiation, signal transduction pathways, antigen processing for appropriate immune responses, stress signaling, inflammatory responses, and apoptosis. It is capable of degrading a variety of cellular proteins in a rapid and timely fashion and most substrate proteins are modified by ubiquitin before their degradation by the proteasome. The proteasome is a large protein complex consisting of a proteolytic core called the 20S particle and ancillary factors that regulate its activity in various ways. The most common form is the 26S proteasome containing one 20S core particle and two 19S regulatory particles that enable the proteasome to degrade ubiquitinated proteins by an ATP-dependent mechanism. Another form is the immunoproteasome containing two 11S regulatory particles, PA28 alpha and PA28 beta, which are induced by interferon gamma under the conditions of intensified immune response. Other regulatory particles include PA28 gamma and PA200. Although PA28 gamma also belongs to a family of activators of the 20S proteasome, it is localized within the nucleus and forms a homoheptamer. PA28 gamma has been implicated in the regulation of cell cycle progression and apoptosis. PA200 has been identified as a large nuclear protein that stimulates proteasomal hydrolysis of peptides. | Genetic Information Processing; Folding, sorting and degradation | Proteasome                                              |
| ko04622 | LinDA  | rhizo  | soil   | 3.15E-09 | BH         | 2.08E-07 | RIG-I-like receptor signaling pathway                   | Specific families of pattern recognition receptors are responsible for detecting viral pathogens and generating innate immune responses. Non-self RNA appearing in a cell as a result of intracellular viral replication is recognized by a family of cytosolic RNA helicases termed RIG-I-like receptors (RLRs). The RLR proteins include RIG-I, MDA5, and LGP2 and are expressed in both immune and nonimmune cells. Upon recognition of viral nucleic acids, RLRs recruit specific intracellular adaptor proteins to initiate signaling pathways that lead to the synthesis of type I interferon and other inflammatory cytokines, which are important for eliminating viruses.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Organismal Systems; Immune system                                | RIG-I-like receptor signaling pathway                   |
| ko00622 | LinDA  | rhizo  | soil   | 8.93E-09 | BH         | 4.72E-07 | Xylene degradation                                      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Metabolism; Xenobiotics biodegradation and metabolism            | Xylene degradation                                      |
| ko04976 | LinDA  | rhizo  | soil   | 3.50E-08 | BH         | 1.32E-06 | Bile secretion                                          | Bile is a vital secretion, essential for digestion and absorption of fats and fat-soluble vitamins in the small intestine. Moreover, bile is an important route of elimination for excess cholesterol and many waste product, bilirubin, drugs and toxic compounds. Bile secretion depends on the function of membrane transport systems in hepatocytes and cholangiocytes and on the structural and functional integrity of the biliary tree. The hepatocytes generate the so-called primary bile in their canaliculi. Cholangiocytes modify the canalicular bile by secretory and reabsorptive processes as bile passes through the bile ducts. The main solutes in bile are bile acids, which stimulate bile secretion osmotically, as well as facilitate the intestinal absorption of dietary lipids by their detergent properties. Bile acids are also important signalling molecules. Through the activation of nuclear receptors, they regulate their own synthesis and transport rates.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Organismal Systems; Digestive system                             | Bile secretion                                          |
| ko01057 | LinDA  | rhizo  | soil   | 3.22E-08 | BH         | 1.32E-06 | Biosynthesis of type II polyketide products             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Metabolism; Metabolism of terpenoids and polyketides             | Biosynthesis of type II polyketide products             |
| ko00120 | LinDA  | rhizo  | soil   | 4.15E-08 | BH         | 1.37E-06 | Primary bile acid biosynthesis                          | Bile acids are steroid carboxylic acids derived from cholesterol in vertebrates. The primary bile acids, cholic acid and chenodeoxycholic acid, are synthesized in the liver and conjugated with taurine or glycine before secretion via bile into the intestine. The conversion from cholesterol to cholic and chenodeoxycholic acids involves four steps: 1) the initiation of synthesis by 7alpha-hydroxylation of sterol precursors, 2) further modifications to the ring structures, 3) side-chain oxidation and shortening (cleavage) by three carbons, and 4) conjugation of the bile acid with taurine or glycine.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Metabolism; Lipid metabolism                                     | Primary bile acid biosynthesis                          |
| ko00621 | LinDA  | rhizo  | soil   | 1.04E-07 | BH         | 3.04E-06 | Dioxin degradation                                      | Dioxins and dioxin-like compounds, including PCDDs, PCDFs and PCBs, are persistent organic pollutants (POPs) that are resistant to environmental degradation. However, POPs can be degraded by certain microorganisms with acquisition of a novel set of enzymes, such as biphenyl degradation by Paraburkholderia xenovorans LB400 involving four novel enzymes encoded in operon-like structures [MD:M00543]. DDT, another POP, and carbazol are also known to be degraded in similar pathways.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Metabolism; Xenobiotics biodegradation and metabolism            | Dioxin degradation                                      |
| ko00232 | LinDA  | rhizo  | soil   | 3.52E-07 | BH         | 9.29E-06 | Caffeine metabolism                                     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Metabolism; Biosynthesis of other secondary metabolites          | Caffeine metabolism                                     |
| ko01053 | LinDA  | rhizo  | soil   | 1.65E-06 | BH         | 3.97E-05 | Biosynthesis of siderophore group nonribosomal peptides |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Metabolism; Metabolism of terpenoids and polyketides             | Biosynthesis of siderophore group nonribosomal peptides |
| ko04971 | LinDA  | rhizo  | soil   | 3.78E-06 | BH         | 8.31E-05 | Gastric acid secretion                                  | Gastric acid is a key factor in normal upper gastrointestinal functions, including protein digestion and calcium and iron absorption, as well as providing some protection against bacterial infections. The principal stimulants of acid secretion at the level of the parietal cell are histamine (paracrine), gastrin (hormonal), and acetycholine (ACh; neurocrine). Stimulation of acid secretion typically involves an initial elevation of intracellular calcium and cAMP, followed by activation of protein kinase cascades, which trigger the translocation of the proton pump, H+,K+-ATPase, from cytoplasmic tubulovesicles to the apical plasma membrane and thereby H+ secretion into the stomach lumen.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Organismal Systems; Digestive system                             | Gastric acid secretion                                  |


```R
# Pathways DA (using MetaCyc database)
setwd("/Users/arastrojo/Library/CloudStorage/OneDrive-UAM/Metag/datos/soy_soil/picrust2_output/")
# We have to first decompress path_abun_unstrat.tsv.gz file
abundance_file <- "./pathways_out/path_abun_unstrat.tsv"
abundance_data <- read_delim(abundance_file, delim = "\t", col_names = TRUE, trim_ws = TRUE)
metacyc_daa_results_df <- pathway_daa(abundance = abundance_data %>% column_to_rownames("pathway"), metadata = metadata, group = "soil", daa_method = "LinDA", p.adjust = "BH")
metacyc_daa_annotated_results_df <- pathway_annotation(pathway = "MetaCyc", daa_results_df = metacyc_daa_results_df, ko_to_kegg = FALSE)
write.csv(metacyc_daa_annotated_results_df, "metacyc_DA_soil.csv")
```

- Pathways DA results table:
| feature  | method | group1 | group2 | p_values | adj_method | p_adjust | description                                            |
|----------|--------|--------|--------|----------|------------|----------|--------------------------------------------------------|
| PWY-6383 | LinDA  | rhizo  | soil   | 1.70E-12 | BH         | 7.20E-10 | mono-trans, poly-cis decaprenyl phosphate biosynthesis |
| PWY-6957 | LinDA  | rhizo  | soil   | 2.22E-11 | BH         | 4.71E-09 | mandelate degradation to acetyl-CoA                    |
| P562-PWY | LinDA  | rhizo  | soil   | 8.33E-11 | BH         | 1.18E-08 | myo-inositol degradation I                             |
| PWY-6071 | LinDA  | rhizo  | soil   | 1.44E-10 | BH         | 1.22E-08 | superpathway of phenylethylamine degradation           |
| PWY-7237 | LinDA  | rhizo  | soil   | 1.33E-10 | BH         | 1.22E-08 | myo-, chiro- and scillo-inositol degradation           |
| PWY-6174 | LinDA  | rhizo  | soil   | 1.88E-10 | BH         | 1.33E-08 | mevalonate pathway II (archaea)                        |
| PWY-5420 | LinDA  | rhizo  | soil   | 4.16E-10 | BH         | 2.52E-08 | catechol degradation II (meta-cleavage pathway)        |
| PWY-5183 | LinDA  | rhizo  | soil   | 6.44E-10 | BH         | 3.41E-08 | superpathway of aerobic toluene degradation            |
| PWY-7391 | LinDA  | rhizo  | soil   | 7.37E-10 | BH         | 3.47E-08 | isoprene biosynthesis II (engineered)                  |
| PWY-7255 | LinDA  | rhizo  | soil   | 9.96E-10 | BH         | 4.22E-08 | ergothioneine biosynthesis I (bacteria)                |
| P125-PWY | LinDA  | rhizo  | soil   | 1.66E-09 | BH         | 6.41E-08 | superpathway of (R,R)-butanediol biosynthesis          |


```R
# Pathways DA plots
metacyc_da_f <- metacyc_daa_results_df[metacyc_daa_results_df$p_adjust < 0.00001,]
p <- pathway_errorbar(abundance = abundance_data %>% column_to_rownames("pathway"),
                      daa_results_df = metacyc_daa_annotated_results_df,
                      Group = metadata$type,
                      ko_to_kegg = FALSE,
                      p_values_threshold = 0.05,
                      order = "group",
                      select = metacyc_da_f$feature,
                      p_value_bar = TRUE,
                      colors = NULL,
                      x_lab = "description")
p
```

__Pathways DA plots (soil type: bulk soil or rhizosphere)__
![metacyc_DA_type](../images/metacyc_DA_type.png)

__Pathways DA plots (soil origirin: agriculture or forestal)__
![metacyc_DA_type](../images/metacyc_DA_soil.png)



* * *

> A partir de aquí no lo necesito, estaría bien tenerlo para comparar los PCA con taxonomía / filogenia y con pathaways/kos, pero a partir de instalar rescript para bajar y filtrar la base de datos se va todo al carajo y qiime deja de funcionar

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
conda install -c conda-forge -c bioconda -c qiime2 -c defaults xmltodict
pip install git+https://github.com/bokulich-lab/RESCRIPt.git
```

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