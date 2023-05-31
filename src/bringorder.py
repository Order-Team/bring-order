import os
import sys
class_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, class_dir)

from bogui import BOGui

class BringOrder():
    def __init__(self):
        self.bogui = BOGui()
        self.bogui()
