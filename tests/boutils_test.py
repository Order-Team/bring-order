import unittest
import bring_order
from unittest.mock import Mock, patch, MagicMock
from bring_order.boutils import BOUtils
from IPython import display

class TestBOUtils(unittest.TestCase):

    def setUp(self):
        self.instance = BOUtils()        

    def test_get_python_code_from_response_returns_correct_string(self):
        response = ("Here's an example code snippet that accomplishes this:\n"
                    "```python\n"
                    "import numpy as np\n"
                    "# Generate sample from standard normal distribution\n"
                    "sample = np.random.normal(loc=0, scale=1, size=1000)\n"
                    "# Calculate sample mean and variance\n"
                    "sample_mean = np.mean(sample)\n"
                    "sample_variance = np.var(sample)\n"
                    "\n"
                    "# Print mean and variance\n"
                    "print('Sample Mean: ', sample_mean)\n"
                    "print('Sample Variance: ', sample_variance)\n"
                    "```\n"
                    "\n"
                    "Finally, the calculated mean and variance are printed to the console.")

        correct = ("import numpy as np\\n"
                   "# Generate sample from standard normal distribution\\n"
                   "sample = np.random.normal(loc=0, scale=1, size=1000)\\n"
                   "# Calculate sample mean and variance\\n"
                   "sample_mean = np.mean(sample)\\n"
                   "sample_variance = np.var(sample)\\n"
                   "\\n"
                   "# Print mean and variance\\n"
                   "print(\\'Sample Mean: \\', sample_mean)\\n"
                   "print(\\'Sample Variance: \\', sample_variance)")

        self.assertEqual(self.instance.get_python_code_from_response(response), correct)