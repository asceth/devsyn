import __builtin__
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import Vec3, WindowProperties
from direct.task.Task import Task

from entities import Entity

base = __builtin__.base

class FreeLookCamera(Entity):
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

  def __init__(self, look_at = Vec3(0, 0, 0), show_target = False):
    """initialize"""
    # basic properties
    ## keeps track of mouse movement
    self.pos = [0.0, 0.0]

    # initialize various velocities
    self.rotation_velocity = 0.05

  def activate(self, position = Vec3(5.0, 5.0, 5.0)):
    print "Activating FreeLook Camera"
    # No moar cursor!
    wp = WindowProperties()
    wp.setCursorHidden(True)
    # does not exist panda 1.3.2 / but is reqired for osx-mouse movement
    try: wp.setMouseMode(WindowProperties.MAbsolute)
    except: pass
    base.win.requestProperties(wp)

    # initialize camera
    base.camLens.setFov(70) # field of view
    base.camera.reparentTo(base.render) # attach it to the render
    ## set position
    base.camera.setPos(position)

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
    print "Deactivating FreeLook Camera"
    # No moar cursor!
    wp = WindowProperties()
    wp.setCursorHidden(True)
    # does not exist panda 1.3.2 / but is reqired for osx-mouse movement
    try: wp.setMouseMode(WindowProperties.MAbsolute)
    except: pass
    base.win.requestProperties(wp)

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
    # rotate the camera
    pointer = base.win.getPointer(0)
    new_position = [pointer.getX(), pointer.getY()]
    # new position - last position gives us difference in mouse movement
    d = [new_position[0] - self.pos[0],
         new_position[1] - self.pos[1]]

    # interpolate mouse last position to new position
    self.pos[0] += d[0] * 0.5
    self.pos[1] += d[1] * 0.5

    # rotate camera using x vector (left/right)
    camright = base.camera.getNetTransform().getMat().getRow3(0)
    camright.normalize()
    base.camera.setH(base.camera.getH() -
                       (d[0] * self.rotation_velocity))

    # rotate camera using z vector (up/down)
    camup = base.camera.getNetTransform().getMat().getRow3(2)
    camup.normalize()
    base.camera.setP(base.camera.getP() -
                       (d[1] * self.rotation_velocity * 2.5))

    base.camera.setPos(base.camera, self.walk * globalClock.getDt() * self.speed)
    base.camera.setPos(base.camera, self.strafe * globalClock.getDt() * self.speed)

    # we don't care about camera collisions in freelook

    # For smoother mouse movement on all platforms
    # we don't immediately set the 'cursor' in the window
    # back to the center.  Instead we let it freely travel
    # within a square region inside the actual window.
    # In this case the region has a 1/4 margin around
    # our game window.
    # If the cursor travels outside of this region
    # we set it back to the center of the region.
    # We ONLY reset the axis that moves out of bounds.

    ## If the mouse escapes the region via the x-axis
    ## reset the x axis to half screen width (center of screen)
    if (self.pos[0] < (base.win.getXSize() * 0.25)):
      self.pos[0] = (base.win.getXSize() / 2)
      base.win.movePointer(0, base.win.getXSize() / 2, int(self.pos[1]))
    elif (self.pos[0] >  (base.win.getXSize() * 0.75)):
      self.pos[0] = (base.win.getXSize() / 2)
      base.win.movePointer(0, base.win.getXSize() / 2, int(self.pos[1]))

    ## If the mouse escapes the region via the y-axis
    ## reset the y axis to half the screen height (center of screen)
    if (self.pos[1] < (base.win.getYSize() * 0.25)):
      self.pos[1] = (base.win.getYSize() / 2)
      base.win.movePointer(0, int(self.pos[0]), base.win.getYSize() / 2)
    elif (self.pos[1] > (base.win.getYSize() * 0.75)):
      self.pos[1] = (base.win.getYSize() / 2)
      base.win.movePointer(0, int(self.pos[0]), base.win.getYSize() / 2)

    return Task.cont



