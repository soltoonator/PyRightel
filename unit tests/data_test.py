import unittest
import time
from PyRightel import data

class dataUnitTests(unittest.TestCase):

    def test_isExpired(self):
        pkg = data.package()
        pkg.startTimestamp = time.time() - 10000
        pkg.endTimestamp = time.time() + 15000
        self.assertFalse(pkg.isExpired)
        pkg.startTimestamp = time.time() + 10000
        pkg.endTimestamp = time.time() - 15000
        self.assertTrue(pkg.isExpired)



if __name__ == '__main__':
    unittest.main()