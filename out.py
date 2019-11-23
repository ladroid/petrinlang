from arc import Arc
class Out(Arc):
  def trigger(self):
    self.place.markers -= self.amount
  def non_block(self):
    return self.place.markers >= self.amount