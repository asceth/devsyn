import __builtin__
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task

from entities import Entity

base = __builtin__.base

class FirstPersonCamera(Entity):
  # TODO: Make speed configurable
  # constants
  speed = 50

  def __init__(self, parent = base.render):
    # basic properties
    ## keeps track of mouse movement
    self.pos = [0.0, 0.0]

    # our prime is the camera
    self.prime = base.camera

    # who are we attached to?
    self.parent = parent

    # initialize various velocities
    self.rotation_velocity = 0.05

  def activate(self, reparent = True):
    print "Activated FirstPerson Camera"
    # initialize camera
    base.camLens.setFov(70) # field of view

    if reparent == True:
      self.reset_parent()

    # initialize camera task
    base.taskMgr.add(self.update, "update_camera_task")

  def deactivate(self):
    self.reset_parent(base.render)
    base.taskMgr.remove("update_camera_task")

  def reset_parent(self, parent = None):
    if parent != None:
      if isinstance(parent, Entity):
        self.parent = parent.prime
      else:
        self.parent = parent

    # attach to our parent
    self.attachTo(self.parent)
    # has to be a way to get the height of the model....
    self.setZ(self.getZ() + 1.0)
    self.parent.hide()

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


    # collisions are taken care of through our
    # parent (usually a player etc)

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

