## Script to create functional enrichment plots from lists of Uniprot IDs using clusterProfiler library

library(clusterProfiler)
library(ggplot2)
library(org.Hs.eg.db)
library(org.Bt.eg.db)

# From humanppi_vs_pdb.ipynb
gene <- scan("/Users/stromjoe/Documents/humanppi_nohit_uniprots.txt", character(), sep=",")
edo <- enrichGO(gene=gene, OrgDb='org.Hs.eg.db', keyType="UNIPROT", ont="ALL", pool=TRUE)
q <- mutate(edo, qscore = -log(p.adjust, base=10)) |> barplot(x="qscore")
q <- q + theme(axis.text.x = element_text(size=12, family = "sans"),
                 axis.text.y = element_text(size=12, family = "sans"),
                 legend.text = element_text(size=12, family="sans"),
                 legend.title = element_text(size=12, family="sans"),
                 panel.background = element_blank(),
                 aspect.ratio = 2/1,
                 plot.margin = unit(c(0,0,0,2.5),"cm"))
q
png(file="/Volumes/imb-luckgr/projects/interface_clustering/visualizations/plots/humanppi_novelclust_goenrich.png", width=600, height=600)
q
dev.off()
pdf(file="/Volumes/imb-luckgr/projects/interface_clustering/visualizations/plots/humanppi_novelclust_goenrich.pdf")
q
dev.off()

# From figure3.ipynb
gene <- scan("/Users/stromjoe/Documents/helical_cluster_uniprots_Bt.txt", character(), sep=",")
edo <- enrichGO(gene=gene, OrgDb='org.Bt.eg.db', keyType="UNIPROT", ont="ALL", pool=TRUE)
q <- mutate(edo, qscore = -log(p.adjust, base=10)) |> barplot(x="qscore")
q <- q + theme(axis.text.x = element_text(size=12, family = "sans"),
               axis.text.y = element_text(size=12, family = "sans"),
               legend.text = element_text(size=12, family="sans"),
               legend.title = element_text(size=12, family="sans"),
               panel.background = element_blank(),
               aspect.ratio = 2/1,
               plot.margin = unit(c(0,0,0,2.5),"cm"))
q
png(file="/Volumes/imb-luckgr/projects/interface_clustering/visualizations/plots/cath-diverse_helical_goenrich.png", width=600, height=600)
q
dev.off()
pdf(file="/Volumes/imb-luckgr/projects/interface_clustering/visualizations/plots/cath-diverse_helical_goenrich.pdf")
q
dev.off()

# From figure3.ipynb
gene <- scan("/Users/stromjoe/Documents/strand_cluster_uniprots_Hs.txt", character(), sep=",")
edo <- enrichGO(gene=gene, OrgDb='org.Hs.eg.db', keyType="UNIPROT", ont="ALL", pool=TRUE)
q <- mutate(edo, qscore = -log(p.adjust, base=10)) |> barplot(x="qscore")
q <- q + theme(axis.text.x = element_text(size=12, family = "sans"),
               axis.text.y = element_text(size=12, family = "sans"),
               legend.text = element_text(size=12, family="sans"),
               legend.title = element_text(size=12, family="sans"),
               panel.background = element_blank(),
               aspect.ratio = 2/1,
               plot.margin = unit(c(0,0,0,2.5),"cm"))
q
png(file="/Volumes/imb-luckgr/projects/interface_clustering/visualizations/plots/cath-diverse_strand_goenrich.png", width=600, height=600)
q
dev.off()
pdf(file="/Volumes/imb-luckgr/projects/interface_clustering/visualizations/plots/cath-diverse_strand_goenrich.pdf")
q
dev.off()
