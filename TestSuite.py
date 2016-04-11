 #!/usr/bin/python

import server
import unittest

import TestIndexRoute
import TestUidRoute

server.app.testing = True
client = server.app.test_client()

def setServerObjects(storedObjects):
    server.storedObjects = storedObjects

def getServerObjects():
    return server.storedObjects

if __name__ == '__main__':
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTest(loader.loadTestsFromTestCase(TestIndexRoute.TestIndexRoute))
    suite.addTest(loader.loadTestsFromTestCase(TestUidRoute.TestUidRoute))
    unittest.TextTestRunner(verbosity=2).run(suite)
