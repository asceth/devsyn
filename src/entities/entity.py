import sys
import __builtin__
from pandac.PandaModules import NodePath, PandaNode, Filename, BitMask32
from direct.showbase.DirectObject import DirectObject

__all__ = ["Entity"]

APP_PATH = __builtin__.APP_PATH
base = __builtin__.base

class Entity(DirectObject, object):
  def __init__(self, model = None):
    self.prime = None
    if model != None:
      self.set_model(model)

  def get_model(self):
    return self.prime

  def set_model(self, model):
    if model != None:
      if isinstance(model, PandaNode):
        self.prime = NodePath(model)
      elif isinstance(model, NodePath):
        self.prime = model
      else:
        if isinstance(model, Filename):
          model = model.getFullpath()
          if Filename(model).exists():
            self.model = Filename(model).getBasenameWoExtension()
            path = model
          else:
            path = APP_PATH + "media/models/" + model
            if Filename(path).exists():
              pass
            elif Filename(path + ".bam").exists():
              path += ".bam"
            elif Filename(path + ".bam.pz").exists():
              path += ".bam.pz"
            elif Filename(path + ".egg").exists():
              path += ".egg"
            elif Filename(path + ".egg.pz").exists():
              path += ".egg.pz"
            elif Filename(path + ".x").exists():
              path += ".x"
            else:
              print ":object(error): can't find model", model, "!"
              # Probably shouldn't exit because of this
              sys.exit(1)
            self.model = model
          self.prime = base.loader.loadModel(path)
        if self.prime == None:
          print ":object(error): can't load model", path, "!"
          # Probably shouldn't exit because of this
          sys.exit(1)

  def getX(self):
    return self.prime.getX(base.render)

  def getY(self):
    return self.prime.getY(base.render)

  def getZ(self):
    return self.prime.getZ(base.render)

  def getH(self):
    return self.prime.getH(base.render)

  def getP(self):
    return self.prime.getP(base.render)

  def getR(self):
    return self.prime.getR(base.render)

  def getSx(self):
    return self.prime.getSx(base.render)

  def getSy(self):
    return self.prime.getSy(base.render)

  def getSz(self):
    return self.prime.getSz(base.render)

  def getPos(self):
    return self.prime.getPos(base.render)

  def getHpr(self):
    return self.prime.getHpr(base.render)

  def getScale(self):
    return self.prime.getScale(base.render)

  def getCollideMask(self):
    return self.prime.getCollideMask()

  def getTransparency(self):
    return self.prime.getTransparency()

  def getTwoSided(self):
    return self.prime.getTwoSided()

  def getParent(self):
    return self.prime.getParent()

  def setX(self, *v):
    self.prime.setX(*v)

  def setY(self, *v):
    self.prime.setY(*v)

  def setZ(self, *v):
    self.prime.setZ(*v)

  def setH(self, *v):
    self.prime.setH(*v)

  def setP(self, *v):
    self.prime.setP(*v)

  def setR(self, *v):
    self.prime.setR(*v)

  def setSx(self, *v):
    self.prime.setSx(*v)

  def setSy(self, *v):
    self.prime.setSy(*v)

  def setSz(self, *v):
    self.prime.setSz(*v)

  def setPos(self, *v):
    self.prime.setPos(*v)

  def setHpr(self, *v):
    self.prime.setHpr(*v)

  def setScale(self, *v):
    self.prime.setScale(*v)

  def setCollideMask(self, *v):
    self.prime.setCollideMask(*v)

  def setTransparency(self, *v):
    self.prime.setTransparency(*v)

  def setTwoSided(self, *v):
    self.prime.setTwoSided(*v)

  def removeNode(self):
    self.prime.removeNode()

  def reparentTo(self, parent):
    if isinstance(parent, Entity):
      parent = parent.prime
    if isinstance(parent, str):
      if parent.startswith("render/"):
        parent = parent[7:]
        tv = parent
        parent = base.render.find(tv)
        if parent == NodePath():
          parent = base.render.find("**/" + tv)
    if parent != NodePath() and parent != None:
      self.prime.reparentTo(parent)

  def wrtReparentTo(self, parent):
    if isinstance(parent, Entity):
      parent = parent.prime
    if isinstance(parent, str):
      if parent.startswith("render/"):
        parent = parent[7:]
        tv = parent
        parent = base.render.find(tv)
        if parent == NodePath():
          parent = base.render.find("**/" + tv)
    if parent != NodePath():
      self.prime.reparentTo(parent)

  def attachTo(self, parent):
    """This attaches the object to another object/nodepath. The caller object stays at the same place, with the same scale and rotation,
    but they become relative to the other object/nodepath. This is useful with for example a character that steps onto a moving ship or so."""
    if isinstance(parent, Entity):
      parent = parent.prime
    if isinstance(parent, str):
      if(parent.startswith("render/")): parent = parent[7:]
      tv = parent
      parent = base.render.find(tv)
      if(parent == NodePath()):
        parent = base.render.find("**/" + tv)
    if(parent != NodePath()):
      self.prime.setPos(self.prime.getPos(parent))
      self.prime.setHpr(self.prime.getHpr(parent))
      self.prime.setScale(self.prime.getScale(parent))
      self.prime.reparentTo(parent)

  def hide(self):
    self.prime.hide()

  def show(self):
    self.prime.show()

  def __del__(self):
    try:
      if isinstance(self.prime, NodePath):
        self.prime.removeNode()
    except AttributeError: pass

  def __getstate__(self):
    return [self.model, self.getX(), self.getY(), self.getZ(), self.getH(),
            self.getP(), self.getR(), self.getSx(), self.getSy(),
            self.getSz(), self.getCollideMask().getWord(),
            self.getTransparency(), self.getTwoSided(), str(self.getParent())]

  def __setstate__(self, p):
    if len(p) < 14:
      print ":object(error): This state is not compatible with this version!"
      sys.exit(1)

    self.setModel(p[0])
    self.setX(p[1])
    self.setY(p[2])
    self.setZ(p[3])
    self.setH(p[4])
    self.setP(p[5])
    self.setR(p[6])
    self.setSx(p[7])
    self.setSy(p[8])
    self.setSz(p[9])
    self.setCollideMask(BitMask32(p[10]))
    self.setTransparency(p[11])
    self.setTwoSided(p[12])
    self.reparentTo(p[13])
