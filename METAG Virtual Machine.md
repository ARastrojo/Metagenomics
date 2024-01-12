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
chmod +x Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
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

Mamba is a tool running on Conda that can be used to install packages 

``` bash
conda install conda-forge::mamba
```

**Other additional software**

```bash
# To download data from GoogleDrive using command line
pip install gdown
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

### Qiime2

Follow instructions from [Qiime2 manual](https://docs.qiime2.org/2023.9/install/native/#miniconda):

```bash
# Update and install wget
conda update conda
conda install wget
# Installing Qiime2
wget https://data.qiime2.org/distro/amplicon/qiime2-amplicon-2023.9-py38-linux-conda.yml
conda env create -n qiime --file qiime2-amplicon-2023.9-py38-linux-conda.yml
rm qiime2-amplicon-2023.9-py38-linux-conda.yml
```

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
sudo apt update -qq
# install two helper packages we need
sudo apt install --no-install-recommends software-properties-common dirmngr
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

### Pavian (for Kraken2 results visualizarion)
This package additionaly install some packages that we are going to use such as ggplot2 or tidyr

```R
if (!require(remotes)) { install.packages("remotes") }
remotes::install_github("fbreitwieser/pavian")
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

|Package                                       | Description                                                    |
|----------------------------------------------|----------------------------------------------------------------|
| abind                                        | Combine Multidimensional Arrays                                |
| ade4                                         | Analysis of Ecological Data: Exploratory and Euclidean Methods |
| anytime                                      | Anything to 'POSIXct' or 'Date' Converter                      |
| ape                                          | Analyses of Phylogenetics and Evolution                        |
| askpass                                      | Password Entry Utilities for R, Git, and SSH                   |
| base64enc                                    | Tools for base64 encoding                                      |
| bayesm                                       | Bayesian Inference for Marketing/Micro-Econometrics            |
| BH                                           | Boost C++ Header Files                                         |
| Biobase                                      | Biobase: Base functions for Bioconductor                       |
| BiocGenerics                                 | S4 generic functions used in Bioconductor                      |
| BiocManager                                  | Access the Bioconductor Project Package Repository             |
| BiocParallel                                 | Bioconductor facilities for parallel evaluation                |
| BiocVersion                                  | Set the appropriate version of Bioconductor packages           |
| biomformat                                   | An interface package for the BIOM file format                  |
| Biostrings                                   | Efficient manipulation of biological strings                   |
| bit                                          | Classes and Methods for Fast Memory-Efficient Boolean Selectio |
| bit64                                        | A S3 Class for Vectors of 64bit Integers                       |
| bitops                                       | Bitwise Operations                                             |
| blob                                         | A Simple S3 Class for Representing Vectors of Binary Data ('BL |
| bslib                                        | Custom 'Bootstrap' 'Sass' Themes for 'shiny' and 'rmarkdown'   |
| cachem                                       | Cache R Objects with Automatic Pruning                         |
| cli                                          | Helpers for Developing Command Line Interfaces                 |
| clipr                                        | Read and Write from the System Clipboard                       |
| colorspace                                   | A Toolbox for Manipulating and Assessing Colors and Palettes   |
| commonmark                                   | High Performance CommonMark and Github Markdown Rendering in R |
| compositions                                 | Compositional Data Analysis                                    |
| cpp11                                        | A C++11 Interface for R's C Interface                          |
| crayon                                       | Colored Terminal Output                                        |
| crosstalk                                    | Inter-Widget Interactivity for HTML Widgets                    |
| crul                                         | HTTP Client                                                    |
| curl                                         | A Modern and Flexible Web Client for R                         |
| d3r                                          | 'd3.js' Utilities for R                                        |
| dada2                                        | Accurate, high-resolution sample inference from amplicon seque |
| data.table                                   | Extension of `data.frame`                                      |
| DBI                                          | R Database Interface                                           |
| DECIPHER                                     | Tools for curating, analyzing, and manipulating biological seq |
| DelayedArray                                 | A unified framework for working transparently with on-disk and |
| deldir                                       | Delaunay Triangulation and Dirichlet (Voronoi) Tessellation    |
| DEoptimR                                     | Differential Evolution Optimization in Pure R                  |
| DESeq2                                       | Differential gene expression analysis based on the negative bi |
| digest                                       | Create Compact Hash Digests of R Objects                       |
| dplyr                                        | A Grammar of Data Manipulation                                 |
| DT                                           | A Wrapper of the JavaScript Library 'DataTables'               |
| ellipsis                                     | Tools for Working with ...                                     |
| evaluate                                     | Parsing and Evaluation Tools that Provide More Details than th |
| extrafont                                    | Tools for Using Fonts                                          |
| extrafontdb                                  | Package for holding the database for the extrafont package     |
| fansi                                        | ANSI Control Sequence Aware String Functions                   |
| farver                                       | High Performance Colour Space Manipulation                     |
| fastmap                                      | Fast Data Structures                                           |
| fontawesome                                  | Easily Work with 'Font Awesome' Icons                          |
| fontBitstreamVera                            | Fonts with 'Bitstream Vera Fonts' License                      |
| fontLiberation                               | Liberation Fonts                                               |
| fontquiver                                   | Set of Installed Fonts                                         |
| foreach                                      | Provides Foreach Looping Construct                             |
| formatR                                      | Format R Code Automatically                                    |
| fs                                           | Cross-Platform File System Operations Based on 'libuv'         |
| futile.logger                                | A Logging Utility for R                                        |
| futile.options                               | Futile Options Management                                      |
| gdtools                                      | Utilities for Graphical Rendering and Fonts Management         |
| generics                                     | Common S3 Generics not Provided by Base R Methods Related to M |
| GenomeInfoDb                                 | Utilities for manipulating chromosome names, including modifyi |
| GenomeInfoDbData                             | Species and taxonomy ID look up tables used by GenomeInfoDb    |
| GenomicAlignments                            | Representation and manipulation of short genomic alignments    |
| GenomicRanges                                | Representation and manipulation of genomic intervals           |
| gfonts                                       | Offline 'Google' Fonts for 'Markdown' and 'Shiny'              |
| ggplot2                                      | Create Elegant Data Visualisations Using the Grammar of Graphi |
| glue                                         | Interpreted String Literals                                    |
| gtable                                       | Arrange 'Grobs' in Tables                                      |
| highr                                        | Syntax Highlighting for R Source Code                          |
| hms                                          | Pretty Time of Day                                             |
| hrbrthemes                                   | Additional Themes, Theme Components and Utilities for 'ggplot2 |
| htmltools                                    | Tools for HTML                                                 |
| htmlwidgets                                  | HTML Widgets for R                                             |
| httpcode                                     | 'HTTP' Status Code Helper                                      |
| httpuv                                       | HTTP and WebSocket Server Library                              |
| httr                                         | Tools for Working with URLs and HTTP                           |
| hwriter                                      | HTML Writer - Outputs R Objects in HTML Format                 |
| igraph                                       | Network Analysis and Visualization                             |
| interp                                       | Interpolation Methods                                          |
| IRanges                                      | Foundation of integer range manipulation in Bioconductor       |
| isoband                                      | Generate Isolines and Isobands from Regularly Spaced Elevation |
| iterators                                    | Provides Iterator Construct                                    |
| jpeg                                         | Read and write JPEG images                                     |
| jquerylib                                    | Obtain 'jQuery' as an HTML Dependency Object                   |
| jsonlite                                     | A Simple and Robust JSON Parser and Generator for R            |
| knitr                                        | A General-Purpose Package for Dynamic Report Generation in R   |
| labeling                                     | Axis Labeling                                                  |
| lambda.r                                     | Modeling Data with Functional Programming                      |
| later                                        | Utilities for Scheduling Functions to Execute Later with Event |
| latticeExtra                                 | Extra Graphical Utilities Based on Lattice                     |
| lazyeval                                     | Lazy (Non-Standard) Evaluation                                 |
| lifecycle                                    | Manage the Life Cycle of your Package Functions                |
| locfit                                       | Local Regression, Likelihood and Density Estimation            |
| magrittr                                     | A Forward-Pipe Operator for R                                  |
| MatrixGenerics                               | S4 Generic Summary Statistic Functions that Operate on Matrix- |
| matrixStats                                  | Functions that Apply to Rows and Columns of Matrices (and to V |
| memoise                                      | 'Memoisation' of Functions                                     |
| microbiome                                   | Microbiome Analytics                                           |
| mime                                         | Map Filenames to MIME Types                                    |
| multtest                                     | Resampling-based multiple hypothesis testing                   |
| munsell                                      | Utilities for Using Munsell Colours                            |
| openssl                                      | Toolkit for Encryption, Signatures and Certificates Based on O |
| pavian                                       | Visualize and analyze metagenomics classification results      |
| permute                                      | Functions for Generating Restricted Permutations of Data       |
| phyloseq                                     | Handling and analysis of high-throughput microbiome census dat |
| pillar                                       | Coloured Formatting for Columns                                |
| pixmap                                       | Bitmap Images / Pixel Maps                                     |
| pkgconfig                                    | Private Configuration for 'R' Packages                         |
| plogr                                        | The 'plog' C++ Logging Library                                 |
| plotly                                       | Create Interactive Web Graphics via 'plotly.js'                |
| plyr                                         | Tools for Splitting, Applying and Combining Data               |
| png                                          | Read and write PNG images                                      |
| prettyunits                                  | Pretty, Human Readable Formatting of Quantities                |
| progress                                     | Terminal Progress Bars                                         |
| promises                                     | Abstractions for Promise-Based Asynchronous Programming        |
| purrr                                        | Functional Programming Tools                                   |
| R6                                           | Encapsulated Classes with Reference Semantics                  |
| rappdirs                                     | Application Directories: Determine Where to Save Data, Caches, |
| RColorBrewer                                 | ColorBrewer Palettes                                           |
| Rcpp                                         | Seamless R and C++ Integration                                 |
| RcppArmadillo                                | 'Rcpp' Integration for the 'Armadillo' Templated Linear Algebr |
| RcppEigen                                    | 'Rcpp' Integration for the 'Eigen' Templated Linear Algebra Li |
| RcppParallel                                 | Parallel Programming Tools for 'Rcpp'                          |
| RCurl                                        | General Network (HTTP/FTP/...) Client Interface for R          |
| readr                                        | Read Rectangular Text Data                                     |
| remotes                                      | R Package Installation from Remote Repositories, Including 'Gi |
| reshape2                                     | Flexibly Reshape Data: A Reboot of the Reshape Package         |
| rhandsontable                                | Interface to the 'Handsontable.js' Library                     |
| rhdf5                                        | R Interface to HDF5                                            |
| rhdf5filters                                 | HDF5 Compression Filters                                       |
| Rhdf5lib                                     | hdf5 library as an R package                                   |
| Rhtslib                                      | HTSlib high-throughput sequencing library as an R package      |
| rlang                                        | Functions for Base Types and Core R and 'Tidyverse' Features   |
| rmarkdown                                    | Dynamic Documents for R                                        |
| robustbase                                   | Basic Robust Statistics                                        |
| Rsamtools                                    | Binary alignment (BAM), FASTA, variant call (BCF), and tabix f |
| RSQLite                                      | SQLite Interface for R                                         |
| Rtsne                                        | T-Distributed Stochastic Neighbor Embedding using a Barnes-Hut |
| Rttf2pt1                                     | 'ttf2pt1' Program                                              |
| S4Arrays                                     | Foundation of array-like containers in Bioconductor            |
| S4Vectors                                    | Foundation of vector-like and list-like containers in Biocondu |
| sankeyD3                                     | D3 JavaScript Sankey Graphs from R                             |
| sass                                         | Syntactically Awesome Style Sheets ('Sass')                    |
| scales                                       | Scale Functions for Visualization                              |
| shiny                                        | Web Application Framework for R                                |
| shinydashboard                               | Create Dashboards with 'Shiny'                                 |
| shinyFileTree                                | Directory tree for R/Shiny                                     |
| shinyjs                                      | Easily Improve the User Experience of Your Shiny Apps in Secon |
| shinyWidgets                                 | Custom Inputs Widgets for Shiny                                |
| ShortRead                                    | FASTQ input and manipulation                                   |
| snow                                         | Simple Network of Workstations                                 |
| sourcetools                                  | Tools for Reading, Tokenizing and Parsing R Code               |
| sp                                           | Classes and Methods for Spatial Data                           |
| SparseArray                                  | Efficient in-memory representation of multidimensional sparse  |
| stringi                                      | Fast and Portable Character String Processing Facilities       |
| stringr                                      | Simple, Consistent Wrappers for Common String Operations       |
| SummarizedExperiment                         | SummarizedExperiment container                                 |
| sys                                          | Powerful and Reliable Tools for Running System Commands in R   |
| systemfonts                                  | System Native Font Finding                                     |
| tensorA                                      | Advanced Tensor Arithmetic with Named Indices                  |
| tibble                                       | Simple Data Frames                                             |
| tidyr                                        | Tidy Messy Data                                                |
| tidyselect                                   | Select from a Set of Strings                                   |
| tinytex                                      | Helper Functions to Install and Maintain TeX Live, and Compile |
| triebeard                                    | 'Radix' Trees in 'Rcpp'                                        |
| tzdb                                         | Time Zone Database Information                                 |
| urltools                                     | Vectorised Tools for URL Handling and Parsing                  |
| utf8                                         | Unicode Text Processing                                        |
| vctrs                                        | Vector Helpers                                                 |
| vegan                                        | Community Ecology Package                                      |
| viridisLite                                  | Colorblind-Friendly Color Maps (Lite Version)                  |
| vroom                                        | Read and Write Rectangular Text Data Quickly                   |
| withr                                        | Run Code 'With' Temporarily Modified Global State              |
| xfun                                         | Supporting Functions for Packages Maintained by 'Yihui Xie'    |
| xtable                                       | Export Tables to LaTeX or HTML                                 |
| XVector                                      | Foundation of external vector representation and manipulation  |
| yaml                                         | Methods to Convert R Data to YAML and Back                     |
| zlibbioc                                     | An R packaged zlib-1.2.5                                       |