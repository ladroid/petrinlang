from pyparsing import *
from place import Place
from net import PetriNet
from arc import Arc
from out import Out
from inn import In
from transition import Transition
from random import choice
import functools
def exmps():
  '''
  grammar:
  ssn ::= nums+ '-' nums+ '-' nums+
  nums ::= '0' | '1' | '2' etc etc
  '''
  dash = '-'

  ssn_parser = Combine(
    Word(nums, exact=3)
    + dash
    + Word(nums, exact=2)
    + dash
    + Word(nums, exact=4)
  )

  input_string = '''
    xxx 225-92-8416 yyy
    103-33-3929 zzz 028-91-0122
  '''

  for match, start, stop in ssn_parser.scanString(input_string):
    print(match, start, stop)

def other():
  val = Word(nums)
  arrow_left = '<-'
  arrow_right = '->'
  narrow = '|'
  star = '*'
  term = val | arrow_left | arrow_right | narrow | star
  
  arra = Forward()
  arra << Word(nums) + Suppress(',') + ZeroOrMore(arra)
  
  place = Literal('place')
  lbrac = Literal('[')
  rbrac = Literal(']')
  fire = Literal('time')
  equal = Literal('=')
  grops = Group(place + equal + lbrac + arra + rbrac + fire + equal + Word(nums) + star + OneOrMore(term)).parseString('place=[ 1,0, ] time=10 * -> <- | -> *')
  for i in grops:
    petri(i)

def petri(elements):
  print(elements)
  between = ''
  list_places = []
  in_statement = False
  checklbrac = '['
  checkrbrac = ']'
  checktime = 'time'
  checkstar = '*'
  checknarrow = '|'

  checkless = '<'
  checkmore = '>'

  listoutinbeforenarrow = []
  listoutinafternarrow = []

  for i in elements:
    if checklbrac in i:
      in_statement = True
    if in_statement:
      between += i
    if checkrbrac in i:
      in_statement = False
      break
  between = between.replace('[','').replace(']','')
  for i in between:
    list_places.append(int(i))
  print(list_places)

  between = ''
  for i in elements:
    if checktime in i:
      in_statement = True
    if in_statement:
      between += i
    if checkstar in i:
      in_statement = False
      break
  between = between.replace('time','').replace('*','').replace('=', '')
  firings = int(between)
  print(firings)

  between = ''
  for i in elements:
    if checkstar in i:
      in_statement = True
    if in_statement:
      between += i
    if checknarrow in i:
      in_statement = False
      break
  between = between.replace('*','').replace('|','')
  for i in between:
    listoutinbeforenarrow.append(i)
  print(listoutinbeforenarrow)

  listoutinafternarrow = elements[13]
  #between = between.replace('|','').replace('*','')
  # for i in between:
  #   listoutinafternarrow.append(i)
  # print(listoutinafternarrow)

  ps = [Place(m) for m in list_places]

  countless = 0
  countmore = 0

  for i in listoutinbeforenarrow:
    if checkless in i:
      countless += 1
    if checkmore in i:
      countmore += 1
  print(countless, countmore)

  listout = []
  listin = []
  for i in range(countless):
    listout = [Out(ps[i])]
  for i in range(countmore):
    listin = [In(ps[i])]

  for i in range(1):
    ts = dict(i=Transition(listout, listin + [In(ps[1])]))
    # a = elements[0]
    # firings = elements[1]
    # coeff = [num for num in elements[2:] if isinstance(num, int)]
    # print('all coeff', coeff)

    # ps = [Place(m) for m in a]
    # ts = dict(
    #      t1=Transition(
    #          [Out(ps[0])], 
    #          [In(ps[0]), In(ps[1])]
    #     )
        # t2=Transition(
        #     [Out(ps[1])],
        #     [In(ps[2]), In(ps[0])])
    #     ,)
    
    firing_sequence = [choice(list(ts.keys())) for _ in range(firings)] # stochastic execution
    print(firing_sequence)
    petri_net = PetriNet(ts)
    petri_net.run(firing_sequence, ps)

other()
