import random

class ProceduralUtility:
  def small_random_axis(vector_list):
    forward = vector_list[0]
    perp1 = vector_list[1]
    perp2 = vector_list[2]

    new_forward = forward + perp1 * (1 * random.random() - 0.5) + perp2 * (1 * random.random() - 0.5)
    new_forward.normalize()

    new_perp2 = new_forward.cross(perp1)
    new_perp2.normalize()

    new_perp1 = new_forward.cross(new_perp2)
    new_perp1.normalize()

    return [new_forward, new_perp1, new_perp2]
  small_random_axis = staticmethod(small_random_axis)

  def random_axis(vector_list):
    forward = vector_list[0]
    perp1 = vector_list[1]
    perp2 = vector_list[2]

    new_forward = forward + perp1 * (2 * random.random() - 1) + perp2 * (2 * random.random() - 1)
    new_forward.normalize()

    new_perp2 = new_forward.cross(perp1)
    new_perp2.normalize()

    new_perp1 = new_forward.cross(new_perp2)
    new_perp1.normalize()

    return [new_forward, new_perp1, new_perp2]
  random_axis = staticmethod(random_axis)
