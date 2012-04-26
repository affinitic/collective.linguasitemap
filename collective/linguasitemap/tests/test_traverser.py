import unittest2 as unittest
from collective.linguasitemap.tests import base

class TestSiteMapTraverser(base.IntegrationTestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """
    

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)