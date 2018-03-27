import unittest
from model import calculator

class PricerTest(unittest.TestCase):
    """This python unit test file is intended to test calculator.py"""

    def setUp(self):
        """Method automatically called before each unit test"""
        self.params_1 = {"S":100,"K":100,"Vol":0.2,"R":0.05,"T":1}
        self.params_2 = {"S":100,"K":100,"Vol":0.2,"R":0.00,"T":1}
        pass

    def test_callPrice(self):
        """Test the vanilla call price value"""
        call_price1 = calculator.BlackScholes.call_price(**self.params_1)
        call_price2 = calculator.BlackScholes.call_price(**self.params_2)
        self.assertAlmostEqual(call_price1,10.45,delta=0.01)
        self.assertAlmostEqual(call_price2,7.965,delta=0.01)

if __name__ == '__main__':
    unittest.main()

