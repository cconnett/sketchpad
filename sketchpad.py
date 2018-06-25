"""A constraint-based 2D geometry drawing tool."""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import z3

import constraints
import elements

class Drawing(object):
  def __init__(self):
    self.elements = []
    self.constraints = []

    self.model = None

  def solve(self):
    self.solver = z3.Solver()
    for constraint in self.constraints:
      self.solver.add(constraint.term)
    status = self.solver.check()
    if status == z3.sat:
      self.model = self.solver.model()
    return status

  def draw(self, cursor):
    if not self.model:
      return
    for element in self.elements:
      element.draw(cursor, self.model)
    print()

class Output(Gtk.Window):
  def __init__(self, drawing):
    super(Output, self).__init__()
    self.canvas = Gtk.DrawingArea()
    self.add(self.canvas)
    self.canvas.connect("draw", self.on_draw)
    self.set_title("Sketchpad")
    self.set_position(Gtk.WindowPosition.CENTER)
    self.connect("delete-event", Gtk.main_quit)
    self.show_all()

    self.drawing = drawing

  def on_draw(self, wid, cursor):
    cursor.set_source_rgb(0,0,0)
    cursor.set_line_width(0.1)
    cursor.translate(600, 400)
    cursor.scale(75, -75)
    self.drawing.draw(cursor)


def main():
  dr = Drawing()
  dr.elements.append(elements.Segment('one'))
  dr.elements.append(elements.Segment('two'))
  dr.elements.append(elements.Segment('three'))
  dr.elements.append(elements.Segment('four'))
  dr.constraints.append(constraints.Coincident(dr.elements[0].b, dr.elements[1].a))
  dr.constraints.append(constraints.Coincident(dr.elements[1].b, dr.elements[2].a))
  dr.constraints.append(constraints.Coincident(dr.elements[2].b, dr.elements[3].a))
  dr.constraints.append(constraints.Coincident(dr.elements[3].b, dr.elements[0].a))
  dr.constraints.append(constraints.LengthMeasure(dr.elements[0], 4))
  dr.constraints.append(constraints.Parallel(dr.elements[0], dr.elements[2]))
  dr.constraints.append(constraints.Parallel(dr.elements[1], dr.elements[3]))
  dr.constraints.append(constraints.Perpendicular(dr.elements[1], dr.elements[2]))

  dr.solve()
  print(dr.model)

  window = Output(dr)
  window.canvas.queue_draw()
  Gtk.main()

if __name__ == '__main__':
  main()
