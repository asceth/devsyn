title = "DevSyn RPG Prototype"

import sys
import __builtin__

from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText, TextNode
from pandac.PandaModules import NodePath, Vec3, Filename

from games.rpg import picker, terrain, lighting
from devsyn.cameras import FreeLookCamera, FirstPersonCamera
from devsyn.entities import Player
from devsyn.procedural.trees import SimpleTree


base = __builtin__.base
APP_PATH = __builtin__.APP_PATH


# Main Class
class Game(DirectObject):
  """initialize"""
  def __init__(self):
    print "______________________"
    print "Class Main"

    base.disableMouse()
    base.camLens.setNear(0.0001)

    # Setup application
    self.keys()
    self.txt = self.info((-1.32, 0.96), title)

    # Initialize classes
    self.grid = None
    self.free_look_camera = None
    self.avatars = None
    self.camera_type = "free_look"
    self.trees = []

    # Initialize World
    self.root = NodePath("rootMain")
    self.root.reparentTo(base.render)

    # Initialize Picker
    self.picker = picker.Picker(self)

    # Initialize Terrain
    self.terrain = terrain.Terrain(self, 65, 2.0, 20.0, 'advanced', False)

    # Initialize Player
    self.player = Player(Filename("media/models/avatars/ralph/ralph"))
    self.player.reparentTo(base.render)
    self.player.setScale(0.05)


    # Initialize Cameras
    self.free_look_camera = FreeLookCamera()
    self.first_person_camera = FirstPersonCamera()

    # Initialize Lights
    self.lights = lighting.Lighting(self)

    # Activate Free Look
    self.free_look_camera.activate()

    return

  """info"""
  def info(self, pos, msg):
    self.font = base.loader.loadFont(APP_PATH + 'media/fonts/OCR.otf')
    return OnscreenText(font = self.font, text = msg, style = 1, fg = (1, 1, 1, 1),
                        pos = pos, align = TextNode.ALeft, scale = .035,
                        mayChange = True)


  """keys"""
  def keys(self):
    self.accept('e', self.toggle_wire_frame)
    self.accept('t', self.toggle_texture)
    self.accept('r', self.snapshot)
    self.accept('q', self.switch_camera)
    self.accept('f', self.grow_tree)
    self.accept('escape', sys.exit)
    return

  def collision_traverse(self, task):
    base.cTrav.traverse(base.render)

  def grow_tree(self):
    picked_object, picked_point = self.picker.pick(0.0, 0.0)

    if picked_object is None:
      return
    else:
      tree = SimpleTree(0.01, Vec3(0.05, 0.05, 0.2), picked_point)
      tree.generate()
      self.trees.append(tree)

  def snapshot(self):
    base.screenshot("snapshot")

  def toggle_wire_frame(self):
    base.toggleWireframe()

  def toggle_texture(self):
    base.toggleTexture()

  def switch_camera(self):
    print "Switching Cameras"
    if self.camera_type == "free_look":
      self.free_look_camera.deactivate()

      self.player.activate()
      self.player.setPos(base.camera.getPos())
      self.first_person_camera.activate(False)
      self.first_person_camera.reset_parent(self.player)

      base.taskMgr.add(self.collision_traverse, "ctrav-traverse")
      self.camera_type = "first_person"
    elif self.camera_type == "first_person":
      self.player.deactivate()
      self.first_person_camera.deactivate()
      self.free_look_camera.activate()
      base.taskMgr.remove("ctrav-traverse")
      self.camera_type = "free_look"
    else:
      self.player.deactivate()
      self.first_person_camera.deactivate()
      self.free_look_camera.activate()
      base.taskMgr.remove("ctrav-traverse")
      self.camera_type = "free_look"


