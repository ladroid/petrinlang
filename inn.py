from arc import Arc
class In(Arc):
  def trigger(self):
    self.place.markers += self.amount