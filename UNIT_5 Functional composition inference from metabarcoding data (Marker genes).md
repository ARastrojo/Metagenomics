# PICRUSt: Functional composition inference from metabarcoding data (Marker genes)

> Original paper: _Langille, M. G. I., Zaneveld, J., Caporaso, J. G., McDonald, D., Knights, D., Reyes, J. A., Clemente, J. C., Burkepile, D. E., Vega Thurber, R. L., Knight, R., Beiko, R. G., & Huttenhower, C. (2013). Predictive functional profiling of microbial communities using 16S rRNA marker gene sequences. Nature Biotechnology, 31(9), 814–821._

> This tutorial is based on [Morgan  Langille Lab's manual](https://github.com/LangilleLab/microbiome_helper/wiki/CBW-2016-PICRUSt-tutorial)

> Another good tutorial with many links to related analysis can be found in [PICRUSt webpage](https://picrust.github.io/picrust/tutorials/metagenome_prediction.html#metagenome-prediction-tutorial)

This page will walk you through the basic steps of using PICRUSt to make functional predictions (e.g. predicted metagenome) from your 16S data.

It uses an OTU table that has already been generated for use with PICRUSt (using QIIME2 and the closed-reference OTU picking protocolo, and [Greengenes](https://greengenes.secondgenome.com/) database). The data we are going to use in this tutorial comes from the stool of three groups of mice that are of different ages (young, middle, and old).

## 1. Preparing data

### 1.1. Create a new directory that will store all of the files created in this tutorial:

```bash
mkdir -p /home/${USER}/Documents/unit_5
cd /home/${USER}/Documents/unit_5
```

### 1.2. Download dataset and unzip:

```bash
wget https://dauam-my.sharepoint.com/:u:/g/personal/alberto_rastrojo_uam_es/EZEgeO_CfCVPtUiaEMdEziAByibVL2w0aYIIw_2W1L3RIQ?download=1 -O picrust_example.zip
unzip picrust_example.zip
``` 

In your working directory you should have an OTU table called "otus.biom" and a mapping file "map.tsv". The OTU table has been produced within QIIME using the greengenes reference database. The mapping file is just a tab-delimited text file that has sample ids in the first column and a couple of additional columns with metadata for each sample.

>map.tsv

| #SampleID | Disease_state | Age_Group |
|:---------:|:-------------:|-----------|
| 9Y-June1  |    Healthy    | 1_Young   |
| 10Y-June1 |    Healthy    | 1_Young   |
| [...]| [...]| [...] |
| M11-Aug14 | Sick          | 2_Mid     |
| M11-Aug15 | Sick          | 2_Mid     |
| [...]  | [...] | [...] |
| 1E-Aug16  | Healthy       | 3_Old     |
| 1E-May23  | Healthy       | 3_Old     |

### 1.3. Download pre-computed database files

In our virtual machines, to save disk space, the database files are not included.

Precomputed files can be download manually from [PICRUSt webpage](https://picrust.github.io/picrust/picrust_precalculated_files.html). 
Then, check MD5 hashes (see below) and move downloaded files to /home/bgm/miniconda3/envs/picrust/lib/python2.7/site-packages/picrust/data/ (folder should be created).

![imagen](https://user-images.githubusercontent.com/13121779/166954986-90a929c5-8c54-47ec-a870-345cb651fde1.png)

or by using the PICRUSt script:

```bash
conda activate picrust
download_picrust_files.py
```

or by using the following command:

```bash
mkdir /home/bgm/miniconda3/envs/picrust/lib/python2.7/site-packages/picrust/data/
wget https://dauam-my.sharepoint.com/:u:/g/personal/alberto_rastrojo_uam_es/EU7uEZfP4rhAhgqcMGoBIukBM7lMgWcaXiBvxS2q8xYVQA?download=1 -O 16S_13_5_precalculated.tab.gz
wget https://dauam-my.sharepoint.com/:u:/g/personal/alberto_rastrojo_uam_es/Ec8MzLpq4KZIsgnSzxGTkecBOMJjXx5HV9oo0XKjxBHQBg?download=1 -O cog_13_5_precalculated.tab.gz
wget https://dauam-my.sharepoint.com/:u:/g/personal/alberto_rastrojo_uam_es/EcL2LXSoksdLheFIMMpxTSABDzQNZi7HYbpnVLmEG0iD7w?download=1 -O ko_13_5_precalculated.tab.gz
wget https://dauam-my.sharepoint.com/:u:/g/personal/alberto_rastrojo_uam_es/EXc8EnKzMixPhDi_29Fw_UYBMsCYpedSIDdxdHjbYA4zJA?download=1 -O rfam_13_5_precalculated.tab.gz
# Check MD5 hashes before moving to the picrust folder
cp *precalculated.tab.gz /home/bgm/miniconda3/envs/picrust/lib/python2.7/site-packages/picrust/data/
```

> In any case check your downloades files using MD5 hashes:

| File | MD5 |
| --- | --- |
| 16S_13_5_precalculated.tab.gz | 2fb637cbf5b0898bbca15a94e9a08f1f |
| cog_13_5_precalculated.tab.gz | 52fc0c2a627903cf3e270ccd5e5f8ed7 |
| ko_13_5_precalculated.tab.gz | 8220d5b3f48af4a86c1542973a365500 |
| rfam_13_5_precalculated.tab.gz | f2c9fed80369243806f8aa970b6e0182 |

## 2. Running PICRUSt predictions 

PICRUSt environmnent should be active (if you did not do it before while downloading the database files)

```bash
conda activate picrust
```


### 2.1. Normalizr 16S copy number

The first step is to correct the OTU table based on the predicted 16S copy number for each organism in the OTU table:

```bash
normalize_by_copy_number.py -i otus.biom -o otus_corrected.biom 
```
Note that this is just a normal OTU table which then could be used with all other tools.
If you want to look at the before and after correction you can use the biom tools to convert it to plain text:

```bash
biom convert -i otus_corrected.biom -o otus_corrected.txt --to-tsv --header-key taxonomy
biom convert -i otus.biom -o otus.txt --to-tsv --header-key taxonomy
```

> otus.txt  

| #OTU ID | 9Y-June1       | 10Y-June1 | 8Y-May23       | 10Y-May23 | 6Y-June1 | 9Y-May23       | Y7-Aug14 | Y7-Aug15 | 6Y-May23       | M11-Aug14     | [...] |
|------------------------------|----------|-----------|----------|-----------|----------|----------|----------|----------|----------|-----------|-------|
| 181348                       | 1.0      | 0.0       | 0.0      | 0.0       | 0.0      | 1.0      | 0.0      | 0.0      | 1.0      | 0.0       | [...] |
| 318732                       | 0.0      | 0.0       | 1.0      | 0.0       | 0.0      | 0.0      | 0.0      | 0.0      | 2.0      | 5.0       | [...] |
| 244484                       | 0.0      | 0.0       | 0.0      | 2.0       | 0.0      | 1.0      | 0.0      | 1.0      | 4.0      | 0.0       | [...] |
| [...]                        |          |           |          |           |          |          |          |          |          |           |       |


> otus_corrected.txt

| #OTU ID | 9Y-June1       | 10Y-June1 | 8Y-May23       | 10Y-May23 | 6Y-June1 | 9Y-May23       | Y7-Aug14 | Y7-Aug15 | 6Y-May23       | M11-Aug14     | [...] |
|---------|----------------|-----------|----------------|-----------|----------|----------------|----------|----------|----------------|---------------|-------|
| 181348  | 0.333333333333 | 0.0       | 0.0            | 0.0       | 0.0      | 0.333333333333 | 0.0      | 0.0      | 0.333333333333 | 0.0           | [...] |
| 318732  | 0.0            | 0.0       | 0.333333333333 | 0.0       | 0.0      | 0.0            | 0.0      | 0.0      | 0.666666666667 | 1.66666666667 | [...] |
| 244484  | 0.0            | 0.0       | 0.0            | 1.0       | 0.0      | 0.5            | 0.0      | 0.5      | 2.0            | 0.0           | [...] |
| [...]   |                |           |                |           |          |                |          |          |                |               | [...] |

As you can see the otus_corrected.txt file has "normalized" the OTU table according to the PICRUSt 16S copy number predictions. 
By looking at the differences between the two OTU files can you tell what the predicted 16S copy number is for OTU 181348? What about OTU 244484?

### 2.2. Predicting functional genes

Ok, now lets actually make our functional predictions of genes using KEGG Ortholog (KOs) and the corrected OTU table as input:

```bash
predict_metagenomes.py -i otus_corrected.biom -o ko_predictions.biom
```

The output from this prediction is a biom file containing the predicted set of gene (KOs) detected in each of the samples. We can check out these KO predictions again by converting the BIOM file first:

```bash
biom convert -i ko_predictions.biom -o ko_predictions.txt --to-tsv --header-key KEGG_Description   
```

| #OTU ID | 9Y-June1 | 10Y-June1 | 8Y-May23 | 10Y-May23 | 6Y-June1 | 9Y-May23 | […] | 2E-May24 | 4E-June1 | 1E-Aug16 | 1E-May23 | KEGG_Description                                             |
|---------|----------|-----------|----------|-----------|----------|----------|-----|----------|----------|----------|----------|--------------------------------------------------------------|
| K01365  | 0        | 0         | 0        | 0         | 0        | 0        | […] | 0        | 0        | 0        | 0        | cathepsin L [EC:3.4.22.15]                                   |
| K01364  | 0        | 0         | 0        | 0         | 0        | 0        | […] | 0        | 0        | 0        | 0        | streptopain [EC:3.4.22.10]                                   |
| K01361  | 18       | 20        | 9        | 4         | 11       | 4        | […] | 15       | 17       | 8        | 9        | lactocepin [EC:3.4.21.96]                                    |
| K01360  | 0        | 0         | 0        | 0         | 0        | 0        | […] | 0        | 0        | 0        | 0        | proprotein convertase subtilisin/kexin type 2 [EC:3.4.21.94] |
| K01362  | 3587     | 3559      | 3868     | 3428      | 3872     | 3462     | […] | 2616     | 3133     | 3457     | 2212     | None                                                         |
| K02249  | 0        | 0         | 0        | 0         | 0        | 0        | […] | 0        | 0        | 0        | 0        | competence protein ComGG                                     |
| K05841  | 0        | 0         | 0        | 0         | 0        | 0        | […] | 0        | 0        | 0        | 0        | sterol 3beta-glucosyltransferase [EC:2.4.1.173]              |

> Note: Default predictions from PICRUSt are based on KOs (KEGG Orthologs) but PICRUSt can also use [COGs](https://www.ncbi.nlm.nih.gov/research/cog) (Clusters of Orthologous Genes) and [Rfams](https://rfam.xfam.org/) databases.


### 2.3. Visualizing metabolic genes with iPATH3

To visualize our predicted genes in a graphical way we can make use of [iPATH3](https://pathways.embl.de/). To do that, we need the list of KOs represented in our dataset:

```bash
cut -f 1 ko_predictions.txt > kos.txt
```
The open kos.txt with MousePad (Ubuntu text editor or other) and copy all KO IDs (except 2 first lines).
Open [iPATH3 webpage](https://pathways.embl.de/) and click on "Metabolism".
Paste your IDs in the bos at the upper right corner and click on "Submit data"

![imagen](https://user-images.githubusercontent.com/13121779/167129595-68e719b2-f1ae-4af6-855f-ed8495c0bebf.png)

iPATH3 creates a map with all metabolic genes present in our dataset: 

![imagen](https://user-images.githubusercontent.com/13121779/167129768-be7f162d-0a9b-40ab-a8b6-3b15a27cc77e.png)

We can repeat the analysis but changind the "map" to check for antibiotic biosynthesis genes in our dataset:

![imagen](https://user-images.githubusercontent.com/13121779/167130197-78d3a179-9f4b-45c5-a4ac-a7c09e5e545c.png)

This is the new map:

![imagen](https://user-images.githubusercontent.com/13121779/167130261-bf47e867-1680-4cb5-bc54-b93bc7c32d57.png)

Both maps are interactive and we can explore our data in detail. For instance, it seems that in our community there are not to much Tetracyclin related genes:

![imagen](https://user-images.githubusercontent.com/13121779/167130616-4b2edd63-d505-45b1-b05e-9df394730458.png)

### 2.4. Pathways prediction


PICRUSt can also collapse KOs to KEGG Pathways. Note that one KO can map to many KEGG Pathways so a simple mapping wouldn't work here. Instead, we use the PICRUSt script "categorize_by_function.py":

```bash
categorize_by_function.py -i ko_predictions.biom -c KEGG_Pathways -l 3 -o pathway_predictions.biom
```

Again lets look at the output:

```bash
biom convert -i pathway_predictions.biom -o pathway_predictions.txt --to-tsv --header-key KEGG_Pathways
```
| #OTU ID                                                         | 9Y-June1 | 10Y-June1 | 8Y-May23 | 10Y-May23 | […] | 4E-June1 | 1E-Aug16 | 1E-May23 | KEGG_Pathways                                                                                                          |
|-----------------------------------------------------------------|----------|-----------|----------|-----------|-----|----------|----------|----------|------------------------------------------------------------------------------------------------------------------------|
| 1,1,1-Trichloro-2,2-bis(4-chlorophenyl)ethane (DDT) degradation | 11       | 21        | 10       | 7         | […] | 4        | 2        | 1        | Metabolism; Xenobiotics Biodegradation and Metabolism; 1,1,1-Trichloro-2,2-bis(4-chlorophenyl)ethane (DDT) degradation |
| ABC transporters                                                | 200982   | 174898    | 195247   | 255298    | […] | 213939   | 229000   | 451627   | Environmental Information Processing; Membrane Transport; ABC transporters                                             |
| Adherens junction                                               | 0        | 0         | 0        | 0         | […] | 0        | 0        | 0        | Cellular Processes; Cell Communication; Adherens junction                                                              |
| Adipocytokine signaling pathway                                 | 6486     | 6300      | 7408     | 6562      | […] | 7082     | 7654     | 5580     | Organismal Systems; Endocrine System; Adipocytokine signaling pathway                                                  |
| African trypanosomiasis                                         | 28       | 25        | 40       | 42        | […] | 9        | 22       | 9        | Human Diseases; Infectious Diseases; African trypanosomiasis                                                           |
| Alanine, aspartate and glutamate metabolism                     | 94807    | 90632     | 103163   | 103640    | […] | 98339    | 104441   | 115040   | Metabolism; Amino Acid Metabolism; Alanine, aspartate and glutamate metabolism                                         |


### 2.5. Pathways statistical analysis (STAMP)

Once we have the Pathways associated with the genes (KOs) in our dataset we can try to test if there is any differences in the pathways among the sample groups. To do that we are going to use [STAMP](https://beikolab.cs.dal.ca/software/STAMP), which is a dedicated program for this kind of data (metagenomics).

However, to make use of STAMP we have to convert our predicted pathways data to an STAMP format. To do that we have to download a Python script from https://github.com/LangilleLab/microbiome_helper/blob/master/biom_to_stamp.py. 

Go to the page, copy python code and create a new file using MousePad and save in unit_5 folder as biom_to_stamp.py. 

Then, we can convert our data to be use in STAMP:

```bash
python biom_to_stamp.py -m KEGG_Pathways pathway_predictions.biom > pathway_predictions.spf
```

Now, to run STAMP, open a new terminal window/tab, and activate the specific environment and execute the program:

```bash
conda activate stamp
STAMP
```

You will see the following window:

![imagen](https://user-images.githubusercontent.com/13121779/167132128-d9629d80-13f7-4b3b-9ac8-1c2af41b684a.png)

Click on File --> Load data

![imagen](https://user-images.githubusercontent.com/13121779/167132264-3f2f8aea-b166-4cf6-a46c-15795384ff02.png)

You should load the "pathway_predictions.spf" file together with "map.tsv" containing the metadata of our dataset.

By default STAMP shows you a PCA analysis of the data using the first column of the map file as grouping:

![imagen](https://user-images.githubusercontent.com/13121779/167133006-4720f156-1ade-48ec-a7fa-d1a0a23721e1.png)

We are going to change the group field (top right) to "Age_Group":

![imagen](https://user-images.githubusercontent.com/13121779/167134909-540fb5e7-17c3-459c-8da3-a65dff2d6d6c.png)

You can see that 98.5% of the variability can be explain by PC1. When we group by age, young and old mice cluster together, while middle age mice form a separated cluster. Going back, we can see that the age do not have an important influence on the grouping, and that disease status is more relevant. 

Now, we can explorer and test which pathways have significant differences. WE have to make some "clicks":
1-Change Plot type to Box Plot
2-Change Profile Level to "Level 3" which actually represents the KEGG Pathways
3-Add Multiple testing correction (Bonferromi-Holm FDR)
4-Click in "Show only active feature to remove non-significant results from the list

![imagen](https://user-images.githubusercontent.com/13121779/167136827-6f29ffc4-2ad9-45c4-8912-bb5bc192b632.png)

Now we can navigate through the feature that were statistically significant between the groups:

For example, "Glycerophospholipid metabolism" is signicantly different in sick mice compare to healthy ones:
 
![imagen](https://user-images.githubusercontent.com/13121779/167137124-423e21b8-2bfe-48ec-88f9-56f86b23a5ac.png)

### 2.6. Pathways statistical analysis (STAMP)

To further analysis a pathway of interest among the significant ones, we can go to [KEGG webpage](https://www.genome.jp/kegg/) and search it:

![imagen](https://user-images.githubusercontent.com/13121779/167138015-ec5637a3-d5b8-4e00-8eb6-05f8af88c64c.png)

Then, click on "map00564" which is the ID of the pathway:

![imagen](https://user-images.githubusercontent.com/13121779/167138095-77a424f9-c53a-4935-9a9e-3fc835fb506a.png)

In the next page you can find general information of the pathway, the graphical map and the genes (KOs) included in it:

![imagen](https://user-images.githubusercontent.com/13121779/167138286-7183910c-1376-4b5b-8d9a-d73538edc8de.png)

Click on the Genes -> KEGG ORTHOLOGY (top right) to obtain the list of genes (KOs):

![imagen](https://user-images.githubusercontent.com/13121779/167138483-1eac6295-7cb2-45ba-bd55-c3d64aa9f1d0.png)

Copy the list to a MousePad text file and save it as "map00564.txt". Then, run the following command to obtain a file only containing a list of the genes implicated in the pathway:

```bash
cut -f 1 -d ' ' map00564.txt | tr '\n' ','
```

Now, using PICRUSt again, we can directly connect the OTUs that are contributing to each KO by using the ''metagenome_contributions.py'' script. Usually the choice of KO ids would be driven by KOs that you are interested in, or KOs that are statistically signficant across your sample groupings. In our case, we have selected the KOs belonging to a significant Pathway:

```bash
metagenome_contributions.py -i otus_corrected.biom -o metagenome_contributions.txt -l K00006,K00057,K00096,K00105,K00111,K00112,K00113,K00550,K00551,K00570,K00623,K00629,K00630,K00631,K00649,K00650,K00655,K00866,K00894,K00901,K00967,K00968,K00980,K00981,K00993,K00994,K00995,K00998,K00999,K01004,K01047,K01048,K01049,K01058,K01080,K01094,K01095,K01096,K01114,K01115,K01126,K01517,K01521,K01613,K03735,K03736,K04019,K05929,K05939,K06123,K06124,K06128,K06129,K06130,K06131,K06132,K06900,K07029,K07094,K08591,K08729,K08730,K08744,K13333,K13506,K13507,K13508,K13509,K13510,K13511,K13512,K13513,K13514,K13515,K13516,K13517,K13519,K13523,K13535,K13618,K13621,K13622,K13623,K13644,K14156,K14286,K14621,K14674,K14676,K15728,K16342,K16343,K16368,K16369,K16619,K16817,K16818,K16860,K17103,K17104,K17105,K17717,K17830,K18693,K18694,K18695,K18696,K18697,K19007,K19664,K19665,K22389,K22831,K24872,K25193
```

| Gene   | Sample   | OTU     | GeneCountPerGenome | OTUAbundanceInSample | CountContributedByOTU | ContributionPercentOfSample | ContributionPercentOfAllSamples | Kingdom     | Phylum              | Class                | Order                  | Family                  | Genus               | Species         |
|--------|----------|---------|--------------------|----------------------|-----------------------|-----------------------------|---------------------------------|-------------|---------------------|----------------------|------------------------|-------------------------|---------------------|-----------------|
| K00998 | 9Y-June1 | 276629  | 1                  | 2.33                 | 2.33                  | 0.0008                      | 0.0000                          | k__Bacteria |  p__Bacteroidetes   |  c__Bacteroidia      |  o__Bacteroidales      |  f__S24-7               |  g__                |  s__            |
| K00998 | 9Y-June1 | 186233  | 1                  | 0.80                 | 0.80                  | 0.0003                      | 0.0000                          | k__Bacteria |  p__Bacteroidetes   |  c__Bacteroidia      |  o__Bacteroidales      |  f__Porphyromonadaceae  |  g__Parabacteroides |  s__distasonis  |
| K00998 | 9Y-June1 | 4306262 | 2                  | 7.50                 | 15.00                 | 0.0052                      | 0.0003                          | k__Bacteria |  p__Verrucomicrobia |  c__Verrucomicrobiae |  o__Verrucomicrobiales |  f__Verrucomicrobiaceae |  g__Akkermansia     |  s__muciniphila |
| K00998 | 9Y-June1 | 553654  | 1                  | 0.25                 | 0.25                  | 0.0001                      | 0.0000                          | k__Bacteria |  p__Firmicutes      |  c__Clostridia       |  o__Clostridiales      |  f__Lachnospiraceae     |  g__                |  s__            |
| K00998 | 9Y-June1 | 193359  | 1                  | 1.33                 | 1.33                  | 0.0005                      | 0.0000                          | k__Bacteria |  p__Bacteroidetes   |  c__Bacteroidia      |  o__Bacteroidales      |  f__S24-7               |  g__                |  s__            |
| K00998 | 9Y-June1 | 528756  | 1                  | 1.33                 | 1.33                  | 0.0005                      | 0.0000                          | k__Bacteria |  p__Bacteroidetes   |  c__Bacteroidia      |  o__Bacteroidales      |  f__S24-7               |  g__                |  s__            |

To explore the result data we can make uso of R and ggplot:

```{r}
install.packege("ggplots2")
library(ggplot2)
setwd("~/Documents/unit_5")
df <- read.table(file = 'metagenome_contributions.txt', sep = '\t', header = TRUE)
ggplot(aes(y = ContributionPercentOfSample, x = Gene, fill = Phylum), data = df) + geom_bar( stat="identity")
```
![imagen](https://user-images.githubusercontent.com/13121779/167165031-561ebe0c-d691-492f-80b8-3a0012d4dc9a.png)

We can explore at different taxonomic level (Order, Family, Genus, etc.)

***





