import unittest
import bring_order
from unittest.mock import Mock, patch, MagicMock
from bring_order.boutils import BOUtils
from IPython import display

class TestBOUtils(unittest.TestCase):

    def setUp(self):
        self.instance = BOUtils()        
