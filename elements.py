import z3

class Element(object):
  def __init__(self, name):
    self.name = name

  def draw(self, cursor, model):
    raise NotImplemented

class Point(Element):
  def __init__(self, name: str):
    super(Point, self).__init__(name)
    self.x = z3.Real(f'{name}.x')
    self.y = z3.Real(f'{name}.y')

  def draw(self, cursor, model):
    pass

def as_float(model, decl):
  ref = model.evaluate(decl)
  if hasattr(ref, 'approx'):
    ref = ref.approx()
  return float(ref.as_fraction())

class Segment(Element):
  def __init__(self, name:str):
    super(Segment, self).__init__(name)
    self.a = Point(f'{name}.a')
    self.b = Point(f'{name}.b')

  def draw(self, cursor, model):
    ax = as_float(model, self.a.x)
    ay = as_float(model, self.a.y)
    bx, by = as_float(model, self.b.x), as_float(model, self.b.y)
    print(ax, ay, bx, by)
    cursor.move_to(ax, ay)
    cursor.line_to(bx, by)
    cursor.stroke()

class Circle(Element):
  def __init__(self, name: str):
    super(Circle, self).__init__(name)
    self.center = Point(f'{name}.center')
    self.radius = z3.Real(f'{name}.r')

class Arc(Element):
  def __init__(self):
    super(Arc, self).__init__(name)
    self.center = Point(f'{name}.center')
    self.alpha = z3.Real('alpha')
    self.beta = z3.Real('beta')
