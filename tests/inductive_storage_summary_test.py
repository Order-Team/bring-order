import unittest
import bring_order
from bring_order.inductive_summary_storage import InductiveSummary
from unittest.mock import Mock, MagicMock

class TestInductiveSummary(unittest.TestCase):
    """ Test class for testing the Deductive class
    """
    def setUp(self):
        self.instance = InductiveSummary()

    def test_summary_is_appended(self):
        self.instance.add(2,4, "Psychosis medication usage of minors.xlsx")   
        entry = self.instance.summaries[0]
        #tämä esitysmuoto varmaankin muuttuu, testi on nyt triviaali
        self.assertEqual(entry, {'id': 2, 'cell_number': 4, 'data': 'Psychosis medication usage of minors.xlsx'}) 