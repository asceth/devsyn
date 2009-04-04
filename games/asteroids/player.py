import sys
import __builtin__
from math import sin, cos, pi

from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import Vec3
from direct.task.Task import Task

from devsyn.entities import Sprite
from devsyn.physics.xy import pymunk
from devsyn.physics.xy.pymunk import Vec2d

base = __builtin__.base
APP_PATH = __builtin__.APP_PATH

SCREEN_X = 20       #Screen goes from -20 to 20 on X
SCREEN_Y = 15       #Screen goes from -15 to 15 on Y
TURN_RATE = 360     #Degrees ship can turn in 1 second
ACCELERATION = 10   #Ship acceleration in units/sec/sec
MAX_VEL = 6         #Maximum ship velocity in units/sec
MAX_VEL_SQ = MAX_VEL ** 2  #Square of the ship velocity
DEG_TO_RAD = pi/180 #translates degrees to radians for sin and cos
PLAYER_MASS = 10

class Player(Sprite):
  def __init__(self):
    Sprite.__init__(self, "media/textures/asteroids/ship")
    self.velocity_direction = 0
    self.rotation_direction = 0

    min, max = self.prime.getTightBounds()
    self.width = max.getX() - min.getX()
    self.height = max.getZ() - min.getZ()

    self.hide()

  def physical_presence(self):
    points = [(-self.width, -self.height), (-self.width, self.height), (self.width, self.height), (self.width, -self.height)]
    moment = pymunk.moment_for_poly(PLAYER_MASS, points, (0, 0))
    self.physical_body = pymunk.Body(PLAYER_MASS, moment)
    self.physical_body.position = Vec2d(self.getX(), self.getZ())
    self.physical_shape = pymunk.Poly(self.physical_body, points, (0, 0))
    self.physical_shape.friction = 0.0
    self.physical_shape.elasticity = 0.6
    return (self.physical_body, self.physical_shape)

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
    self.accept("j", self.set_rotation_direction, [-1])
    self.accept("j-up", self.set_rotation_direction, [0])
    self.accept("l", self.set_rotation_direction, [1])
    self.accept("l-up", self.set_rotation_direction, [0])

  def ignore_controls(self):
    self.ignore("i")
    self.ignore("i-up")
    self.ignore("k")
    self.ignore("k-up")
    self.ignore("j")
    self.ignore("j-up")
    self.ignore("l")
    self.ignore("l-up")

  def set_velocity_direction(self, value):
    self.velocity_direction = value

  def set_rotation_direction(self, value):
    self.rotation_direction = value

  def update(self, task):
    dt = task.time - task.last
    task.last = task.time

    heading = self.getR()
    if self.rotation_direction != 0:
      heading += (dt * TURN_RATE * self.rotation_direction)
      self.setR(heading % 360)

    heading_rad = DEG_TO_RAD * heading

    if self.velocity_direction != 0:
      new_velocity = (Vec2d(sin(heading_rad), cos(heading_rad)) * self.velocity_direction * ACCELERATION * dt)

      if new_velocity.get_length_sqrd() > MAX_VEL_SQ:
        new_velocity.normalized()
        new_velocity *= MAX_VEL
      else:
        self.physical_body.apply_impulse(new_velocity, (0, 0))

    # Update the position
    new_position = Vec3(self.physical_body.position.x, self.getY(), self.physical_body.position.y)
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
    self.physical_body.position = (self.getX(), self.getZ())
    return Task.cont

