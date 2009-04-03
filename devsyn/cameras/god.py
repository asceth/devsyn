import __builtin__
from pandac.PandaModules import Vec3, WindowProperties
from direct.task.Task import Task

from devsyn.entities import Entity

base = __builtin__.base

class GodCamera(Entity):
  # TODO: speed should be configurable
  # constants
  speed   = 25
  FORWARD = Vec3(0, 1, 0)
  BACK    = Vec3(0, -1, 0)
  LEFT    = Vec3(-1, 0, 0)
  RIGHT   = Vec3(1, 0, 0)
  STOP    = Vec3(0) # zero vector

  walk = STOP
  strafe = STOP

  def __init__(self):
    """initialize"""
    # basic properties
    ## keeps track of mouse movement
    self.pos = [0.0, 0.0]

  def activate(self, position = Vec3(0, 0, 0)):
    print "Activating God Camera"
    # No moar cursor!
    wp = WindowProperties()
    wp.setCursorHidden(True)
    # does not exist panda 1.3.2 / but is reqired for osx-mouse movement
    try: wp.setMouseMode(WindowProperties.MAbsolute)
    except: pass
    base.win.requestProperties(wp)

    # initialize camera
    base.camLens.setFov(55) # field of view
    base.camera.reparentTo(base.render) # attach it to the render
    ## set position
    base.camera.setPos(position)
    base.camera.setHpr(0, 0, -90)
    self.prime = base.camera

    # initialize mouse controls
    ## walking and stopping if input is lost
    self.accept("s" , self.set_walk, [self.BACK])
    self.accept("s-up" , self.set_walk, [self.STOP])
    self.accept("w" , self.set_walk, [self.FORWARD])
    self.accept("w-up" , self.set_walk, [self.STOP])
    self.accept("d" , self.set_strafe, [self.RIGHT])
    self.accept("d-up" , self.set_strafe, [self.STOP])
    self.accept("a" , self.set_strafe, [self.LEFT])
    self.accept("a-up" , self.set_strafe, [self.STOP])

    # initialize camera task
    base.taskMgr.add(self.update, "update_camera_task")

  def deactivate(self):
    print "Deactivating God Camera"
    # No moar cursor!
    wp = WindowProperties()
    wp.setCursorHidden(True)
    # does not exist panda 1.3.2 / but is reqired for osx-mouse movement
    try: wp.setMouseMode(WindowProperties.MAbsolute)
    except: pass
    base.win.requestProperties(wp)

    self.prime = None

    self.ignore("s")
    self.ignore("s-up")
    self.ignore("w")
    self.ignore("w-up")
    self.ignore("d")
    self.ignore("d-up")
    self.ignore("a")
    self.ignore("a-up")

    base.taskMgr.remove("update_camera_task")

  def set_walk(self, value):
    self.walk = value
  def set_strafe(self, value):
    self.strafe = value

  def update(self, task):
    base.camera.setPos(self.walk * globalClock.getDt() * self.speed)
    base.camera.setPos(self.strafe * globalClock.getDt() * self.speed)
    return Task.cont



