import __builtin__
from pandac.PandaModules import Spotlight, PerspectiveLens, Fog, OrthographicLens
from pandac.PandaModules import PointLight, AmbientLight, DirectionalLight
from pandac.PandaModules import Vec4

base = __builtin__.base

class Lighting:
  def __init__(self, ancestor = None):
    print "____________________________________________________"
    print "Class Lights"
    self.ancestor = ancestor

    #Initialize bg colour
    colour = (0.2, 0.2, 0.6)
    base.setBackgroundColor(*colour)
    base.camLens.setFar(1000.0)

    self.alight = AmbientLight('ambient_light')
    self.alight.setColor(Vec4(0.7, 0.7, 0.7, 1))
    self.alnp = base.render.attachNewNode(self.alight)
    base.render.setLight(self.alnp)

    self.plight = PointLight('sunlight')
    self.plight.setColor(Vec4(2.5, 2.5, 2.5, 1))
    self.plnp = base.render.attachNewNode(self.plight)
    self.plnp.setPos(50, 0, 300)
    self.plnp.lookAt(self.ancestor.terrain.root)
    base.render.setLight(self.plnp)

    # Initialize linear fog
    self.fog = Fog("Fog object")
    self.fog.setMode(Fog.MLinear)
    self.fog.setLinearRange(14.0,40.0)
    self.fog.setColor(*colour)
    #base.render.setFog(self.fog)



