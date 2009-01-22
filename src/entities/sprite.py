import __builtin__

from pandac.PandaModules import Point2
from entities import Entity

base = __builtin__.base
APP_PATH = __builtin__.APP_PATH

class Sprite(Entity):
  def __init__(self, texture = None, position = Point2(0, 0), depth = 55, scale = 1,
               transparency = True):
    Entity.__init__(self, "shapes/plane")
    self.prime.reparentTo(base.camera)
    self.prime.setPos(Point3(position.getX(), depth, position.getY()))
    self.prime.setScale(scale)

    # tells panda3d to not care about what order to draw the sprite in, prevents
    # z-fighting
    self.prime.setBin("unsorted", 0)

    # tells panda3d not to check if something has been drawn in front of it
    self.prime.setDepthTest(False)
    if transparency:
      self.prime.setTransparency(1)

    if texture:
      self.texture = base.loader.loadTexture(APP_PATH + "media/textures/" +
                                             texture + ".png")
      self.prime.setTexture(self.texture, 1)

  def activate(self):
    self.accept_controls()
    base.taskMgr.add(self.move_update, 'player-move-task')
    base.taskMgr.add(self.jump_update, 'player-jump-task', 40)

  def deactivate(self):
    self.ignore_controls()
    base.taskMgr.remove('player-move-task')
    base.taskMgr.remove('player-jump-task')
