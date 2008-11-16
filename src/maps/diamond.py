import os
import random
import __builtin__
from pandac.PandaModules import PNMImage, Filename

APP_PATH = __builtin__.APP_PATH

"""
DiamondMap:
 Generates a random procedural heighmap of given size(**2+1) using
   Diamond Square algorithm and saves it to disk.
 If wanted, splits the heightmap in x*y subimages and saves them to disk.
"""

class DiamondMap:
  def __init__(self, heightmap_file = None, size = 33, height_modifier = 2):
    # init heightmap
    heightmap = self.init_map(size, False)

    # make random map
    heightmap = self.random_map(heightmap, False, (0.0, 0.0, 0.0, 0.0))

    # draw heightmap
    drawn_heightmap = self.draw_map(heightmap, height_modifier)

    # save map
    drawn_heightmap.write(Filename(heightmap_file))
    print "    /height map saved in", heightmap_file

  def init_map(self, size, random_data = False):
    """Generate random static or a blank map"""
    heightmap = []

    if random_data:
      # random noise background
      for x in range(size):
        heightmap.append([])
        for y in range(size):
          heightmap[-1].append(random.random())
    else:
      # black background
      for x in range(size):
        heightmap.append([])
        for y in range(size):
          heightmap[-1].append(0.0)

    return heightmap

  def draw_map(self, heightmap, height_modifier):
    """Draws the heightmap in the image
       The range of values is assumed to be 0.0 to 1.0 in a 2D, square array.
       The range is converted to grayscale values of 0 to 255.
       A heightmap modifier is added to boost height differences.
    """
    # get size
    size = (len(heightmap), len(heightmap[0]))

    # create image
    hmap = PNMImage(size[0], size[1])

    # draw map
    for y in range(size[0]):
      for x in range(size[1]):
        h = (heightmap[x][y]) * height_modifier
        try:
          hmap.setXel(x, y, h)
        except:
          print "Error on x,y: ", str((x, y)), "; map --> 0-255 value: ", str((heightmap[x][y], h))

    return hmap

  def random_map(self, heightmap, show_in_progress = False,
                 seed_values = (0.5, 0.5, 0.5, 0.5)):
    """Make procedural terrain using the D/S Algorithm"""
    # get size
    size = len(heightmap)

    # Seed the corners
    corners = ((0, 0), (size - 1, 0), (0, size - 1), (size - 1, size -1))
    for n in range(4):
      point = corners[n]
      heightmap[point[0]][point[1]] = seed_values[n]

    # Starting values
    ## For edge-wrapping purposes.
    size_minus_1 = size - 1
    ## cell_size lets us repeat the algorithm over sections
    ## of this size each time.  After one pass we decrease the cell_size
    ## to match what we just subdivided so we can subdivide again.
    cell_size = size - 1
    cell_size_half = cell_size / 2

    ## How many times have we done the algorithm?
    iteration = 0

    ## Total possible variation of a height from expected average
    chaos = 1.0
    ## Possible variation up or down
    chaos_half = chaos * 0.5
    diamond_chaos_half = (chaos / 1.414) * 0.5 ## Reduced by sqrt(2) for D step.

    # While our cell_size is greater than 1 we keep repeating
    # the algorithm.
    while cell_size > 1:
      # Begin the algorithm
      iteration += 1

      # Find the anchor points that mark the upper-left corner of each cell
      for anchor_y in range(0, size - 1, cell_size):
        for anchor_x in range(0, size - 1, cell_size):
          # Calculate the center of the cell
          cx = anchor_x + cell_size_half
          cy = anchor_y + cell_size_half

          # The "Diamond" phase

          neighbors = ([cx - cell_size_half, cy - cell_size_half],
                       [cx + cell_size_half, cy - cell_size_half],
                       [cx - cell_size_half, cy + cell_size_half],
                       [cx + cell_size_half, cy + cell_size_half])

          # Correct for points outside the map
          for n in range(4):
            neighbor = neighbors[n]
            if neighbor[0] < 0:
              neighbors[n][0] += size
            elif neighbor[0] > size:
              neighbors[n][0] -= size
            if neighbor[1] < 0:
              neighbors[n][1] += size
            elif neighbor[1] > size:
              neighbors[n][1] -= size

          average = sum([heightmap[n[0]][n[1]] for n in neighbors]) * .25
          h = average - chaos_half + (random.random() * chaos)
          h = max(0.0, min(1.0, h))
          heightmap[cx][cy] = h

          # The "Square" phase

          # Calculate four "edge points" surround the center
          edge_points = ((cx, cy - cell_size_half),
                         (cx - cell_size_half, cy),
                         (cx + cell_size_half, cy),
                         (cx, cy + cell_size_half))
          for point in edge_points:
            neighbors = [[point[0], point[1] - cell_size_half],
                         [point[0] - cell_size_half, point[1]],
                         [point[0] + cell_size_half, point[1]],
                         [point[0], point[1] + cell_size_half]]

            # Correct for points outside the map
            for n in range(4):
              neighbor = neighbors[n]
              if neighbor[0] < 0:
                neighbors[n][0] += size
              elif neighbor[0] > size_minus_1:
                neighbors[n][0] -= size
              if neighbor[1] < 0:
                neighbors[n][1] += size
              elif neighbor[1] > size_minus_1:
                neighbors[n][1] -= size

            average = sum([heightmap[n[0]][n[1]] for n in neighbors]) * .25
            h = average - chaos_half + (random.random() * chaos)
            h = max(0.0,min(1.0,h))
            heightmap[point[0]][point[1]] = h

      # End of iteration. Reduce cell size and chaos.
      cell_size /= 2
      cell_size_half /= 2
      chaos *= .45
      chaos_half = chaos * .55#.5
      diamond_chaos_half = (chaos / 1.414) * .25

    return heightmap





