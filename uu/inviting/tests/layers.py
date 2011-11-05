from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.testing import z2
from zope.configuration import xmlconfig


# fixture layer classes:
class ProductLayer(PloneSandboxLayer):
    """base product layer, for use by per-profile layers"""

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """load package zcml to initialize product"""
        import uu.inviting
        self.loadZCML(package=uu.inviting)

    def setUpPloneSite(self, portal):
        """Install named setup profile for class to portal"""
        self.applyProfile(portal, self.PROFILE)


class DefaultProfileTestLayer(ProductLayer):
    """Layer for default profile testing"""
    
    PROFILE = 'uu.inviting:default'


class UninstallAfterInstallTestLayer(ProductLayer):
    
    INSTALL_PROFILE = 'uu.inviting:default'
    UNINSTALL_PROFILE = 'uu.inviting:uninstall'
    
    def setUpPloneSite(self, portal):
        ## install
        self.applyProfile(portal, self.INSTALL_PROFILE)
        ## uninstall
        self.applyProfile(portal, self.UNINSTALL_PROFILE)
    


# fixture bases:
DEFAULT_PROFILE_FIXTURE = DefaultProfileTestLayer()

DEFAULT_PROFILE_TESTING = IntegrationTesting(
    bases=(DEFAULT_PROFILE_FIXTURE,),
    name='uu.inviting:Default Profile')

# Functional testing layers:
DEFAULT_PROFILE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DEFAULT_PROFILE_FIXTURE,),
    name='uu.inviting:Default Profile Functional')


# uninstalled add-on fixture
POST_UNINSTALL_PROFILE_FIXTURE = UninstallAfterInstallTestLayer()

POST_UNINSTALL_PROFILE_TESTING = IntegrationTesting(
    bases=(POST_UNINSTALL_PROFILE_FIXTURE,),
    name='uu.inviting:Uninstall profile')


