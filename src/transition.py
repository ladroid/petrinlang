class Transition:
  def __init__(self, out_arc, in_arc):
    self.out_arc = set(out_arc)
    self.arcs = self.out_arc.union(in_arc)
  def fire(self):
    not_blocked = all(arc.non_block() for arc in self.out_arc)
    if not_blocked:
      for arc in self.arcs:
        arc.trigger()
    return not_blocked # return if fired, just for the sake of debuging