import unittest2 as unittest
from zope import interface
from collective.linguasitemap import testing
from collective.linguasitemap.tests import utils
from collective.linguasitemap.browser.interfaces import ILayer
from plone.browserlayer.layer import mark_layer

class IntegrationTestCase(unittest.TestCase):

    layer = testing.INTEGRATION

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        self.portal = self.layer['portal']
        testing.setRoles(self.portal, testing.TEST_USER_ID, ['Manager'])
        testing.login(self.portal, testing.TEST_USER_NAME)
        languages = ['en','fr','nl']
        defaultLanguage = 'en'
        self.portal.portal_languages.manage_setLanguageSettings(defaultLanguage,
                                                                languages)
        self.portal.invokeFactory('Folder', 'dossier')
        self.folder = self.portal['dossier']
        self.folder.setLanguage('fr')
        self.folder.reindexObject()
        self.portal.portal_properties.site_properties.enable_sitemap = True
        self.request = self.layer['request']
        mark_layer(self.portal, self)

class FunctionalTestCase(IntegrationTestCase):

    layer = testing.FUNCTIONAL
    
    def setUp(self):
        super(FunctionalTestCase, self).setUp()
        #we need to commit to be able to use browser
        import transaction
        transaction.commit()

