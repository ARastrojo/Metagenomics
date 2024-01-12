```{r}
# install.package("ggplots2")
library(ggplot2)
setwd("/home/metag/Documents/unit_5")
df <- read.table(file = 'metagenome_contributions.txt', sep = '\t', header = TRUE)
ggplot(aes(y = ContributionPercentOfSample, x = Gene, fill = Phylum), data = df) + geom_bar( stat="identity")
```