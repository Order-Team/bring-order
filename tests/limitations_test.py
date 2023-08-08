import unittest
from ipywidgets import widgets
from unittest.mock import Mock, patch, MagicMock
from bring_order.boutils import BOUtils
from bring_order.bogui import BOGui
from bring_order.bodi import Bodi
from bring_order.limitations import Limitations


class TestLimitations(unittest.TestCase):

    def setUp(self):
        bogui = Mock()
        self.instance = Limitations(bogui)
        self.instance.bogui = bogui

    def test_check_limitations_returns_false_when_empty(self):
        self.assertFalse(self.instance.check_limitations())

    def test_check_limitations_returns_true_when_not_empty(self):
        value = "Some limitations"
        self.assertTrue(self.instance.check_limitations(value))        

    def test_call_check_limitation_returns_false_when_one_limitation_is_empty(self):
        self.instance.data_limitations.append(widgets.Text('Limitation'))
        self.instance.data_limitations.append(widgets.Text(''))
        self.assertFalse(self.instance.call_check_limitation())

    def test_call_check_limitation_returns_true_with_no_empty_limitations(self):
        self.instance.data_limitations[0].value = 'Limitation0'
        for n in range(1,3):
            self.instance.data_limitations.append(
                widgets.Text(f'Limitation{n}')
            )
        self.assertTrue(self.instance.call_check_limitation())

    def test_format_limitations_returns_correct_string(self):
        self.instance.data_limitations[0].value = 'Limitation0'
        self.instance.data_limitations.append(widgets.Text(f'Limitation1'))
        text = self.instance.format_limitations()
        correct = '### Limitations\\n- Limitation0\\n- Limitation1\\n'
        self.assertEqual(text, correct)    

    def test_last_limitations_is_not_removed(self):
        self.instance.remove_limitations()
        self.assertEqual(len(self.instance.data_limitations), 1)        
    
    def test_add_limitation_adds_limitation_input_to_list(self):
        self.instance.bogui.create_input_field = lambda dv, ph : widgets.Text(
            value=f'{dv}',
            placeholder=f'{ph}')
        self.instance.bogui.create_message = lambda value : widgets.HTML(value)
        self.instance.add_limitation()
        self.assertEqual(len(self.instance.data_limitations), 2)
        self.instance.add_limitation()
        self.assertEqual(len(self.instance.data_limitations), 3)     

    def test_remove_limitations_removes_limitations(self):
        self.instance.bogui.create_input_field = lambda dv, ph : widgets.Text(
            value=f'{dv}',
            placeholder=f'{ph}')
        self.instance.bogui.create_message = lambda value : widgets.HTML(value)
        self.instance.add_limitation()
        self.assertEqual(len(self.instance.data_limitations), 2)
        self.instance.remove_checkboxes = [
            widgets.Checkbox(value=True),
            widgets.Checkbox(value=False)
        ]
        self.instance.remove_limitations()
        self.assertEqual(len(self.instance.data_limitations), 1)
        self.assertEqual(len(self.instance.remove_checkboxes), 1)      
    