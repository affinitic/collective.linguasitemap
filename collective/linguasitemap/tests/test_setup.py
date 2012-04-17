"""This is an integration "unit" test. It uses PloneTestCase, but does not
use doctest syntax.

You will find lots of examples of this type of test in CMFPlone/tests, for 
example.
"""

from collective.linguasitemap.tests import base
from plone.browserlayer import utils

class TestSetup(base.TestCase):
    """The name of the class should be meaningful. This may be a class that
    tests the installation of a particular product.
    """

    def setUp(self):
        super(TestSetup, self).setUp()
        self.portal_types = self.portal.portal_types

    def beforeTearDown(self):
        pass

    def test_browserlayer(self):
        from collective.linguasitemap.browser.interfaces import ILayer
        layers = utils.registered_layers()
        self.assertIn(ILayer, layers)

class TestUninstall(base.TestCase):
    """Test if the addon uninstall well"""

    def setUp(self):
        super(TestUninstall, self).setUp()
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=['collective.linguasitemap'])

    def test_uninstall_browserlayer(self):
        from collective.linguasitemap.browser.interfaces import ILayer
        layers = utils.registered_layers()
        self.assertNotIn(ILayer, layers)


def test_suite():
   return base.build_test_suite((TestSetup, TestUninstall))
