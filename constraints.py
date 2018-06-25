import math
from typing import Union

import z3

import elements

class Constraint(object):
  def __init__(self):
    pass

class Coincident(Constraint):
  def __init__(self, a: elements.Point, b: elements.Point):
    self.term = z3.And([
      a.x == b.x,
      a.y == b.y])

def Cosine(theta):
  return z3.parse_smt2_string('(cos theta)', decls={'theta': theta})

def DistanceSquared(a: elements.Point, b: elements.Point):
  return ((b.x - a.x) ** 2 + (b.y - a.y) ** 2)

def LengthSquared(s: elements.Segment):
  return DistanceSquared(s.a, s.b)

def DotProduct(a: elements.Segment, b: elements.Segment):
  # Treat both segments as vectors at the origin.
  vector1 = (a.b.x - a.a.x, a.b.y - a.a.y)
  vector2 = (b.b.x - b.a.x, b.b.y - b.a.y)
  dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
  return dot_product

def PerpProduct(a: elements.Segment, b: elements.Segment):
  # Treat both segments as vectors at the origin.
  vector1 = (a.b.x - a.a.x, a.b.y - a.a.y)
  vector2 = (b.b.x - b.a.x, b.b.y - b.a.y)
  perp_of_vector2 = (-vector2[1], vector2[0])
  perp_product = (vector1[0] * perp_of_vector2[0] + vector1[1] * perp_of_vector2[1])
  return perp_product

class Horizontal(Constraint):
  def __init__(self, s: elements.Segment):
    self.term = s.a.y == s.b.y

class Vertical(Constraint):
  def __init__(self, s: elements.Segment):
    self.term = s.a.x == s.b.x

class HorizontalMeasure(Constraint):
  def __init__(self, a: elements.Point, b: elements.Point, d: float):
    self.term = z3.Abs(b.x - a.x) == d

class VerticalMeasure(Constraint):
  def __init__(self, a: elements.Point, b: elements.Point, d: float):
    self.term = z3.Abs(b.y - a.y) == d

class DistanceMeasure(Constraint):
  def __init__(self, a: elements.Point, b: elements.Point, d: float):
    self.term = DistanceSquared(a, b) == d**2

class LengthMeasure(DistanceMeasure):
  def __init__(self, s:elements.Segment, d: float):
    self.term = LengthSquared(s) == d**2

class AngleMeasure(Constraint):
  def __init__(self, a: elements.Segment, b: elements.Segment, theta: float):
    theta = theta % math.pi
    self.term = (DotProduct(a, b) ** 2 == LengthSquared(a) * LengthSquared(b) *
                 Cosine(theta) * Cosine(theta))

class Parallel(AngleMeasure):
  def __init__(self, a: elements.Segment, b: elements.Segment):
    self.term = PerpProduct(a, b) == 0

class Perpendicular(AngleMeasure):
  def __init__(self, a: elements.Segment, b: elements.Segment):
    self.term = DotProduct(a, b) == 0

  # distance
  # radius
  # angle


class Tangency(Constraint):
  # 1. Perpendicular to a radius and incident.
  # 2. Closest point is exactly radius distant.
  def __init__(
      self, base: Union[elements.Arc, elements.Circle],
      tangent: Union[elements.Segment, elements.Arc, elements.Circle]):
    self.base = base
    self.tangent = tangent

    self.tangent_point = elements.Point()

    if isinstance(base, elements.Arc):
      pass
      # self.term = z3.And(self.term, point of tangency within angle bound of arc)
