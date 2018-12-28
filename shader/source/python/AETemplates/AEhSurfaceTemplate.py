import pymel.core as pm

class AEhSurfaceTemplate(pm.ui.AETemplate):

    def __init__(self, nodeName):
        super(AEhSurfaceTemplate, self).__init__(nodeName)
        pm.mel.AEswatchDisplay(nodeName)
        self.beginScrollLayout()
        self.buildBody(nodeName)
        self.addExtraControls("ExtraControls")
        self.endScrollLayout()

    def addControl(self, control, label=None, **kwargs):
        pm.ui.AETemplate.addControl(self, control, label=label, **kwargs)

    def beginLayout(self, name, collapse=True):
        pm.ui.AETemplate.beginLayout(self, name, collapse=collapse)

    def buildBody(self, nodeName):
        self.beginLayout('Diffuse', collapse=0)
        self.addControl("diffuseColor", label="Diffuse Color")
        self.addControl("diffuseMultiplier", label="Diffuse Multiplier")
        self.addControl("diffuseRoughness", label="Diffuse Roughness")
        self.endLayout()
