"""usefull functions for mesh and models management"""

from pandac.PandaModules import NodePath
from direct.actor.Actor import Actor
import __builtin__

base = __builtin__.base

#===============================================================================
def loadInstance(parent, source, name, size = None, pos = None, color = None):
  # create instance of a previous loaded model
  model = parent.attachNewNode(name)
  instance = source.instanceTo(model)
  # model aditional transformations
  if size != None:
    resizeToUnit(model, size)
  if pos != None:
    model.setPos(pos[0], pos[1], pos[2])
  if color != None:
    model.setColorScale(color[0], color[1], color[2], color[3])
  return model

#=============================================================================
def loadModel(parent, path, name, size = None, pos = None,
              color = None, tex = None):
  # New models are loaded in a non-standard way to allow flattenStrong to work effectively over them.
  model = base.loader.loadModel(path)
  model.reparentTo(parent)
  # model aditional transformations
  if size != None:
    resizeToUnit(model, size)
  if pos != None:
    model.setPos(pos[0], pos[1], pos[2])
  if color != None:
    model.setColorScale(color[0], color[1], color[2], color[3])
  if tex != None:
    tx = base.loader.loadTexture(tex)
    model.setTexture(tx)
  return model

#=============================================================================
def loadModelCopy(parent, path, name, size = None, pos = None,
                  color = None, tex = None):
  # New models are loaded in a non-standard way to allow flattenStrong to work effectively over them.
  modelRoot = base.loader.loadModelCopy(path)
  model = NodePath(name)
  modelRoot.getChildren().reparentTo(model)
  model.reparentTo(parent)
  #model aditional transformations
  if size != None:
    resizeToUnit(model, size)
  if pos != None:
    model.setPos(pos[0], pos[1], pos[2])
  if color != None:
    model.setColorScale(color[0], color[1], color[2], color[3])
  if tex != None:
    tx = base.loader.loadTexture(tex)
    model.setTexture(tx)
  return model


def loadActor(parent = base.render, path = None, anim = None,
              size = None, pos = None, color = None, tex = None):
  #load actor model
  model = Actor(path,{"walk":path+"-walk","run":path+"-run"})
  model.reparentTo(parent)
  #model aditional transformations
  if size != None:
    resizeToUnit(model, size)
  if pos != None:
    model.setPos(pos[0], pos[1], pos[2])
  if color != None:
    model.setColorScale(color[0], color[1], color[2], color[3])
  if tex != None:
    tx = base.loader.loadTexture(tex)
    model.setTexture(tx, 1)
  return model


def deleteModel(model):
  #Calling delete() or cleanup() is the way on an actor, or removeNode() on a model.
  model.removeNode()


def resizeToUnit(model, size = 1.0, showBounds = False):
  """resizes any model to given size (radius=1*size) """
  bounds = model.getBounds()
  center = bounds.getCenter()
  radius = bounds.getRadius() * 1.15 #have to add .15 for scaling 1:1 (why?)
  newsize=1.0 / radius * size
  model.setScale(newsize)
  #model.showBounds()



