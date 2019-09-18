#!/usr/bin/python3
import unittest
import aduc, gpmc, dns, adsi

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromModule(aduc))
    suite.addTests(loader.loadTestsFromModule(gpmc))
    suite.addTests(loader.loadTestsFromModule(dns))
    suite.addTests(loader.loadTestsFromModule(adsi))

    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
