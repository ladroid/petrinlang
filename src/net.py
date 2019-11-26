class PetriNet:
  def __init__(self, transitions):
    self.transitions = transitions

  def run(self, firing_sequence, ps):
    print('Using firing sequence:\n', ' => '.join(firing_sequence))
    print('start {}\n'.format([p.markers for p in ps]))

    for name in firing_sequence:
      t = self.transitions[name]
      if t.fire():
        print('{} fired!'.format(name))
        print('  =>  {}'.format([p.markers for p in ps]))
      else:
        print('{} ...fizzled.'.format(name))

    print('\nfinal {}'.format([p.markers for p in ps]))