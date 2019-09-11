#!/usr/bin/python3
import unittest
import aduc

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromModule(aduc))

    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
