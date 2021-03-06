from unittest import TestCase
import os.path
from idg2sl import Srivas2016Parser


class TestSrivas(TestCase):
    """
    This tests the function that parses the
    Srivas et al, A network of conserved synthetic lethal interactions for exploration of precision cancer therapy
    Cell. 2016
    PubMed PMID: 27453043
    which corresponds to the function
    parse_srivas_2016
    """
    def setUp(self) -> None:
        self.inputfile = os.path.join(os.path.dirname(__file__), 'data', 'srivas_small.tsv')
        parser = Srivas2016Parser(fname=self.inputfile)
        self.srivas_list = parser.parse()
        self.first_entry = self.srivas_list[0]

    def test_count_entries(self):
        """
        There are 16 unique genes in srivas_small.
        There are 16 genes altogether.
        Thus, 16 of the entries should be marked as max
        :return:
        """
        self.assertEqual(16, len(self.srivas_list))
        num_max = sum([1 for item in self.srivas_list if item.is_maximum()])
        self.assertEqual(16, num_max)

    def test_get_symbol(self):
        self.assertEqual("IMPDH1", self.first_entry.get_gene_A_symbol())
        self.assertEqual("CHEK1", self.first_entry.get_gene_B_symbol())

    def test_get_perturbation(self):
        self.assertEqual("pharmaceutical", self.first_entry.get_gene_A_pert())
        self.assertEqual("natural (is a TSG)", self.first_entry.get_gene_B_pert())

    def test_get_cellosaurus(self):
        self.assertEqual("HeLa-Cells", self.first_entry.get_cell_line())
        self.assertEqual("CVCL_0030", self.first_entry.get_cellosaurus_id())

    # def test_get_cancer_type(self):
    #     self.assertEqual("", self.first_entry.get_cancer_type())
    #     self.assertEqual("", self.first_entry.get_ncit_id())

    def test_get_assay(self):
        self.assertEqual("pharmaceutical + siRNA", self.first_entry.get_assay())

    def test_get_pmid(self):
        self.assertEqual('27453043', self.first_entry.get_pmid())
