install.packages("ggpicrust2")



https://github.com/jtamames/SqueezeMeta
https://github.com/jtamames/SqueezeMeta/wiki/Using-R-to-analyze-your-SQM-results
BiocManager::install("SQMtools")
library('SQMtools')



packages <- list.files("/home/metag/R/x86_64-pc-linux-gnu-library/4.3/")
df = data.frame()

for (p in packages){
    p_info <- packageDescription(p, fields = c("Package", "Title", "Version"))
    row <- c(p_info$Package, p_info$Title, p_info$Version) 
    df <- rbind(df, row)
}
colnames(df) <- c("Name", "Description", "version")
write.table(df, "tmp.txt", append = FALSE, sep = "\t", quote = FALSE, row.names = FALSE)


