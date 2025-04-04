# Preparing Virtual Machine / local machine

Install [Xubuntu 22.04.3 LTS](https://cdimages.ubuntu.com/xubuntu/releases/22.04/release/xubuntu-22.04.3-desktop-amd64.iso) in a virtual machine using VirtualBox (2 cores, 4 Gb of RAM and 50 Gb disk space) or in your local machine.

```
# Some updates
sudo apt-get update
sudo apt-get install gcc
sudo apt-get install make
```
***
# Install Miniconda

```
wget https://repo.anaconda.com/miniconda/Miniconda3-py311_23.10.0-1-Linux-x86_64.sh
chmod +x Miniconda3-py311_23.10.0-1-Linux-x86_64.sh
bash Miniconda3-py311_23.10.0-1-Linux-x86_64.sh
```

**Miniconda activation**

By default, after Miniconda installation introduce the following code automatically in _.bashrc_ file to start conda at the terminal startup. However, for an unknown reason, in Xubuntu this does not occur. So, to get conda initialized at _terminal_ startup we need to included the following code at the end of _.bashrc_: 

```
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/metag/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
	eval "$__conda_setup"
else
	if [ -f "/home/metag/miniconda3/etc/profile.d/conda.sh" ]; then
    	. "/home/metag/miniconda3/etc/profile.d/conda.sh"
	else
    	export PATH="/home/metag/miniconda3/bin:$PATH"
	fi
fi
unset __conda_setup
# <<< conda initialize <<<
```

Then, restart _terminal_ window and conda should be initialized. 

**Conda channels**

```bash
conda config --add channels bioconda
conda config --add channels default
conda config --add channels conda-forge
```

## Install Mamba

Mamba is a tool running on Conda that can be used to install packages. It's usually quicker than conda to install programs, and we only need to change the _conda_ word by _mamba_. 

``` bash
conda install -c conda-forge mamba

# In the syntaxis we can also used the following command
# conda install conda-forge::mamba
```

**Other additional software**

```bash
# To download data from GoogleDrive using command line
pip install gdown
# pip is the default python packages manager (similar to conda, but only for python)
```

```bash
# GNU version of the awk program
sudo apt-get install gawk
```

## Installing system libraries needed for some R packages

### Curl

``` bash
sudo apt-get install libcurl4-gnutls-dev
```

### XML2-lib

``` bash
sudo apt-get install libxml2-dev
```

### libfontconfig1-dev

``` bash
sudo apt-get install libfontconfig1-dev
```

### libcairo2-dev

``` bash
sudo apt-get install libcairo2-dev
```

## Installing conda environments and the required programs

<!--### Qiime2

Follow instructions from [Qiime2 manual](https://docs.qiime2.org/2023.9/install/native/#miniconda):

```bash
# Update and install wget
conda update conda
conda install wget
# Installing Qiime2
wget https://raw.githubusercontent.com/qiime2/distributions/dev/latest/passed/qiime2-amplicon-ubuntu-latest-conda.yml
conda env create -n qiime2-dev --file qiime2-amplicon-ubuntu-latest-conda.yml
rm qiime2-amplicon-ubuntu-latest-conda.yml
```
-->

### Cutadapt

Tool to remove primers or specific sequences from reads in fastq files
``` bash
conda create -n cutadaptenv -c bioconda cutadapt
```

### Fasttree2

Tool to calculate ML phylogenetic trees from sequence alignments
``` bash
conda install -c bioconda fasttree
```

### Picrust (v1)

```bash
conda create -n picrust
conda install -c bioconda picrust

# Download pre-computed database files
conda activate picrust
download_picrust_files.py
conda deactivate

# Database files can also be download from picrust webpage (https://picrust.github.io/picrust/picrust_precalculated_files.html)

# Database file is located in $HOME/miniconda3/envs/picrust/lib/python2.7/site-packages/picrust/data
```

If standard installation fails, you can try to install picrust by using _conda pack_:
```bash
# Download pre-installed picrust enviroment 
gdown 1CTpbRgrSWT40dlajjM6HU-524dQow0SJ
# md5 (picrust.tar.gz) = bb1f8a85d1057927bc09fea92ce02ff7
mkdir /home/${USER}/miniconda3/envs/picrust
tar -xzf picrust.tar.gz -C /home/${USER}/miniconda3/envs/picrust
```

<!--### Picrust2

```bash
mamba create -n picrust2 -c bioconda -c conda-forge picrust2=2.5.2
```
-->

### STAMP

This program is out of date and cannot be installed using _conda_ because uses python v2.7 which is no longer maintained. Although some python v2.7 can be used, in this case STAMP requires a library (pyQt4) which is not avaible. But we can _clone_  the  _conda environment_ created when all libraries were availble by using _conda-pack_ (see Tips before starting for more details). 

```bash
gdown 1ANLUfRcoudLWH40CFUomd0Ma50h4mAAn
# md5 (stamp.tar.gz) = 3160a72c735bf6fe6a391ce5b749bba1
mkdir /home/metag/miniconda3/envs/stamp
tar -xzf stamp.tar.gz -C /home/metag/miniconda3/envs/stamp
```

***
# R and RStudio

- [Installing R](https://cran.r-project.org/bin/linux/ubuntu/fullREADME.html) 
```bash
sudo apt-get update
sudo apt-get install r-base
sudo apt-get install r-base-dev
```

- [Installing  most updated R](https://cran.r-project.org/bin/linux/ubuntu/)

Ubuntu repositories do not contain the latest stable version for R. To get it, we have to add a security key and a repository to bypass Ubuntu list.

``` bash
# update indices
sudo apt-get update -qq
# install two helper packages we need
sudo apt-get install --no-install-recommends software-properties-common dirmngr
# add the signing key (by Michael Rutter) for these repos
# To verify key, run gpg --show-keys /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc 
# Fingerprint: E298A3A825C0D65DFD57CBB651716619E084DAB9
wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | sudo tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc
# add the R 4.0 repo from CRAN -- adjust 'focal' to 'groovy' or 'bionic' (Ubuntu version) using $(lsb_release -cs)
sudo add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"

# installing r-base and developer tools
sudo apt-get install r-base
sudo apt-get install r-base-dev
```
- [RStudio](https://posit.co/download/rstudio-desktop/)

Download the correct version from [here](https://download1.rstudio.org/electron/jammy/amd64/rstudio-2023.09.1-494-amd64.deb) and follow installation instructions.

## R Packages

Currently, User libraries are stored at */home/metag/R/x86_64-pc-linux-gnu-library/4.3* (4.3 in this case is the R version we have in our system).

### Pavian (for Kraken2 results visualization)
This package additionaly install some packages that we are going to use such as ggplot2 or tidyr. 
```R
if (!require(remotes)) { install.packages("remotes") }
remotes::install_github("fbreitwieser/pavian")
```

#### SQMtools (for SqueezeMeta results visualization)
``` R
if (!require("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("SQMtools")
```

### Installing Bioconductor

Many packages related to bioinformatic analysis are available from [Bioconductor](https://www.bioconductor.org/) platfform. Let's install it. At the moment of preparing this document the Bioconductor version was 3.18

``` R
if (!require("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install(version = "3.18")
```

### 16S Analysis Packages

#### DADA2 for Amplicon Sequence Variants (ASVs) determination
``` R
BiocManager::install("dada2")
```

#### DECIPHER for sequence comparisons
``` R
BiocManager::install("DECIPHER")
```

#### Phyloseq for analysis of community composition
``` R
BiocManager::install("phyloseq")
```

#### Microbiome, additional tools to study community composition based on Phyloseq
``` R
BiocManager::install("microbiome")
```

#### DESeq2, to study differential community enrichment
``` R
BiocManager::install("DESeq2")
```

#### Agricolae, Statistical Procedures for Agricultural Research
``` R
install.packages("agricolae") 
```

### Dataframe manipulation

Dataframes can be manipulated with the packages defined in tidyverse such as dplyr, tidyr and tibble and readr. All of them except readr have been already installed as dependencies of the previous packages.

``` R
install.packages("readr")
```

### Graphical packages

Most of the graphical results are going to be plotted using ggplot2, which we are not going to install as when installing Pavian the package was installed. Nevertheless, we need additional packages

#### hrbrthenmes, an easy tool to stablish scales in plots

``` R
install.packages("hrbrthemes")
```

#### Plotly, to create html interactive plots

``` R
install.packages("plotly")
```

### List of packages and description

Packages in library ‘/home/metag/R/x86_64-pc-linux-gnu-library/4.3’:
```r
packages <- list.files("/home/metag/R/x86_64-pc-linux-gnu-library/4.3/")
df = data.frame()

for (p in packages){
    p_info <- packageDescription(p, fields = c("Package", "Title", "Version"))
    row <- c(p_info$Package, p_info$Title, p_info$Version) 
    df <- rbind(df, row)
}
colnames(df) <- c("Name", "Description", "version")
write.table(df, "tmp.txt", append = FALSE, sep = "\t", quote = FALSE, row.names = FALSE)
```



| Name                 | Description                                                                                               | version    |
|----------------------|-----------------------------------------------------------------------------------------------------------|------------|
| abind                | Combine Multidimensional Arrays                                                                           | 1.4-5      |
| ade4                 | Analysis of Ecological Data: Exploratory and Euclidean Methods in Environmental Sciences                  | 1.7-22     |
| agricolae            | Statistical Procedures for Agricultural Research                                                          | 1.3-7      |
| AlgDesign            | Algorithmic Experimental Design                                                                           | 1.2.1      |
| AnnotationDbi        | Manipulation of SQLite-based annotations in Bioconductor                                                  | 1.64.1     |
| anytime              | Anything to 'POSIXct' or 'Date' Converter                                                                 | 0.3.9      |
| ape                  | Analyses of Phylogenetics and Evolution                                                                   | 5.7-1      |
| askpass              | Password Entry Utilities for R, Git, and SSH                                                              | 1.2.0      |
| backports            | Reimplementations of Functions Introduced Since R-3.0.0                                                   | 1.4.1      |
| base64enc            | Tools for base64 encoding                                                                                 | 0.1-3      |
| bayesm               | Bayesian Inference for Marketing/Micro-Econometrics                                                       | 3.1-6      |
| BH                   | Boost C++ Header Files                                                                                    | 1.84.0-0   |
| Biobase              | Biobase: Base functions for Bioconductor                                                                  | 2.62.0     |
| BiocGenerics         | S4 generic functions used in Bioconductor                                                                 | 0.48.1     |
| BiocManager          | Access the Bioconductor Project Package Repository                                                        | 1.30.22    |
| BiocParallel         | Bioconductor facilities for parallel evaluation                                                           | 1.36.0     |
| BiocVersion          | Set the appropriate version of Bioconductor packages                                                      | 3.18.1     |
| biomformat           | An interface package for the BIOM file format                                                             | 1.30.0     |
| Biostrings           | Efficient manipulation of biological strings                                                              | 2.70.1     |
| bit                  | Classes and Methods for Fast Memory-Efficient Boolean Selections                                          | 4.0.5      |
| bit64                | A S3 Class for Vectors of 64bit Integers                                                                  | 4.0.5      |
| bitops               | Bitwise Operations                                                                                        | 1.0-7      |
| blob                 | A Simple S3 Class for Representing Vectors of Binary Data ('BLOBS')                                       | 1.2.4      |
| brew                 | Templating Framework for Report Generation                                                                | 1.0-10     |
| brio                 | Basic R Input Output                                                                                      | 1.1.4      |
| bslib                | Custom 'Bootstrap' 'Sass' Themes for 'shiny' and 'rmarkdown'                                              | 0.6.1      |
| cachem               | Cache R Objects with Automatic Pruning                                                                    | 1.0.8      |
| callr                | Call R from R                                                                                             | 3.7.3      |
| cli                  | Helpers for Developing Command Line Interfaces                                                            | 3.6.2      |
| clipr                | Read and Write from the System Clipboard                                                                  | 0.8.0      |
| colorspace           | A Toolbox for Manipulating and Assessing Colors and Palettes                                              | 2.1-0      |
| commonmark           | High Performance CommonMark and Github Markdown Rendering in R                                            | 1.9.0      |
| compositions         | Compositional Data Analysis                                                                               | 2.0-7      |
| cpp11                | A C++11 Interface for R's C Interface                                                                     | 0.4.7      |
| crayon               | Colored Terminal Output                                                                                   | 1.5.2      |
| credentials          | Tools for Managing SSH and Git Credentials                                                                | 2.0.1      |
| crosstalk            | Inter-Widget Interactivity for HTML Widgets                                                               | 1.2.1      |
| crul                 | HTTP Client                                                                                               | 1.4.0      |
| curl                 | A Modern and Flexible Web Client for R                                                                    | 5.2.0      |
| d3r                  | 'd3.js' Utilities for R                                                                                   | 1.1.0      |
| dada2                | Accurate, high-resolution sample inference from amplicon sequencing data                                  | 1.30.0     |
| data.table           | Extension of `data.frame`                                                                                 | 1.14.10    |
| DBI                  | R Database Interface                                                                                      | 1.2.1      |
| DECIPHER             | Tools for curating, analyzing, and manipulating biological sequences                                      | 2.30.0     |
| DelayedArray         | A unified framework for working transparently with on-disk and in-memory array-like datasets              | 0.28.0     |
| deldir               | Delaunay Triangulation and Dirichlet (Voronoi) Tessellation                                               | 2.0-2      |
| DEoptimR             | Differential Evolution Optimization in Pure R                                                             | 1.1-3      |
| desc                 | Manipulate DESCRIPTION Files                                                                              | 1.4.3      |
| DESeq2               | Differential gene expression analysis based on the negative binomial distribution                         | 1.42.0     |
| diffobj              | Diffs for R Objects                                                                                       | 0.3.5      |
| digest               | Create Compact Hash Digests of R Objects                                                                  | 0.6.34     |
| downlit              | Syntax Highlighting and Automatic Linking                                                                 | 0.4.3      |
| dplyr                | A Grammar of Data Manipulation                                                                            | 1.1.4      |
| DT                   | A Wrapper of the JavaScript Library 'DataTables'                                                          | 0.31       |
| ellipsis             | Tools for Working with ...                                                                                | 0.3.2      |
| evaluate             | Parsing and Evaluation Tools that Provide More Details than the Default                                   | 0.23       |
| extrafont            | Tools for Using Fonts                                                                                     | 0.19       |
| extrafontdb          | Package for holding the database for the extrafont package                                                | 1.0        |
| fansi                | ANSI Control Sequence Aware String Functions                                                              | 1.0.6      |
| farver               | High Performance Colour Space Manipulation                                                                | 2.1.1      |
| fastmap              | Fast Data Structures                                                                                      | 1.1.1      |
| fontawesome          | Easily Work with 'Font Awesome' Icons                                                                     | 0.5.2      |
| fontBitstreamVera    | Fonts with 'Bitstream Vera Fonts' License                                                                 | 0.1.1      |
| fontLiberation       | Liberation Fonts                                                                                          | 0.1.0      |
| fontquiver           | Set of Installed Fonts                                                                                    | 0.2.1      |
| foreach              | Provides Foreach Looping Construct                                                                        | 1.5.2      |
| formatR              | Format R Code Automatically                                                                               | 1.14       |
| fs                   | Cross-Platform File System Operations Based on 'libuv'                                                    | 1.6.3      |
| futile.logger        | A Logging Utility for R                                                                                   | 1.4.3      |
| futile.options       | Futile Options Management                                                                                 | 1.0.1      |
| gdtools              | Utilities for Graphical Rendering and Fonts Management                                                    | 0.3.5      |
| generics             | Common S3 Generics not Provided by Base R Methods Related to Model Fitting                                | 0.1.3      |
| GenomeInfoDb         | Utilities for manipulating chromosome names, including modifying them to follow a particular naming style | 1.38.5     |
| GenomeInfoDbData     | Species and taxonomy ID look up tables used by GenomeInfoDb                                               | 1.2.11     |
| GenomicAlignments    | Representation and manipulation of short genomic alignments                                               | 1.38.1     |
| GenomicRanges        | Representation and manipulation of genomic intervals                                                      | 1.54.1     |
| gert                 | Simple Git Client for R                                                                                   | 2.0.1      |
| gfonts               | Offline 'Google' Fonts for 'Markdown' and 'Shiny'                                                         | 0.2.0      |
| ggplot2              | Create Elegant Data Visualisations Using the Grammar of Graphics                                          | 3.4.4      |
| gh                   | 'GitHub' 'API'                                                                                            | 1.4.0      |
| gitcreds             | Query 'git' Credentials from 'R'                                                                          | 0.1.2      |
| glue                 | Interpreted String Literals                                                                               | 1.7.0      |
| graph                | graph: A package to handle graph data structures                                                          | 1.80.0     |
| gss                  | General Smoothing Splines                                                                                 | 2.2-7      |
| gtable               | Arrange 'Grobs' in Tables                                                                                 | 0.3.4      |
| highr                | Syntax Highlighting for R Source Code                                                                     | 0.10       |
| hms                  | Pretty Time of Day                                                                                        | 1.1.3      |
| hrbrthemes           | Additional Themes, Theme Components and Utilities for 'ggplot2'                                           | 0.8.0      |
| htmltools            | Tools for HTML                                                                                            | 0.5.7      |
| htmlwidgets          | HTML Widgets for R                                                                                        | 1.6.4      |
| httpcode             | 'HTTP' Status Code Helper                                                                                 | 0.3.0      |
| httpuv               | HTTP and WebSocket Server Library                                                                         | 1.6.13     |
| httr                 | Tools for Working with URLs and HTTP                                                                      | 1.4.7      |
| httr2                | Perform HTTP Requests and Process the Responses                                                           | 1.0.0      |
| hwriter              | HTML Writer - Outputs R Objects in HTML Format                                                            | 1.3.2.1    |
| igraph               | Network Analysis and Visualization                                                                        | 1.6.0      |
| ini                  | Read and Write '.ini' Files                                                                               | 0.3.1      |
| interp               | Interpolation Methods                                                                                     | 1.1-5      |
| IRanges              | Foundation of integer range manipulation in Bioconductor                                                  | 2.36.0     |
| isoband              | Generate Isolines and Isobands from Regularly Spaced Elevation Grids                                      | 0.2.7      |
| iterators            | Provides Iterator Construct                                                                               | 1.0.14     |
| jpeg                 | Read and write JPEG images                                                                                | 0.1-10     |
| jquerylib            | Obtain 'jQuery' as an HTML Dependency Object                                                              | 0.1.4      |
| jsonlite             | A Simple and Robust JSON Parser and Generator for R                                                       | 1.8.8      |
| KEGGgraph            | KEGGgraph: A graph approach to KEGG PATHWAY in R and Bioconductor                                         | 1.62.0     |
| KEGGREST             | Client-side REST access to the Kyoto Encyclopedia of Genes and Genomes (KEGG)                             | 1.42.0     |
| knitr                | A General-Purpose Package for Dynamic Report Generation in R                                              | 1.45       |
| labeling             | Axis Labeling                                                                                             | 0.4.3      |
| lambda.r             | Modeling Data with Functional Programming                                                                 | 1.2.4      |
| later                | Utilities for Scheduling Functions to Execute Later with Event Loops                                      | 1.3.2      |
| latticeExtra         | Extra Graphical Utilities Based on Lattice                                                                | 0.6-30     |
| lazyeval             | Lazy (Non-Standard) Evaluation                                                                            | 0.2.2      |
| lifecycle            | Manage the Life Cycle of your Package Functions                                                           | 1.0.4      |
| locfit               | Local Regression, Likelihood and Density Estimation                                                       | 1.5-9.8    |
| magrittr             | A Forward-Pipe Operator for R                                                                             | 2.0.3      |
| MatrixGenerics       | S4 Generic Summary Statistic Functions that Operate on Matrix-Like Objects                                | 1.14.0     |
| matrixStats          | Functions that Apply to Rows and Columns of Matrices (and to Vectors)                                     | 1.2.0      |
| memoise              | 'Memoisation' of Functions                                                                                | 2.0.1      |
| microbiome           | Microbiome Analytics                                                                                      | 1.24.0     |
| mime                 | Map Filenames to MIME Types                                                                               | 0.12       |
| miniUI               | Shiny UI Widgets for Small Screens                                                                        | 0.1.1.1    |
| minqa                | Derivative-Free Optimization Algorithms by Quadratic Approximation                                        | 1.2.6      |
| multtest             | Resampling-based multiple hypothesis testing                                                              | 2.58.0     |
| munsell              | Utilities for Using Munsell Colours                                                                       | 0.5.0      |
| openssl              | Toolkit for Encryption, Signatures and Certificates Based on OpenSSL                                      | 2.1.1      |
| org.Hs.eg.db         | Genome wide annotation for Human                                                                          | 3.18.0     |
| pathview             | a tool set for pathway based data integration and visualization                                           | 1.42.0     |
| pavian               | Visualize and analyze metagenomics classification results                                                 | 1.2.1      |
| permute              | Functions for Generating Restricted Permutations of Data                                                  | 0.9-7      |
| phyloseq             | Handling and analysis of high-throughput microbiome census data                                           | 1.46.0     |
| pillar               | Coloured Formatting for Columns                                                                           | 1.9.0      |
| pixmap               | Bitmap Images / Pixel Maps                                                                                | 0.4-12     |
| pkgbuild             | Find Tools Needed to Build R Packages                                                                     | 1.4.3      |
| pkgconfig            | Private Configuration for 'R' Packages                                                                    | 2.0.3      |
| pkgload              | Simulate Package Installation and Attach                                                                  | 1.3.3      |
| plogr                | The 'plog' C++ Logging Library                                                                            | 0.2.0      |
| plotly               | Create Interactive Web Graphics via 'plotly.js'                                                           | 4.10.3     |
| plyr                 | Tools for Splitting, Applying and Combining Data                                                          | 1.8.9      |
| png                  | Read and write PNG images                                                                                 | 0.1-8      |
| praise               | Praise Users                                                                                              | 1.0.0      |
| prettyunits          | Pretty, Human Readable Formatting of Quantities                                                           | 1.2.0      |
| processx             | Execute and Control System Processes                                                                      | 3.8.3      |
| profvis              | Interactive Visualizations for Profiling R Code                                                           | 0.3.8      |
| progress             | Terminal Progress Bars                                                                                    | 1.2.3      |
| promises             | Abstractions for Promise-Based Asynchronous Programming                                                   | 1.2.1      |
| ps                   | List, Query, Manipulate System Processes                                                                  | 1.7.5      |
| purrr                | Functional Programming Tools                                                                              | 1.0.2      |
| R6                   | Encapsulated Classes with Reference Semantics                                                             | 2.5.1      |
| rappdirs             | Application Directories: Determine Where to Save Data, Caches, and Logs                                   | 0.3.3      |
| rcmdcheck            | Run 'R CMD check' from 'R' and Capture Results                                                            | 1.4.0      |
| RColorBrewer         | ColorBrewer Palettes                                                                                      | 1.1-3      |
| Rcpp                 | Seamless R and C++ Integration                                                                            | 1.0.12     |
| RcppArmadillo        | 'Rcpp' Integration for the 'Armadillo' Templated Linear Algebra Library                                   | 0.12.6.6.1 |
| RcppEigen            | 'Rcpp' Integration for the 'Eigen' Templated Linear Algebra Library                                       | 0.3.3.9.4  |
| RcppParallel         | Parallel Programming Tools for 'Rcpp'                                                                     | 5.1.7      |
| RCurl                | General Network (HTTP/FTP/...) Client Interface for R                                                     | 1.98-1.14  |
| readr                | Read Rectangular Text Data                                                                                | 2.1.5      |
| rematch2             | Tidy Output from Regular Expression Matching                                                              | 2.1.2      |
| remotes              | R Package Installation from Remote Repositories, Including 'GitHub'                                       | 2.4.2.1    |
| reshape2             | Flexibly Reshape Data: A Reboot of the Reshape Package                                                    | 1.4.4      |
| Rgraphviz            | Provides plotting capabilities for R graph objects                                                        | 2.46.0     |
| rhandsontable        | Interface to the 'Handsontable.js' Library                                                                | 0.3.8      |
| rhdf5                | R Interface to HDF5                                                                                       | 2.46.1     |
| rhdf5filters         | HDF5 Compression Filters                                                                                  | 1.14.1     |
| Rhdf5lib             | hdf5 library as an R package                                                                              | 1.24.1     |
| Rhtslib              | HTSlib high-throughput sequencing library as an R package                                                 | 2.4.0      |
| rlang                | Functions for Base Types and Core R and 'Tidyverse' Features                                              | 1.1.3      |
| rmarkdown            | Dynamic Documents for R                                                                                   | 2.25       |
| rmutil               | Utilities for Nonlinear Regression and Repeated Measurements Models                                       | 1.1.10     |
| robustbase           | Basic Robust Statistics                                                                                   | 0.99-1     |
| roxygen2             | In-Line Documentation for R                                                                               | 7.3.0      |
| rprojroot            | Finding Files in Project Subdirectories                                                                   | 2.0.4      |
| Rsamtools            | Binary alignment (BAM), FASTA, variant call (BCF), and tabix file import                                  | 2.18.0     |
| RSQLite              | SQLite Interface for R                                                                                    | 2.3.4      |
| rstudioapi           | Safely Access the RStudio API                                                                             | 0.15.0     |
| Rtsne                | T-Distributed Stochastic Neighbor Embedding using a Barnes-Hut Implementation                             | 0.17       |
| Rttf2pt1             | 'ttf2pt1' Program                                                                                         | 1.3.12     |
| rversions            | Query 'R' Versions, Including 'r-release' and 'r-oldrel'                                                  | 2.1.2      |
| S4Arrays             | Foundation of array-like containers in Bioconductor                                                       | 1.2.0      |
| S4Vectors            | Foundation of vector-like and list-like containers in Bioconductor                                        | 0.40.2     |
| sankeyD3             | D3 JavaScript Sankey Graphs from R                                                                        | 0.3.2      |
| sass                 | Syntactically Awesome Style Sheets ('Sass')                                                               | 0.4.8      |
| scales               | Scale Functions for Visualization                                                                         | 1.3.0      |
| sessioninfo          | R Session Information                                                                                     | 1.2.2      |
| shiny                | Web Application Framework for R                                                                           | 1.8.0      |
| shinydashboard       | Create Dashboards with 'Shiny'                                                                            | 0.7.2      |
| shinyFileTree        | Directory tree for R/Shiny                                                                                | 0.0.0.9000 |
| shinyjs              | Easily Improve the User Experience of Your Shiny Apps in Seconds                                          | 2.1.0      |
| shinyWidgets         | Custom Inputs Widgets for Shiny                                                                           | 0.8.1      |
| ShortRead            | FASTQ input and manipulation                                                                              | 1.60.0     |
| snow                 | Simple Network of Workstations                                                                            | 0.4-4      |
| sourcetools          | Tools for Reading, Tokenizing and Parsing R Code                                                          | 0.1.7-1    |
| sp                   | Classes and Methods for Spatial Data                                                                      | 2.1-2      |
| SparseArray          | Efficient in-memory representation of multidimensional sparse arrays                                      | 1.2.3      |
| SQMtools             | Analyze Results Generated by the 'SqueezeMeta' Pipeline                                                   | 1.6.3      |
| stringi              | Fast and Portable Character String Processing Facilities                                                  | 1.8.3      |
| stringr              | Simple, Consistent Wrappers for Common String Operations                                                  | 1.5.1      |
| SummarizedExperiment | SummarizedExperiment container                                                                            | 1.32.0     |
| sys                  | Powerful and Reliable Tools for Running System Commands in R                                              | 3.4.2      |
| systemfonts          | System Native Font Finding                                                                                | 1.0.5      |
| tensorA              | Advanced Tensor Arithmetic with Named Indices                                                             | 0.36.2.1   |
| testthat             | Unit Testing for R                                                                                        | 3.2.1      |
| tibble               | Simple Data Frames                                                                                        | 3.2.1      |
| tidyr                | Tidy Messy Data                                                                                           | 1.3.0      |
| tidyselect           | Select from a Set of Strings                                                                              | 1.2.0      |
| timeDate             | Rmetrics - Chronological and Calendar Objects                                                             | 4032.109   |
| tinytex              | Helper Functions to Install and Maintain TeX Live, and Compile LaTeX Documents                            | 0.49       |
| triebeard            | 'Radix' Trees in 'Rcpp'                                                                                   | 0.4.1      |
| tzdb                 | Time Zone Database Information                                                                            | 0.4.0      |
| urlchecker           | Run CRAN URL Checks from Older R Versions                                                                 | 1.0.1      |
| urltools             | Vectorised Tools for URL Handling and Parsing                                                             | 1.7.3      |
| usethis              | Automate Package and Project Setup                                                                        | 2.2.2      |
| utf8                 | Unicode Text Processing                                                                                   | 1.2.4      |
| vctrs                | Vector Helpers                                                                                            | 0.6.5      |
| vegan                | Community Ecology Package                                                                                 | 2.6-4      |
| viridisLite          | Colorblind-Friendly Color Maps (Lite Version)                                                             | 0.4.2      |
| vroom                | Read and Write Rectangular Text Data Quickly                                                              | 1.6.5      |
| waldo                | Find Differences Between R Objects                                                                        | 0.5.2      |
| whisker              | {{mustache}} for R, Logicless Templating                                                                  | 0.4.1      |
| withr                | Run Code 'With' Temporarily Modified Global State                                                         | 2.5.2      |
| xfun                 | Supporting Functions for Packages Maintained by 'Yihui Xie'                                               | 0.41       |
| XML                  | Tools for Parsing and Generating XML Within R and S-Plus                                                  | 3.99-0.16  |
| xml2                 | Parse XML                                                                                                 | 1.3.6      |
| xopen                | Open System Files, 'URLs', Anything                                                                       | 1.0.0      |
| xtable               | Export Tables to LaTeX or HTML                                                                            | 1.8-4      |
| XVector              | Foundation of external vector representation and manipulation in Bioconductor                             | 0.42.0     |
| yaml                 | Methods to Convert R Data to YAML and Back                                                                | 2.3.8      |
| zip                  | Cross-Platform 'zip' Compression                                                                          | 2.3.0      |
| zlibbioc             | An R packaged zlib-1.2.5                                                                                  | 1.48.0     |
