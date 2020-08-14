from collections import defaultdict
from idg2sl import SyntheticLethalInteraction
from idg2sl.sl_dataset_parser import SL_DatasetParser
from .sl_constants import SlConstants
from idg2sl.gene_pair import GenePair
import csv


class Steckel2012Parser(SL_DatasetParser):
    """
    Steckel M, et al. Determination of synthetic lethal interactions in KRAS oncogene-dependent cancer cells reveals novel
    therapeutic targeting strategies. Cell Res. 2012 Aug;22(8):1227-45.  PubMed PMID: 22613949
    HCT-116 human colon cancer cells and the isogenic derivative, HKE-3, in which the activated, but not the
    normal, KRAS allele has been removed by homologous recombination
    a Delta-Z-score cut-off value of 3.3 was selected to generate a primary hit list of 89 genes
    (∼ 1.2% of the total number of genes screened)
    KRAS itself was placed ninth in this ΔZ-score ranking list, scoring very highly in HCT-116 and weakly in HKE-3 cells
    and thereby serving as an important internal control (Supplementary information, Table S1). Of the remaining 88 genes,
    18 with a Z-score in excess of 2.0 in the HKE-3 cell line alone were eliminated from further analysis, following the
    reasoning that high levels of apoptosis resulting from siRNA-mediated silencing of these genes would likely
    constitute an undesirably strong cytotoxic effect in wild-type KRAS cells (Supplementary information, Figure S2B
    and S2C). Thus, our starting list for further validation comprised 70 candidate genes.
    6159 lines in Harnessing Supp.
    Parse strategy
    delta_zscore >= 3.3 reveals 89 candidates (correct)
    if we remove kras and genes with HKE3_zscore > 2, we get to 70 genes (correct)
    This does not match with the Harnessing paper, which reports 80 SL genes. We will stick with the results
    of the initial screen, i.e., 70 genes, and count the rest as negatives.
    I replaced P11 by ENDOU
    """

    def __init__(self, fname='data/steckel-2012-KRAS.tsv'):
        pmid = 'PMID:22613949'
        super().__init__(fname=fname, pmid=pmid)

    def parse(self):
        kras_symbol = 'KRAS'
        kras_id = 'NCBIGene:3845'
        kras_perturbation = SlConstants.ACTIVATING_MUTATION  # activating_mutation
        gene2_perturbation = SlConstants.SI_RNA  # 'siRNA'
        assay_string = "RNA-interference assay"
        effect_type = 'stddev'
        cell_line = 'HCT-116'
        cellosaurus = 'CVCL_0291'
        cancer = "Colorectal Carcinoma"
        ncit = "NCIT:C2955"
        sli_dict = defaultdict(list)
        # GeneID	Locus.ID	Accession	HCT-116.Z-score	HKE-3.Z-score	D.Z-score
        with open(self.fname) as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter='\t')
            for row in csvreader:
                if len(row) != 6:
                    raise ValueError("Line has %d fields (should have 6): %s" % (len(F), line))
                geneB_sym = row['GeneID']  # F[0]
                geneB_sym = self.get_current_symbol(geneB_sym)
                locusID = row['Locus.ID']  # F[1]
                accession = row['Accession']  # F[2]
                HCT116_zscore = float(row['HCT-116.Z-score'])  # float(F[3])
                HKE3_zscore = float(row['HKE-3.Z-score'])  # float(F[4])
                delta_zscore = float(row['D.Z-score'])
                if geneB_sym in self.entrez_dict:
                    geneB_id = "NCBIGene:{}".format(self.entrez_dict.get(geneB_sym))
                else:
                    raise ValueError("Could not find id for gene %s in Steckel 2012" % geneB_sym)
                if geneB_sym == "KRAS":
                    continue  # This was an internal control!
                if delta_zscore >= 3.3 and HKE3_zscore < 2:
                    SL = True
                else:
                    SL = False
                sli = SyntheticLethalInteraction(gene_A_symbol=kras_symbol,
                                                 gene_A_id=kras_id,
                                                 gene_B_symbol=geneB_sym,
                                                 gene_B_id=geneB_id,
                                                 gene_A_pert=kras_perturbation.to_string(),
                                                 gene_B_pert=gene2_perturbation.to_string(),
                                                 effect_type=effect_type,
                                                 effect_size=HCT116_zscore,
                                                 cell_line=cell_line,
                                                 cellosaurus_id=cellosaurus,
                                                 cancer_type=cancer,
                                                 ncit_id=ncit,
                                                 assay=assay_string,
                                                 pmid=self.pmid,
                                                 SL=SL)
                gene_pair = GenePair(kras_symbol, geneB_sym)
                sli_dict[gene_pair].append(sli)
        sli_list = self._mark_maximum_entries(sli_dict)
        return sli_list
