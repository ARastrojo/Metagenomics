Channels:
 - bioconda
 - conda-forge
 - defaults
Platform: linux-64
Collecting package metadata (repodata.json): done
Solving environment: - warning  libmamba Added empty dependency for problem type SOLVER_RULE_UPDATE
failed

LibMambaUnsatisfiableError: Encountered problems while solving:
  - package bowtie2-2.2.1-py27h2bce143_4 requires python >=2.7,<2.8.0a0, but none of the providers can be installed

Could not solve for environment specs
The following packages are incompatible
\u251c\u2500 bowtie2 is installable with the potential options
\u2502  \u251c\u2500 bowtie2 [2.2.1|2.2.4|...|2.3.5.1] would require
\u2502  \u2502  \u2514\u2500 python [2.7* |>=2.7,<2.8.0a0 ], which can be installed;
\u2502  \u251c\u2500 bowtie2 [2.2.1|2.2.4|...|2.3.4.3] would require
\u2502  \u2502  \u2514\u2500 python [3.5* |>=3.5,<3.6.0a0 ], which can be installed;
\u2502  \u251c\u2500 bowtie2 [2.2.1|2.2.4|...|2.5.1] would require
\u2502  \u2502  \u2514\u2500 python >=3.6,<3.7.0a0 , which can be installed;
\u2502  \u251c\u2500 bowtie2 [2.2.1|2.2.4|...|2.5.1] would require
\u2502  \u2502  \u2514\u2500 python >=3.7,<3.8.0a0 , which can be installed;
\u2502  \u251c\u2500 bowtie2 [2.2.1|2.2.4|...|2.5.2] would require
\u2502  \u2502  \u2514\u2500 python >=3.8,<3.9.0a0 , which can be installed;
\u2502  \u251c\u2500 bowtie2 [2.2.1|2.2.4|...|2.5.2] would require
\u2502  \u2502  \u2514\u2500 python >=3.9,<3.10.0a0 , which can be installed;
\u2502  \u251c\u2500 bowtie2 [2.2.4|2.2.5|...|2.3.0] would require
\u2502  \u2502  \u2514\u2500 python 3.4* , which can be installed;
\u2502  \u251c\u2500 bowtie2 [2.2.4|2.2.5|...|2.3.4.1] would require
\u2502  \u2502  \u2514\u2500 python 3.6* , which can be installed;
\u2502  \u2514\u2500 bowtie2 [2.4.5|2.5.0|2.5.1|2.5.2] would require
\u2502     \u2514\u2500 python >=3.10,<3.11.0a0 , which can be installed;
\u2514\u2500 pin-1 is not installable because it requires
   \u2514\u2500 python 3.11.* , which conflicts with any installable versions previously reported.

Pins seem to be involved in the conflict. Currently pinned specs:
 - python 3.11.* (labeled as 'pin-1')
