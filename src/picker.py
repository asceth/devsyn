import math, __builtin__
from direct.showbase import DirectObject
from pandac.PandaModules import CollisionTraverser, CollisionHandlerQueue
from pandac.PandaModules import CollisionNode,CollisionRay, GeomNode

base = __builtin__.base

class Picker(DirectObject.DirectObject):
  def __init__(self, ancestor=None):
    print "________________"
    print "Class Picker"
    self.ancestor = ancestor

    # create traverser
    base.cTrav = CollisionTraverser()

    # create collision ray
    self.create_ray(self, base.camera, name = "mouse_ray", show = True)

    # initialize mouse picks
    self.accept('mouse1-up', self.mouse_pick, [1, self.queue])
    self.accept('mouse3', self.mouse_pick, [3, self.queue])

  def mouse_right(self, picked_object, picked_point):
    if picked_object == None: return

    # get cell from picked_point
    cell = (int(math.floor(picked_point[0])), int(math.floor(picked_point[1])))
    # trace udpated info about the cell
    self.ancestor.txt.setText(str(self.ancestor.grid.data[cell[0]][cell[1]]))

  def mouse_left(self, picked_object, picked_point):
    if picked_object == None: return
    # do nothing right now

  def mouse_pick(self, button, queue):
    # get mouse coords
    if base.mouseWatcherNode.hasMouse() == False: return

    mpos = base.mouseWatcherNode.getMouse()
    # locate ray from camera lens to mouse coords
    self.rayNP.reparentTo(base.camera)
    self.ray.setFromLens(base.camNode, mpos.getX(), mpos.getY())

    # get collision: picked object and point
    picked_object, picked_point = self.get_collision(queue)

    # call appropriate mouse function (left or right)
    if button == 1:
      self.mouse_left(picked_object, picked_point)
    elif button == 3:
      self.mouse_right(picked_object, picked_point)

  def pick(self, x, y):
    # locate ray from camera lens to mouse coords
    self.rayNP.reparentTo(base.camera)
    self.ray.setFromLens(base.camNode, x, y)

    # get collision: picked object and point
    return self.get_collision(self.queue)

  def get_collision(self, queue):
    # do the traversal
    base.cTrav.traverse(base.render)

    # process collision entries in queue
    if queue.getNumEntries() > 0:
      queue.sortEntries()
      for i in range(queue.getNumEntries()):
        collision_entry = queue.getEntry(i)
        picked_object = collision_entry.getIntoNodePath()

        # iterate up in model heirarchy to find a pickable tag
        parent = picked_object.getParent()
        for n in range(4):
          if parent.getTag('pickable') != "" or parent == base.render:
            break
          parent = parent.getParent()
        if parent.getTag('pickable') != "":
          picked_object = parent
          picked_point = collision_entry.getSurfacePoint(picked_object)
          return picked_object, picked_point
    return None, None

  """sets nodepath pickable state"""
  def make_pickable(self, new_object, tag = 'true'):
    new_object.setTag('pickable', tag)

  def create_ray(self, object, entity, name, show = False, x = 0, y = 0, z = 0,
                 dx = 0, dy = 0, dz = -1):
    # create queue
    object.queue = CollisionHandlerQueue()
    # create ray
    object.rayNP = entity.attachNewNode(CollisionNode(name))
    object.ray = CollisionRay(x, y, 1, dx, dy, dz)
    object.rayNP.node().addSolid(object.ray)
    object.rayNP.node().setFromCollideMask(GeomNode.getDefaultCollideMask())
    base.cTrav.addCollider(object.rayNP, object.queue)
    if show:
      object.rayNP.show()



