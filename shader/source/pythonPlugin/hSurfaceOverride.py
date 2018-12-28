'''Ambient and Friends surface shader implementation'''

import logging
import path
import sys
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OpenMayaRender

logger = logging.getLogger("render")

"""
    For viewport2.0 a surface shader has to be declared with the help of several shader xml files.
    
"""
class hSurfaceShaderOverride(OpenMayaRender.MPxSurfaceShadingNodeOverride):
    def __init__(self, obj):
        OpenMayaRender.MPxSurfaceShadingNodeOverride.__init__(self, obj)
        
        fragmentFolder = path.path(__file__).parent + "/hSurfaceFragments"
        fragmentMgr = OpenMayaRender.MRenderer.getFragmentManager()
        logger.debug("Adding fragment search path: {0}".format(fragmentFolder))
        fragmentMgr.addFragmentPath(fragmentFolder)
        
        fragments = []
        fragments.append("hSurfaceCombiner")
        fragments.append("hSurfaceDiffuse")


        for fragment in fragments:
            if fragmentMgr.hasFragment(fragment):
                logger.debug("Fragment {0} already loaded.".format(fragment))
            else:
                fragmentFilename = fragment + ".xml"
                loadedFragmentName = fragmentMgr.addShadeFragmentFromFile(fragmentFilename, False)
                if loadedFragmentName == fragment:
                    logger.debug("Fragment {0} successfully loaded.".format(fragment))

        graphName = "hSurface"
        if fragmentMgr.hasFragment(graphName):
            logger.debug("Fragmentgraph {0} already loaded.".format(graphName))
        else:
            fragmentGraphFilename = graphName + ".xml"
            loadedFragmentGraphName = fragmentMgr.addFragmentGraphFromFile(fragmentGraphFilename)
            if loadedFragmentGraphName == fragmentGraphFilename:
                logger.debug("Fragmentgraph {0} successfully loaded.".format(graphName))
            
            
        
    def supportedDrawAPIs(self):
        return OpenMayaRender.MRenderer.kOpenGL | OpenMayaRender.MRenderer.kDirectX11

    def fragmentName(self):
        return "hSurface"

    @staticmethod
    def creator(obj):
        return hSurfaceShaderOverride(obj)
    
