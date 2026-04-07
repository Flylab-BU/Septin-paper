library(bio3d)

mypdbfile <- "/Volumes/My_Passport/myoc/run_results/final_dcds/olf_mut_365K/step3_input.pdb"
mydcdfile <- "/Volumes/My_Passport/myoc/run_results/final_dcds/olf_mut_365K/step5_5.dcd"

dcd <- read.dcd(mydcdfile)
pdb <- read.pdb(mypdbfile)

ca.inds <- atom.select(pdb, elety="CA")

xyz <- fit.xyz(fixed=pdb$xyz, mobile=dcd,
               fixed.inds=ca.inds$xyz,
               mobile.inds=ca.inds$xyz)

pc <- pca.xyz(xyz[,ca.inds$xyz])
plot(pc, col=bwr.colors(nrow(xyz)) )