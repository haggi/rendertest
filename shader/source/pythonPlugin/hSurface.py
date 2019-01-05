import sys

import logging
import pymel.core as pm
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.api.OpenMayaRender as OpenMayaRender

# import hSurfaceOverride

logger = logging.getLogger("render")

NODE_ID = OpenMaya.MTypeId(0x0011CF56)


class hSurface(OpenMayaMPx.MPxNode):

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def postConstructor(self):
        logger.debug("postConstructor")

    @staticmethod
    def hSurfaceCreator():
        return OpenMayaMPx.asMPxPtr(hSurface())

    @staticmethod
    def hSurfaceInitializer():
        nAttr = OpenMaya.MFnNumericAttribute()

        hSurface.diffuseColor = nAttr.createColor(
            "diffuseColor", "diffuseColor")
        nAttr.setDefault(.5, .5, .5)
        hSurface.addAttribute(hSurface.diffuseColor)

        hSurface.diffuseMultiplier = nAttr.create(
            "diffuseMultiplier", "diffuseMultiplier", OpenMaya.MFnNumericData.kFloat, 1.0)
        nAttr.setSoftMin(0.0)
        nAttr.setSoftMax(1.0)
        hSurface.addAttribute(hSurface.diffuseMultiplier)

        hSurface.diffuseRoughness = nAttr.create(
            "diffuseRoughness", "diffuseRoughness", OpenMaya.MFnNumericData.kFloat, 0.0)
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        hSurface.addAttribute(hSurface.diffuseRoughness)

        # this Attribute only exists for a default display in Legacy Viewport, therefore it is hidden
        hSurface.color = nAttr.createColor("color", "color")
        nAttr.setDefault(.5, .5, .5)
        nAttr.setHidden(True)
        hSurface.addAttribute(hSurface.color)

        hSurface.outColor = nAttr.createColor("outColor", "outColor")
        nAttr.keyable = False
        nAttr.storable = False
        nAttr.readable = True
        nAttr.writable = False
        nAttr.setHidden(True)
        hSurface.addAttribute(hSurface.outColor)

        hSurface.attributeAffects(hSurface.diffuseColor, hSurface.outColor)

    def compute(self, plug, data):

        if plug == hSurface.outColor:
            outColorHandle = data.outputValue(hSurface.outColor)
            outColorHandle.setMFloatVector(OpenMaya.MFloatVector(.5, .5, .5))
            outColorHandle.setClean()


sRegistrantId = "hSurfacePlugin"
sDrawDBClassification = "drawdb/shader/surface/hSurface"
swatchRendererClassification = "swatch/ArnoldRenderSwatch"
sFullClassification = "shader/surface:" + swatchRendererClassification


def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)

    try:
        mplugin.registerNode("hSurface", NODE_ID, hSurface.hSurfaceCreator,
                             hSurface.hSurfaceInitializer, OpenMayaMPx.MPxNode.kDependNode, sFullClassification)
    except:
        sys.stderr.write("Failed to register node: hSurface")
        raise


"""     try:
        OpenMayaRender.MDrawRegistry.registerShadingNodeOverrideCreator(
            sDrawDBClassification, sRegistrantId, hSurfaceOverride.hSurfaceShaderOverride.creator)
    except:
        sys.stderr.write("Failed to register hSurface override\n")
        raise
 """


def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(NODE_ID)
    except:
        sys.stderr.write("Failed to deregister node: hSurface")
        raise
"""     try:
        print "Deregister", sDrawDBClassification, sRegistrantId
        OpenMayaRender.MDrawRegistry.deregisterShadingNodeOverrideCreator(
            sDrawDBClassification, sRegistrantId)
    except:
        sys.stderr.write("Failed to deregister hSurface override\n")
        raise
 """
