import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from src.arc import Arc
class Out(Arc):
  def trigger(self):
    self.place.markers -= self.amount
  def non_block(self):
    return self.place.markers >= self.amount