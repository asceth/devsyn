import sys
import __builtin__
from math import sin, cos, pi

from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import Vec3
from direct.task.Task import Task

from entities import Sprite

base = __builtin__.base
APP_PATH = __builtin__.APP_PATH

SCREEN_X = 20       #Screen goes from -20 to 20 on X
SCREEN_Y = 15       #Screen goes from -15 to 15 on Y
TURN_RATE = 360     #Degrees ship can turn in 1 second
ACCELERATION = 10   #Ship acceleration in units/sec/sec
MAX_VEL = 6         #Maximum ship velocity in units/sec
MAX_VEL_SQ = MAX_VEL ** 2  #Square of the ship velocity
DEG_TO_RAD = pi/180 #translates degrees to radians for sin and cos

class Player(Sprite):
  def __init__(self):
    Sprite.__init__(self, "media/textures/asteroids/ship")
    self.velocity = Vec3(0, 0, 0)
    self.velocity_direction = 0
    self.hide()

  def activate(self):
    self.show()
    self.update_task = base.taskMgr.add(self.update, "update-player")
    self.update_task.last = 0
    self.accept_controls()

  def deactivate(self):
    self.hide()
    base.taskMgr.remove("update-player")
    self.ignore_controls()

  def accept_controls(self):
    self.accept("i", self.set_velocity_direction, [1])
    self.accept("i-up", self.set_velocity_direction, [0])
    self.accept("k", self.set_velocity_direction, [-1])
    self.accept("k-up", self.set_velocity_direction, [0])

  def ignore_controls(self):
    self.ignore("arrow_up")
    self.ignore("arrow_up-up")
    self.ignore("arrow_down")
    self.ignore("arrow_down-up")

  def set_velocity_direction(self, value):
    self.velocity_direction = value

  def update(self, task):
    dt = task.time - task.last
    task.last = task.time

    heading = self.getR()
    heading_rad = DEG_TO_RAD * heading

    if self.velocity_direction != 0:
      new_velocity = (Vec3(sin(heading_rad) * self.velocity_direction, 0, cos(heading_rad) * self.velocity_direction) * ACCELERATION * dt)
      new_velocity += self.velocity

      if new_velocity.lengthSquared() > MAX_VEL_SQ:
        new_velocity.normalize()
        new_velocity *= MAX_VEL
      self.velocity = new_velocity

    # Update the position
    new_position = self.getPos() + (self.velocity * dt)

    radius = .5 * self.getScale().getX()

    if new_position.getX() - radius > SCREEN_X:
      new_position.setX(-SCREEN_X)
    elif new_position.getX() + radius < -SCREEN_X:
      new_position.setX(SCREEN_X)
    if new_position.getZ() - radius > SCREEN_Y:
      new_position.setZ(-SCREEN_Y)
    elif new_position.getZ() + radius < -SCREEN_Y:
      new_position.setZ(SCREEN_Y)

    self.setPos(new_position)

    return Task.cont

