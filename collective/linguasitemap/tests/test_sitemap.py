import unittest2 as unittest

from zope import component
from collective.linguasitemap.tests import base, utils
from plone.testing.z2 import Browser

class UnitTestSiteMapView(unittest.TestCase):
    
    def test_language(self):
        from collective.linguasitemap.browser import sitemap
        sm = sitemap.SiteMapView(utils.FakeContext(), None)
        self.assertTrue(hasattr(sm, 'language'))
        self.assertEqual(sm.language, 'all')

class UnitTestSiteMapTraverser(unittest.TestCase):
    
    def test_extractLanguage(self):
        from collective.linguasitemap.browser import sitemap
        traverser = sitemap.SiteMapTraverser(None, None)
        self.assertTrue(traverser.extractLanguage('notsitemap')         is None)
        self.assertTrue(traverser.extractLanguage('sitemap.xml.gz')     is None)
        self.assertTrue(traverser.extractLanguage(None)                 is None)
        self.assertTrue(traverser.extractLanguage('sitemap_fr.xml.gz') =='fr')
        self.assertTrue(traverser.extractLanguage('sitemap_xx.xml.gz') =='xx')
        self.assertTrue(traverser.extractLanguage('sitemap_yyy.xml.gz') == 'yyy')

    def test_publishTraverse(self):
        from collective.linguasitemap.browser import sitemap
        traverser = sitemap.SiteMapTraverser(utils.FakeContext(), {'URL':'http://nohost/plone'})
        self.assertRaises(KeyError, traverser.publishTraverse, {'URL':'http://nohost/plone'}, 'test')
    

class IntegrationTestSiteMap(base.IntegrationTestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """

    def test_language(self):
        from collective.linguasitemap.browser import sitemap
        sm = sitemap.SiteMapView(self.portal, self.portal.REQUEST)
        self.assertTrue(hasattr(sm, 'language'))
        self.assertEqual(sm.language,'all')

        sm = component.getMultiAdapter((self.portal, self.portal.REQUEST),
                                       name="sitemap.xml.gz")
        self.assertTrue(hasattr(sm, 'language'))
        self.assertEqual(sm.language,'all')


class FunctionaTestSiteMap(base.FunctionalTestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """

    def test_language(self):
        browser = Browser(self.layer['app'])
        sm = browser.open(self.portal.absolute_url()+'/sitemap.xml.gz')
        self.assertFalse(browser.isHtml)
        self.assert_(len(browser.contents)>0)
        #TODO: open the gzip and then parse the xml and then verify content

