import __builtin__
import random

from pandac.PandaModules import NodePath, GeomVertexData, GeomVertexFormat
from pandac.PandaModules import Geom, GeomVertexWriter, GeomTriangles, GeomNode, Vec3
from pandac.PandaModules import Texture, DepthTestAttrib
from pandac.PandaModules import PNMImage, Filename, BitMask32
from pandac.PandaModules import GeoMipTerrain, TextureStage

import meshes
from devsyn.maps import DiamondMap

APP_PATH = __builtin__.APP_PATH
base = __builtin__.base

class Terrain:
  """initialize"""
  def __init__(self, ancestor = None, size = 65, alt = 2.0, div = 5, tile_theme = 'random', retro = True):
    print "_________________"
    print "Class Terrain"
    self.ancestor = ancestor

    # initialize basic properties
    self.alt = alt
    self.div = div
    self.divsep = 1.0
    self.retro = retro
    self.map_path = APP_PATH + 'media/maps/'
    self.texture_path = APP_PATH + 'media/tiles/advanced/'
    self.themes = ['advanced']

    self.tiles = [{'rgb':(0, 50, 255), 'tex':APP_PATH + 'media/tiles/advanced/water.png', 'score':2, 'h':0}]


    # create terrain nodepath
    self.root = NodePath("rootTerrain")
    self.root.setSz(1.0)
    self.root.reparentTo(self.ancestor.root)

    # make terrain pickable as 'terrain'
    self.ancestor.picker.make_pickable(self.root, 'terrain')

    # create a random heightmap of given size
    self.heightmap = DiamondMap(self.map_path + "hmap.png", size, alt)

    # generate data from hmap and cmap
    self.data = self.make_data(self.map_path + "hmap.png")

    # generate subdata from data
    self.subdata = self.make_subdata(base_data = self.data, div = self.div)

    self.geomip_terrain = GeoMipTerrain("geomip_terrain")
    self.geomip_terrain.setHeightfield(Filename(self.map_path + "hmap.png"))
    self.geomip_terrain.getRoot().setSz(20)
    self.geomip_terrain.setBlockSize(32)
    self.geomip_terrain.setFactor(400)
    self.geomip_terrain.setMinLevel(1.5)
    self.geomip_terrain.setFocalPoint(base.camera)
    self.geomip_terrain.getRoot().reparentTo(self.root)
    self.geomip_terrain.generate()


    tex0 = base.loader.loadTexture(self.texture_path + "water.jpg")
    tex0.setMinfilter(Texture.FTLinearMipmapLinear)
    tex1 = base.loader.loadTexture(self.texture_path + "desert.png")
    tex1.setMinfilter(Texture.FTLinearMipmapLinear)
    tex2 = base.loader.loadTexture(self.texture_path + "water.jpg")
    tex2.setMinfilter(Texture.FTLinearMipmapLinear)
    tex3 = base.loader.loadTexture(self.texture_path + "rock.png")
    tex3.setMinfilter(Texture.FTLinearMipmapLinear)
    tex4 = base.loader.loadTexture(self.texture_path + "desert.png")
    tex4.setMinfilter(Texture.FTLinearMipmapLinear)
    tex5 = base.loader.loadTexture(self.texture_path + "sand.jpg")
    tex5.setMinfilter(Texture.FTLinearMipmapLinear)
    tex6 = base.loader.loadTexture(self.texture_path + "default.png")
    tex6.setMinfilter(Texture.FTLinearMipmapLinear)

    # set mutiltextures
    self.geomip_terrain.getRoot().setTexture( TextureStage('tex0'),tex0 )
    self.geomip_terrain.getRoot().setTexture( TextureStage('tex1'),tex1 )
    self.geomip_terrain.getRoot().setTexture( TextureStage('tex2'),tex2 )
    self.geomip_terrain.getRoot().setTexture( TextureStage('tex3'),tex3 )
    self.geomip_terrain.getRoot().setTexture( TextureStage('tex4'),tex4 )
    self.geomip_terrain.getRoot().setTexture( TextureStage('tex5'),tex5 )
    self.geomip_terrain.getRoot().setTexture( TextureStage('tex6'),tex6 )

    # load shader
    self.geomip_terrain.getRoot().setShader(base.loader.loadShader(APP_PATH + 'media/cg/terraintexture.sha'))

    base.taskMgr.add(self.update_terrain, "update-terrain")

    # generate mesh tiles
    #for a in range(0, len(self.subdata)):
    #  for b in range(0, len(self.subdata[a])):
        # generate base mesh
    #    mesh = self.make_base(a, b)
        # generate layer mesh
    #    for i in range(0, len(self.tiles)):
    #      layer = self.make_layer(i, a, b)
    print "    /terrain mesh created in ", self.div, "x", self.div, "tiles"
    # generate num cubes (?)
    self.num_cubes()

  def update_terrain(self, task):
    self.geomip_terrain.update()
    return task.cont

  """make data matrix from heightmap"""
  def make_data(self, hmapfile):
    # open heightmap for reading pixel data
    heightmap = PNMImage()
    heightmap.read(Filename(hmapfile))
    xs = heightmap.getXSize()
    ys = heightmap.getYSize()

    # generate data bi-dimensional array
    data = []
    for x in range(xs):
      data.append([])
      for y in range(ys):
        # set data dictionary properties
        # name
        name = "cell_" + str(x) + "_" + str(y)
        # height
        height = (heightmap.getXel(x, ys - y - 1)[0] * 10)

        if self.retro == True:
          if height < 1 :
            height = height / 5
            height = int(height)
        # c and rgb
        c = [random.random(), random.random(), random.random()]
        rgb = (int(c[0] * 255), int(c[1] * 255), int(c[2] * 255))
        # default texture
        texture = self.tiles[0]['tex']
        texturenum = 0
        score = self.tiles[0]['score']

        # from rgb we assign tex and score
        for n in range(len(self.tiles)):
          if rgb == self.tiles[n]['rgb']:
            texture = self.tiles[n]['tex']
            texturenum = n
            score = self.tiles[n]['score']
            break

        # set terrain data dictionary
        data[x].append({'name':name, 'h':height, 'c':c, 'rgb':rgb, 'tex':texture,
                        'texnum':texturenum, 'score':score})
    return data

  """make subdata matrix from data"""
  def make_subdata(self, base_data = [[]], div = 3):
    # generate subdata
    subdata = []
    for a in range(0, div):
      subdata.append([])
      for b in range(0, div):
        subdata[a].append([])
        # get max, max2
        xmax = int(len(base_data) / div)
        xmax2 = xmax + 1

        if len(base_data) / (div * 1.0) == xmax:
          if a == div - 1:
            xmax2 -= 1
        else:
          if a == div - 1:
            xmax2 += 1

        ymax = int(len(base_data[a]) / div )
        ymax2 = ymax + 1
        if len(base_data[0]) / (div * 1.0) == ymax:
          if b == div - 1:
            ymax2 -= 1
        else:
          if b == div - 1:
            ymax2 += 1

        # get x1, y1
        x1 = a * xmax
        y1 = b * ymax

        # generate subdata
        for x in range(0, xmax2):
          subdata[a][b].append([])
          for y in range(0, ymax2):
            subdata[a][b][x].append([])
            subdata[a][b][x][y] = base_data[x + x1][y + y1]
    return subdata

  """make terrain base mesh from data"""
  def make_base(self, a, b):
    # get data
    data = self.subdata[a][b]
    # set vertex data
    vdata = GeomVertexData('plane', GeomVertexFormat.getV3n3c4t2(), Geom.UHStatic)
    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    color = GeomVertexWriter(vdata, 'color')
    uv = GeomVertexWriter(vdata, 'texcoord')

    # set vertices
    number = 0
    for x in range(0, len(data) - 1):
      for y in range(0, len(data[x]) - 1):
        # get vertex data
        v1 = Vec3(x, y, data[x][y]['h'])
        v2 = Vec3(x + 1, y, data[x+1][y]['h'])
        v3 = Vec3(x + 1, y + 1, data[x+1][y+1]['h'])
        v4 = Vec3(x, y + 1, data[x][y+1]['h'])
        n = (0, 0, 1) # normal

        # assign vertex colors + alpha
        option = 1 # black
        if option == 1:
          c = 0
          c1 = [c, c, c, 1]
          c2 = [c, c, c, 1]
          c3 = [c, c, c, 1]
          c4 = [c, c, c, 1]
        # option2: color vertices
        if option == 2:
          alpha = 1.0
          c1 = [data[x][y]['c'][0], data[x][y]['c'][1],
                data[x][y]['c'][2], alpha]
          c2 = [data[x+1][y]['c'][0], data[x+1][y]['c'][1],
                data[x+1][y]['c'][2], alpha]
          c3 = [data[x+1][y+1]['c'][0], data[x+1][y+1]['c'][1],
                data[x+1][y+1]['c'][2], alpha]
          c4 = [data[x][y+1]['c'][0], data[x][y+1]['c'][1],
                data[x][y+1]['c'][2], alpha]

        if option == 3:
          c1 = self.color_vertex(v1)
          c2 = self.color_vertex(v2)
          c3 = self.color_vertex(v3)
          c4 = self.color_vertex(v4)

        vertex.addData3f(v1)
        normal.addData3f(*n)
        color.addData4f(*c1)
        uv.addData2f(0,0)

        vertex.addData3f(v2)
        normal.addData3f(*n)
        color.addData4f(*c2)
        uv.addData2f(1,0)

        vertex.addData3f(v3)
        normal.addData3f(*n)
        color.addData4f(*c3)
        uv.addData2f(1,1)

        vertex.addData3f(v1)
        normal.addData3f(*n)
        color.addData4f(*c1)
        uv.addData2f(0,0)

        vertex.addData3f(v3)
        normal.addData3f(*n)
        color.addData4f(*c3)
        uv.addData2f(1,1)

        vertex.addData3f(v4)
        normal.addData3f(*n)
        color.addData4f(*c4)
        uv.addData2f(0,1)

#         # add vertex h
#         vertex.addData3f(v1)
#         # normal.addData3f(*n)
#         vertex.addData3f(v2)
#         # normal.addData3f(*n)
#         vertex.addData3f(v3)
#         # normal.addData3f(*n)
#         vertex.addData3f(v1)
#         # normal.addData3f(*n)
#         vertex.addData3f(v3)
#         # normal.addData3f(*n)
#         vertex.addData3f(v4)
#         # normal.addData3f(*n)
#         # add vertex color
#         color.addData4f(*c1)
#         color.addData4f(*c2)
#         color.addData4f(*c3)
#         color.addData4f(*c1)
#         color.addData4f(*c3)
#         color.addData4f(*c4)

        # iterate
        number = number + 2

    # add triangles
    prim = GeomTriangles(Geom.UHStatic)
    for n in range(number):
      prim.addVertices((n * 3) + 2, (n * 3) + 0, (n * 3) + 1)
    prim.closePrimitive()

    # make geom
    geom = Geom(vdata)
    geom.addPrimitive(prim)

    # make geom node
    node = GeomNode("base" + "_" + str(a) + "_" + str(b))
    node.addGeom(geom)

    # make mesh nodePath
    mesh = NodePath(node)
    # set render order
    mesh.setBin("", 1)

    # locate mesh
    mesh.setPos(self.divsep * (a * int(len(self.data[a]) / self.div)),
                self.divsep * (b * int(len(self.data[b]) / self.div)), 0)

    # reparent mesh
    mesh.reparentTo(self.root)

    # return mesh
    return mesh

  def color_vertex(self, vertex):
    alpha = 0.8
    height = float(vertex[2])

    if height < 0.2:
      height += 0.2

    if height < 1:
      return [(height / 2.0), 0, 0, alpha]
    elif height < 4:
      return [0, 0, (height / 7.0), alpha]
    elif height < 7:
      return [0, ((height - 3.0) / 7.0), (height / 7.0), alpha]
    elif height < 8:
      return [0, (height / 8.0), (height / 9.0), alpha]
    elif height < 10:
      return [(height / 14), (height / 10.0), (height / 12.0), alpha]
    else:
      return [(height / 12.0), (height / 12.0), (height / 12.0), alpha]

  def num_cubes(self):
    # create axis cubes
    self.num_cubes = []
    for n in range(len(self.data)):
      self.num_cubes.append(meshes.loadModel(parent = self.ancestor.root,
                                             path = APP_PATH + "media/models/shapes/cube",
                                             name = "num_cube" + str(n),
                                             size = 0.05, pos = (n, -0.5, 0),
                                             color = None))


  def make_layer(self, i, a, b):
    # get data
    data = self.subdata[a][b]

    # set color + alpha of vertex texture
    def ap(n):
      alpha = 0
      if i == n:
        alpha = 1.0
      return alpha
    def tp(n):
      list = [0, 0, 0, 0]
      if i == n:
        list = [1, 1, 1, 0.75]
      return list

    # set vertex data
    vdata = GeomVertexData('plane', GeomVertexFormat.getV3n3c4t2(), Geom.UHStatic)
    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    color = GeomVertexWriter(vdata, 'color')
    uv = GeomVertexWriter(vdata, 'texcoord')

    # set vertices
    number = 0
    for x in range(0, len(data) - 1):
      for y in range(0, len(data[x]) - 1):
        # get vertex data
        v1 = Vec3(x, y, data[x][y]['h'])
        c1 = data[x][y]['c']
        t1 = data[x][y]['texnum']
        v2 = Vec3(x+1, y, data[x+1][y]['h'])
        c2 = data[x+1][y]['c']
        t2 = data[x+1][y]['texnum']
        v3 = Vec3(x+1, y+1, data[x+1][y+1]['h'])
        c3 = data[x+1][y+1]['c']
        t3 = data[x+1][y+1]['texnum']
        v4 = Vec3(x, y+1, data[x][y+1]['h'])
        c4 = data[x][y+1]['c']
        t4 = data[x][y+1]['texnum']
        n=(0, 0, 1) # normal

        # assign vertex colors + alpha
        a1, a2, a3, a4 = ap(t1), ap(t2), ap(t3), ap(t4)
        t1, t2, t3, t4 = tp(t1), tp(t2), tp(t3), tp(t4)

        if v1[2]==0:
          t1 = [data[x][y]['c'][0], data[x][y]['c'][1], data[x][y]['c'][2],
                a1]
        if v2[2]==0:
          t2 = [data[x+1][y]['c'][0], data[x+1][y]['c'][1],
                data[x+1][y]['c'][2], a2]
        if v3[2]==0:
          t3 = [data[x+1][y+1]['c'][0], data[x+1][y+1]['c'][1],
                data[x+1][y+1]['c'][2], a3]
        if v4[2]==0:
          t4 = [data[x][y+1]['c'][0], data[x][y+1]['c'][1],
                data[x][y+1]['c'][2], a4]

        if a1 == 0 and a2 == 0 and a3 == 0 and a4 == 0:
          continue

        # add vertices
        vertex.addData3f(v1)
        normal.addData3f(*n)
        color.addData4f(*t1)
        uv.addData2f(0,0)

        vertex.addData3f(v2)
        normal.addData3f(*n)
        color.addData4f(*t2)
        uv.addData2f(1,0)

        vertex.addData3f(v3)
        normal.addData3f(*n)
        color.addData4f(*t3)
        uv.addData2f(1,1)

        vertex.addData3f(v1)
        normal.addData3f(*n)
        color.addData4f(*t1)
        uv.addData2f(0,0)

        vertex.addData3f(v3)
        normal.addData3f(*n)
        color.addData4f(*t3)
        uv.addData2f(1,1)

        vertex.addData3f(v4)
        normal.addData3f(*n)
        color.addData4f(*t4)
        uv.addData2f(0,1)

        number = number + 2

    # add triangles
    prim = GeomTriangles(Geom.UHStatic)
    for n in range(number):
      prim.addVertices((n * 3) + 2, (n * 3) + 0, (n * 3) + 1)
    prim.closePrimitive()

    # make geom
    geom = Geom(vdata)
    geom.addPrimitive(prim)

    # make geom node
    node = GeomNode("layer" + str(i) + "_" + str(a) + "_" + str(b))
    node.addGeom(geom)

    # make mesh nodePath
    mesh = NodePath(node)

    # load and assign texture
    txfile = self.tiles[i]['tex']
    tx = base.loader.loadTexture(txfile)
    tx.setMinfilter(Texture.FTLinearMipmapLinear)
    mesh.setDepthTest(DepthTestAttrib.MLessEqual)
    mesh.setDepthWrite(False)
    mesh.setTransparency(True)
    mesh.setTexture(tx)

    # set render order
    mesh.setBin("", 1)

    # locate mesh
    mesh.setPos(self.divsep * (a * int(len(self.data[a]) / self.div)),
                self.divsep * (b * int(len(self.data[b]) / self.div)), 0.001)

    # reparent mesh
    mesh.reparentTo(self.root)

    # return mesh
    return mesh


  def getCellPos(self, x, y):
    """ returns the center location of the current cell at the given location """
    # get cell vertices
    v1, v2, v3, v4 = self.getCellVertices(x, y)
    # get cell center point
    x = (v1[0] + v2[0] + v3[0] + v4[0]) / 4.0
    y = (v1[1] + v2[1] + v3[1] + v4[1]) / 4.0
    z = (v1[2] + v2[2] + v3[2] + v4[2]) / 4.0
    return x, y, z

  def getElevation(self, x, y):
    """ returns the terrain elevation at the given xy location
        Uses bilinear interpolation (thanks pro-soft for let me know about that)
        (1-a)(1-b)      a(1-b)    where a and b are the horizontal and vertical
        b(1-a)            ab      distances to the nearest top-left pixel.
    """

    v1, v2, v3, v4 = self.getCellVertices(x, y)
    # get elevation: bilinear interpolation
    a = abs(x - v4[0]) # x distance to top-left
    b = abs(y - v4[1]) # y distance to top-right
    i1 = v4[2] # top-left
    i2 = v3[2] # top-right
    i3 = v1[2] # bottom-left
    i4 = v2[2] # bottom-right
    # bilinear interpolation equation
    z = (1-a) * (1-b) * i1 + (a) * (1-b) * i2 + (1-a) * (b) * i3 + (a)*(b) * i4

    # solve exceptions (not working)
    ## h1,h2,h3,h4=self.getElevationExceptions(v1[2],v2[2],v3[2],v4[2])
    ## i1=h4#top-left
    ## i2=h3#top-right
    ## i3=h1#bottom-left
    ## i4=h2#bottom-right
    ## #bilinear interpolation equation
    ## z=(1-a)*(1-b)*i1 + (a)*(1-b)*i2 + (1-a)*(b)*i3 + (a)*(b)*i4
    return z


  def getCellVertices(self,x,y,debug=False):
    """ calculates the location of the 4 vertices of the current cell
        at the given location
    """
    # vertex 1
    x1 = int(x)
    y1 = int(y)
    z1 = self.data[x1][y1]['h']
    if debug == True:
      self.cube1.setPos(x1, y1, z1)
    # vertex2
    x2 = x1 + 1
    y2 = y1
    z2 = self.data[x2][y2]['h']
    if debug == True:
      self.cube2.setPos(x2, y2, z2)
    #vertex3
    x3 = x1 + 1
    y3 = y1 + 1
    z3 = self.data[x3][y3]['h']
    if debug == True:
      self.cube3.setPos(x3, y3, z3)
    #vertex4
    x4 = x1
    y4 = y1 + 1
    z4 = self.data[x4][y4]['h']
    if debug==True:
      self.cube4.setPos(x4, y4, z4)

    return (x1,y1,z1),(x2,y2,z2),(x3,y3,z3),(x4,y4,z4)


  def getElevationExceptions(self,h1,h2,h3,h4):
    d = 1.05
    d2 = 0.95
    if h1 == h2 and h1 == h3 and h1 != h4:
      h1 = h1 * d
      h2 = h2 * d
      h3 = h3 * d
      h4 = h4 * d2
    if h1==h2 and h1==h4 and h1!=h3:
      h1 = h1 * d
      h2 = h2 * d
      h4 = h4 * d
      h3 = h3 * d2
    if h1==h3 and h1==h4 and h1!=h2:
      h1 = h1 * d
      h3 = h3 * d
      h4 = h4 * d
      h2 = h2 * d2
    if h2==h3 and h2==h4 and h2!=h1:
      h2 = h2 * d
      h3 = h3 * d
      h4 = h4 * d
      h1 = h1 * d2

    return h1, h2, h3, h4







