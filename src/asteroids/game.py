title = "Asteroids"

import sys
import __builtin__
from math import sin, cos, pi
from random import randint, choice, random
import cPickle

from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText, TextNode
from pandac.PandaModules import NodePath, Vec3, Filename

from cameras import GodCamera
from entities import Sprite

base = __builtin__.base
APP_PATH = __builtin__.APP_PATH

SPRITE_POS = 55     #At default field of view and a depth of 55, the screen
                    #dimensions is 40x30 units
SCREEN_X = 20       #Screen goes from -20 to 20 on X
SCREEN_Y = 15       #Screen goes from -15 to 15 on Y
TURN_RATE = 360     #Degrees ship can turn in 1 second
ACCELERATION = 10   #Ship acceleration in units/sec/sec
MAX_VEL = 6         #Maximum ship velocity in units/sec
MAX_VEL_SQ = MAX_VEL ** 2  #Square of the ship velocity
DEG_TO_RAD = pi/180 #translates degrees to radians for sin and cos
BULLET_LIFE = 2     #How long bullets stay on screen before removed
BULLET_REPEAT = .05  #How often bullets can be fired
BULLET_SPEED = 10   #Speed bullets move
AST_INIT_VEL = 1    #Velocity of the largest asteroids
AST_INIT_SCALE = 3  #Initial asteroid scale
AST_VEL_SCALE = 2.2 #How much asteroid speed multiplies when broken up
AST_SIZE_SCALE = .6 #How much asteroid scale changes when broken up
AST_MIN_SCALE = 1.1 #If and asteroid is smaller than this and is hit,
                    #it disapears instead of splitting up

class Game(DirectObject):
  def __init__(self):
    self.title_text = self.info((-1.32, 0.96), title)

    base.disableMouse()
    self.ship = Sprite("ship")


  """info"""
  def info(self, pos, msg):
    self.font = base.loader.loadFont(APP_PATH + 'media/fonts/OCR.otf')
    return OnscreenText(font = self.font, text = msg, style = 1, fg = (1, 1, 1, 1),
                        pos = pos, align = TextNode.ALeft, scale = .035,
                        mayChange = True)

