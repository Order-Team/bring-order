import unittest
from ipywidgets import widgets
from unittest.mock import Mock
from bring_order.limitations import Limitations
from bring_order.boval import BOVal


class TestLimitations(unittest.TestCase):

    def setUp(self):
        bogui = Mock()
        self.instance = Limitations(bogui, BOVal())
        self.instance.bogui = bogui

    def test_check_limitations_returns_false_when_empty(self):
        self.assertFalse(self.instance.check_limitations())

    def test_check_limitations_returns_true_when_not_empty(self):
        value = "Some limitations"
        self.assertTrue(self.instance.check_limitations(value))

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

    def test_not_normally_distributed_returns_expected_list(self):
        self.instance.data_limitations[0].value = 'Monthly.Income is not normally distributed'
        self.instance.data_limitations.append(widgets.Text(f'Data sample is too small'))
        self.instance.data_limitations.append(widgets.Text(f'Amount.Funded.By.Investors is not normally distributed'))
        result = self.instance.not_normally_distributed_variables()
        self.assertEqual(2, len(result))

    def test_create_limitation_grid_creates_correct_number_of_checkboxes(self):
        self.instance.data_limitations = [widgets.Text(), widgets.Text()]
        self.instance.bogui.create_message = lambda value: widgets.HTML(value)
        self.instance.bogui.create_checkbox = lambda desc: widgets.Checkbox(description=desc)
        self.instance.create_limitation_grid()
        self.assertEqual(len(self.instance.remove_checkboxes), 2)

    def test_set_error_value(self):
        self.instance.set_error_value('My error')
        self.assertEqual(self.instance.empty_limitations_error.value, 'My error')

    def test_not_independent_variables_returns_correct_list(self):
        self.instance.data_limitations[0].value = 'Var1 is not normally distributed'
        self.instance.data_limitations.append(widgets.Text('Data sample is too small'))
        self.instance.data_limitations.append(widgets.Text('Var1 and Var2 are not independent'))
        self.instance.data_limitations.append(widgets.Text('Var3 and Var4 are not independent'))
        self.assertEqual(
            self.instance.not_independent_variables(),
            ['Var1 and Var2', 'Var3 and Var4']
        )

    def test_other_limitations_returns_correct_list(self):
        self.instance.data_limitations[0].value = 'Var1 is not normally distributed'
        self.instance.data_limitations.append(widgets.Text('Data sample is too small'))
        self.instance.data_limitations.append(widgets.Text('Var1 and Var2 are not independent'))
        self.assertEqual(
            self.instance.other_limitations(),
            ['Data sample is too small']
        )

    def test_get_limitations_for_print_returns_empty_if_no_limitations_are_added(self):
        self.instance.data_limitations = [widgets.Text(value='', placeholder='Limitation 1')]
        self.assertEqual(
            self.instance.get_limitations_for_print().value,
            ''
        )

    def test_get_limitations_for_print_returns_correct_string_value(self):
        self.instance.data_limitations = [widgets.Text(value='', placeholder='Limitation 1')]
        self.instance.data_limitations.append(widgets.Text('Var1 is not normally distributed'))
        self.instance.data_limitations.append(widgets.Text('Var2 is not normally distributed'))
        self.instance.data_limitations.append(widgets.Text('Data sample is too small'))
        self.instance.data_limitations.append(widgets.Text('Var3 and Var4 are not independent'))
        correct = (
            '<h4>There are some data limitations you should consider:</h4>\n<ul>\n'
            '<li><b>Variables that are not normally distributed:</b> Var1, Var2</li>\n'
            '<li><b>Variables that are not independent:</b> Var3 and Var4</li>\n'
            '<li>Data sample is too small</li>'
            '</ul>'
        )
        self.assertEqual(self.instance.get_limitations_for_print().value, correct)
