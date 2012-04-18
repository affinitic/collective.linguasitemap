from plone.testing import z2

from plone.app.testing import *
import collective.linguasitemap

FIXTURE = PloneWithPackageLayer(zcml_filename="configure.zcml",
                                zcml_package=collective.linguasitemap,
                                additional_z2_products=('Products.LinguaPlone',),
                                gs_profile_id='collective.linguasitemap:default',
                                name="collective.linguasitemap:FIXTURE")

INTEGRATION = IntegrationTesting(bases=(FIXTURE,),
                        name="collective.linguasitemap:Integration")

FUNCTIONAL = FunctionalTesting(bases=(FIXTURE,),
                        name="collective.linguasitemap:Functional")
