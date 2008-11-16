import math

from pandac.PandaModules import Vec3, GeomVertexData, GeomVertexFormat
from pandac.PandaModules import Geom, GeomVertexWriter, GeomVertexRewriter

from entites import Entity

class SimpleTree(Entity):
  def __init__(self, length = Vec3(4, 4, 7), position = Vec3(0, 0, 0),
               iterations = 10, branches = 4, vector_list = [Vec3(0, 0, 1),
                                                             Vec3(1, 0, 0),
                                                             Vec3(0, -1, 0)]):
    self.vdata = GeomVertexData("body vertices", GeomVertexFormat.getV3n3cpt2(),
                               Geom.UHStatic)
    self.position = position
    self.length = length
    self.vector_list = vector_list
    self.iterations = 10
    self.branches = 4

    if iterations > 0:
      self.draw_body(position, vector_list, length.getX())

  def draw_body(self, radius = 1, keep_drawing = True, num_vertices = 8):
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

    draw_rewriter.set_row(start_row)
    tex_rewriter.set_row(start_row)

    angle_slice = (2 * math.pi) / num_vertices
    current_angle = 0

    perp1 = self.vector_list[1]
    perp2 = self.vector_list[2]

    # write vertex information
    for i in range(num_vertices):
      adjacent_circle = self.position + (perp1 * math.cos(current_angle) + perp2 * math.sin(current_angle)) * radius
      normal = perp1 * math.cos(current_angle) + perp2 * math.sin(current_angle)
      normal_writer.addData3f(normal)
      vertex_writer.addData3f(adjacent_circle)
      tex_rewriter.addData2f(sCoord, (i + 0.001) / (num_vertices - 1))
      color_writer.addData4f(0.5, 0.5, 0.5, 1.0)
      draw_rewriter.addData1f(keep_drawing)
      current_angle += angle_slice

    draw_reader = GeomVertexReader(self.vdata, "drawFlag")
    draw_reader.setRow(start_row - num_vertices)
