from plone.app.layout.sitemap import sitemap as base
from BTrees.OOBTree import OOBTree
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.layout.navigation.interfaces import INavigationRoot

from Products.CMFCore.interfaces import ISiteRoot
from zope.traversing.interfaces import IBeforeTraverseEvent

from ZPublisher.BaseRequest import DefaultPublishTraverse

import logging
logger = logging.getLogger('test')

class SiteMapTraverser(DefaultPublishTraverse):
    
    def publishTraverse(self, request, name):
        """catch sitemap name"""

        #pre condition
        if not name.startswith('sitemap_') or not name.endswith('.xml.gz') or \
           name == 'sitemap.xml.gz' or len(name) not in (17,19):
            return super(SiteMapTraverser, self).publishTraverse(request, name)

        logger.info('call for sitemap: %s'%name)

        sitemap_view = self.context.restrictedTraverse('@@sitemap.xml.gz')
        language = self.extractLanguage(name)

        if language is None:
            return super(SiteMapTraverser, self).publishTraverse(request, name)

        sitemap_view.language = language
        sitemap_view.filename = 'sitemap_%s.xml.gz'%language
        return sitemap_view

    def extractLanguage(self, name):
        if type(name) not in (str, unicode): return
        if name.startswith('sitemap') and len(name)>11 and '_' in name:
            sitemap = name.split('.')[0]
            lang = str(sitemap.split('_')[1])

            return lang


class SiteMapView(base.SiteMapView):
    """override sitemap"""

    def __init__(self, context, request):
        super(SiteMapView, self).__init__(context, request)
        self.language = 'all'

    def objects(self):
        """Returns the data to create the sitemap."""
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {'Language': self.language}
        utils = getToolByName(self.context, 'plone_utils')
        query['portal_type'] = utils.getUserFriendlyTypes()
        ptool = getToolByName(self, 'portal_properties')
        siteProperties = getattr(ptool, 'site_properties')
        typesUseViewActionInListings = frozenset(
            siteProperties.getProperty('typesUseViewActionInListings', [])
            )
        
        is_plone_site_root = IPloneSiteRoot.providedBy(self.context)
        if not is_plone_site_root:
            query['path'] = '/'.join(self.context.getPhysicalPath())


        query['is_default_page'] = True
        default_page_modified = OOBTree()
        for item in catalog.searchResults(query):
            key = item.getURL().rsplit('/', 1)[0]
            value = (item.modified.micros(), item.modified.ISO8601())
            default_page_modified[key] = value

        # The plone site root is not catalogued.
        if is_plone_site_root:
            loc = self.context.absolute_url()
            date = self.context.modified()
            # Comparison must be on GMT value
            modified = (date.micros(), date.ISO8601())
            default_modified = default_page_modified.get(loc, None)
            if default_modified is not None:
                modified = max(modified, default_modified)
            lastmod = modified[1]
            yield {
                'loc': loc,
                'lastmod': lastmod,
                #'changefreq': 'always', # hourly/daily/weekly/monthly/yearly/never
                #'prioriy': 0.5, # 0.0 to 1.0
            }

        query['is_default_page'] = False
        for item in catalog.searchResults(query):
            loc = item.getURL()
            date = item.modified
            # Comparison must be on GMT value
            modified = (date.micros(), date.ISO8601())
            default_modified = default_page_modified.get(loc, None)
            if default_modified is not None:
                modified = max(modified, default_modified)
            lastmod = modified[1]
            if item.portal_type in typesUseViewActionInListings:
                loc += '/view'
            yield {
                'loc': loc,
                'lastmod': lastmod,
                #'changefreq': 'always', # hourly/daily/weekly/monthly/yearly/never
                #'prioriy': 0.5, # 0.0 to 1.0
            }

class NavigationRootSiteMapView(SiteMapView):
    """A sitemap that extract the language from the navigation root"""

    def objects(self):
        is_navigation_root = INavigationRoot.providedBy(self.context)
        if is_navigation_root:
            self.language = self.context.Language()
        return super(NavigationRootSiteMapView, self).objects()

