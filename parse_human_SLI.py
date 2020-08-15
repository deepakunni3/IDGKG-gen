from idg2sl.parsers.blomen_2015_parser import Blomen2015Parser
from idg2sl import *

manual = ManualEntry()
manual_list = manual.get_entries()
print("We got %d manually entered entries." % len(manual_list))

mohni2014 = Mohni2014Parser()
mohni2014_list = mohni2014.parse()
for x in mohni2014_list:
    print(x)
print("[INFO] Shen et al 2017  n= %d SL interactions" % len(mohni2014_list))
exit(0)

shen2017 = Shen2017Parser()
shen2017_list = shen2017.parse()
print("[INFO] Shen et al 2017  n= %d SL interactions" % len(shen2017_list))
exit(0)

han2017 = Han2017Parser()
han2017_list = han2017.parse()
print("[INFO] Han et al 2017  n= %d SL interactions" % len(han2017_list))
exit(0)

wang2017 = Wang2017Parser()
wang2017_list = wang2017.parse()
print("[INFO] Wang et al 2017  n= %d SL interactions" % len(wang2017_list))
exit(0)

srivas2016 = Srivas2016Parser()
srivas2016_list = srivas2016.parse()
print("[INFO] Srivas et al 2016  n= %d SL interactions" % len(srivas2016_list))
exit(0)

shen2015 = Shen2015Parser()
shen2015_list = shen2015.parse()
print("[INFO] Shen et al 2015  n= %d SL interactions" % len(shen2015_list))
exit(0)

toyoshima2008 = Toyoshima2008Parser()
toyoshima2008_list = toyoshima2008.parse()
print("[INFO] Toyoshima et al 2008  n= %d SL interactions" % len(toyoshima2008_list))
exit(0)

lord2008 = Lord2008Parser()
lord2008_list = lord2008.parse()
print("[INFO] Lord et al 2008  n= %d SL interactions" % len(lord2008_list))
exit(0)

steckel2012 = Steckel2012Parser()
steckel2012_list = steckel2012.parse()
print("[INFO] Steckel et al 2012  n= %d SL interactions" % len(steckel2012_list))

bommi2008 = Bommi2008Parser()
bommi2008_list = bommi2008.parse()
print("[INFO] Bommi et al 2008  n= %d SL interactions" % len(bommi2008_list))
exit(0)
# Turner 2008
turner2008 = Turner2008Parser()
turner_list = turner2008.parse()
print("[INFO] Turner et al 2008  n= %d SL interactions" % len(turner_list))

# Blomen 2015
blomen2015 = Blomen2015Parser()
blomen_list = blomen2015.parse()
print("[INFO] Blomen et al 2015  n= %d SL interactions" % len(blomen_list))

# Luo et al 2009
luo2009parser = Luo2009Parser()
luo2009_list = luo2009parser.parse()
print("[INFO] Luo et al 2009  n= %d SL interactions" % len(luo2009_list))

manual = ManualEntry()
manual_list = manual.get_entries()

sli_lists = [luo2009_list, bommi2008_list, turner_list, steckel2012_list, lord2008_list,
             toyoshima2008_list, shen2015_list, srivas2016_list, han2017_list,
             wang2017_list, shen2017_list, manual_list]

n = 0
n_SL = 0
for sli_list in sli_lists:
    for sli in sli_list:
        # if n < 10:
        # print(sli.get_tsv_line())
        n += 1
        if sli.get_SL():
            n_SL += 1

print("We got %d interactions including %d synthetic lethal interactions" % (n, n_SL))


def save_SL_data(path, sli_lists):
    with open(path, 'w') as out_f:
        # out_f.write("Gen1,Gen2,weight\n")
        for sli_list in sli_lists:
            for sli in sli_list:
                if sli.get_SL():
                    out_f.write(sli.get_gene_A_symbol() + "\t" + sli.get_gene_B_symbol() + "\t")
                    out_f.write(str(sli.get_effect_size()) + "\n")


def save_SL_data_ncbi(path, sli_lists):
    with open(path, 'w') as out_f:
        # out_f.write("Gen1,Gen2,weight\n")
        for sli_list in sli_lists:
            for sli in sli_list:
                if sli.get_SL():
                    out_f.write(sli.get_gene_A_id().split(":")[1] + "\t" + sli.get_gene_B_id().split(":")[1] + "\t")
                    out_f.write(str(sli.get_effect_size()) + "\n")


def save_SL_data_ensembl(path, sli_lists):
    found, nfound = 0, 0
    with open(path, 'w') as out_f:
        # out_f.write("Gen1,Gen2,weight\n")
        for sli_list in sli_lists:
            for sli in sli_list:
                # if sli.get_SL():

                if not sli.get_gene_A_id().startswith("NCBI"):
                    geneA_id = ncbi2ensembl.get(sli.get_gene_A_id().split(":")[1])
                elif sli.get_gene_A_symbol() in symbol2ensembl:
                    geneA_id = symbol2ensembl.get(sli.get_gene_A_symbol())
                else:
                    geneA_id = "n/a"

                if sli.get_gene_B_id().startswith("NCBI") and sli.get_gene_B_id().split(":")[1] in ncbi2ensembl:
                    geneB_id = ncbi2ensembl.get(sli.get_gene_B_id().split(":")[1])
                elif sli.get_gene_B_symbol() in symbol2ensembl:
                    geneB_id = symbol2ensembl.get(sli.get_gene_B_symbol())
                else:
                    geneB_id = "n/a"

                if geneA_id.startswith("ENS"):
                    found += 1
                else:
                    # if geneA_id is not "n/a":
                    # print(geneA_id)
                    nfound += 1
                if geneB_id.startswith("ENS"):
                    found += 1
                else:
                    # if geneB_id is not "n/a":
                    # print(geneB_id)
                    nfound += 1
                out_f.write("SL_data\t" + geneA_id + "\t" + geneB_id + "\t" + str(sli.get_effect_size()) + "\n")
    print("Found %d genes, didn't find %d genes" % (found, nfound))
    print(nfound / (found + nfound))


file = "SL_graph.tsv"
ncbi_file = "SL_graph_ncbi.tsv"
ensembl_file = "SL_graph_ensembl.tsv"

# save_SL_data(file, sli_lists)
# save_SL_data_ncbi(ncbi_file, sli_lists)
save_SL_data_ensembl(ensembl_file, sli_lists)

# df = pd.read_csv(filename)
# print(df.head())
# Graphtype = nx.Graph()
# G = nx.from_pandas_edgelist(df, "Gen1", "Gen2", "weight")
# labels=nx.draw_networkx_labels(G, pos=nx.spectral_layout(G))
# nx.draw(G, with_labels = True)
# plt.show()
