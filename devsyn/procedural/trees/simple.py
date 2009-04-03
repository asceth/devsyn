import math
import __builtin__

from pandac.PandaModules import Vec3, GeomVertexData, GeomVertexFormat
from pandac.PandaModules import Geom, GeomVertexWriter, GeomVertexRewriter
from pandac.PandaModules import GeomVertexReader, GeomTristrips, CullFaceAttrib
from pandac.PandaModules import GeomNode, NodePath, Mat4, Vec4, TransformState
from pandac.PandaModules import GeomVertexArrayFormat, InternalName

from devsyn.entities import Entity
from devsyn.procedural.utility import ProceduralUtility

APP_PATH = __builtin__.APP_PATH
base = __builtin__.base

class SimpleTree(Entity):
  geom_vertex_format = None

  def get_format():
    if SimpleTree.geom_vertex_format is None:
      format_array = GeomVertexArrayFormat()
      format_array.addColumn(InternalName.make("drawFlag"), 1, Geom.NTUint8,
                             Geom.COther)
      format = GeomVertexFormat(GeomVertexFormat.getV3n3cpt2())
      format.addArray(format_array)
      SimpleTree.geom_vertex_format = GeomVertexFormat.registerFormat(format)

    return SimpleTree.geom_vertex_format
  get_format = staticmethod(get_format)


  def __init__(self, scale = 0.125, length = Vec3(4, 4, 7), position = Vec3(0, 0, 0),
               iterations = 10, num_branches = 4, vector_list = [Vec3(0, 0, 1),
                                                             Vec3(1, 0, 0),
                                                             Vec3(0, -1, 0)]):
    self.set_model(NodePath("SimpleTree"))


    self.format = SimpleTree.get_format()
    self.vdata = GeomVertexData("body vertices", self.format, Geom.UHStatic)
    self.position = position
    self.length = length
    self.vector_list = vector_list
    self.iterations = iterations
    self.num_branches = num_branches
    self.scale = scale

    self.bark_texture = base.loader.loadTexture(APP_PATH +
                                                'media/textures/trees/bark.jpg')

  def generate(self):
    self.recurse(self.length, self.position, self.iterations, self.vector_list)
    self.get_model().setTexture(self.bark_texture, 1)
    self.reparentTo(base.render)

  def recurse(self, length, position, iterations, vector_list):
    if iterations > 0:
      self.draw_body(position, vector_list, length.getX())
      # move forward along the right axis
      new_position = position + vector_list[0] * length.length()

      # Only branch every third level
      if iterations % 3 == 0:
        # decrease dimensions when we branch
        length = Vec3(length.getX() / 2, length.getY() / 2,
                      length.getZ() / 1.1)
        for i in range(self.num_branches):
          self.recurse(length, new_position, iterations - 1,
                       ProceduralUtility.random_axis(vector_list))
      else:
        # just make another branch connected to this one with a small
        # variation in direction
        self.recurse(length, new_position, iterations - 1,
                     ProceduralUtility.small_random_axis(vector_list))
    else:
      self.draw_body(position, vector_list, length.getX(), False)
      self.draw_leaf(position, vector_list, self.scale)


  def draw_body(self, position, vector_list, radius = 1, keep_drawing = True, num_vertices = 8):
    circle_geom = Geom(self.vdata)

    vertex_writer = GeomVertexWriter(self.vdata, "vertex")
    color_writer = GeomVertexWriter(self.vdata, "color")
    normal_writer = GeomVertexWriter(self.vdata, "normal")
    draw_rewriter = GeomVertexRewriter(self.vdata, "drawFlag")
    tex_rewriter = GeomVertexRewriter(self.vdata, "texcoord")

    start_row = self.vdata.getNumRows()
    vertex_writer.setRow(start_row)
    color_writer.setRow(start_row)
    normal_writer.setRow(start_row)

    sCoord = 0

    if start_row != 0:
      tex_rewriter.setRow(start_row - num_vertices)
      sCoord = tex_rewriter.getData2f().getX() + 1

      draw_rewriter.setRow(start_row - num_vertices)
      if draw_rewriter.getData1f() == False:
        sCoord -= 1

    draw_rewriter.setRow(start_row)
    tex_rewriter.setRow(start_row)

    angle_slice = 2 * math.pi / num_vertices
    current_angle = 0

    perp1 = vector_list[1]
    perp2 = vector_list[2]

    # write vertex information
    for i in range(num_vertices):
      adjacent_circle = position + (perp1 * math.cos(current_angle) + perp2 * math.sin(current_angle)) * radius
      normal = perp1 * math.cos(current_angle) + perp2 * math.sin(current_angle)
      normal_writer.addData3f(normal)
      vertex_writer.addData3f(adjacent_circle)
      tex_rewriter.addData2f(sCoord, (i + 0.001) / (num_vertices - 1))
      color_writer.addData4f(0.5, 0.5, 0.5, 1.0)
      draw_rewriter.addData1f(keep_drawing)
      current_angle += angle_slice

    draw_reader = GeomVertexReader(self.vdata, "drawFlag")
    draw_reader.setRow(start_row - num_vertices)

    # we can't draw quads directly so use Tristrips
    if start_row != 0 and draw_reader.getData1f() != False:
      lines = GeomTristrips(Geom.UHStatic)
      half = int(num_vertices * 0.5)
      for i in range(num_vertices):
        lines.addVertex(i + start_row)
        if i < half:
          lines.addVertex(i + start_row - half)
        else:
          lines.addVertex(i + start_row - half - num_vertices)

      lines.addVertex(start_row)
      lines.addVertex(start_row - half)
      lines.closePrimitive()
      lines.decompose()
      circle_geom.addPrimitive(lines)

      circle_geom_node = GeomNode("Debug")
      circle_geom_node.addGeom(circle_geom)

      circle_geom_node.setAttrib(CullFaceAttrib.makeReverse(), 1)

      self.get_model().attachNewNode(circle_geom_node)

  def draw_leaf(self, position, vector_list, scale = 0.125):
    # use the vectors that describe the direction the branch grows
    # to make the right rotation matrix
    new_cs = Mat4(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    new_cs.setRow(0, vector_list[2]) # right
    new_cs.setRow(1, vector_list[1]) # up
    new_cs.setRow(2, vector_list[0]) # forward
    new_cs.setRow(3, Vec3(0, 0, 0))
    new_cs.setCol(3, Vec4(0, 0, 0, 1))

    axis_adjustment = Mat4.scaleMat(scale) * new_cs * Mat4.translateMat(position)

    leaf_model = base.loader.loadModelCopy(APP_PATH + 'media/models/shrubbery')
    leaf_texture = base.loader.loadTexture(APP_PATH + 'media/models/material-10-cl.png')

    leaf_model.reparentTo(self.get_model())
    leaf_model.setTexture(leaf_texture, 1)
    leaf_model.setTransform(TransformState.makeMat(axis_adjustment))

