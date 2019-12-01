import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lark import Lark, Transformer, Visitor, Tree, v_args, UnexpectedInput
from src.place import Place
from src.net import PetriNet
from src.arc import Arc
from src.out import Out
from src.inn import In
from src.transition import Transition
from random import choice
import functools
grammar = '''
?start: calc | NAME "=" calc -> assign | value | printval | petri

?calc: prod | calc "+" prod -> add | calc "-" prod -> sub

?prod: atom | prod "*" atom -> mul | prod "/" atom -> div

?atom: NUMBER -> number | "-" atom -> neg | NAME -> var | "("calc")"

?value: array | SIGNED_NUMBER -> number | string

?array: "[" [value ("," value)*] "]"

?printval: "print" value
petri: "petrin" "->" "place=" array "," "time=" value "," star [ arrow_left value (arrow_left)*  value arrow_right | value arrow_right (arrow_right)* arrow_left value | arrow_left value (arrow_left)* | value arrow_right (arrow_right)*] value narrow [arrow_left value (arrow_left)* value arrow_right | value arrow_right (arrow_right)* arrow_left value | arrow_left value (arrow_left)* | value arrow_right (arrow_right)*] star

?star: ["*" ("*")*]

?arrow_left: "<-"
?arrow_right: "->"

arrow: ["<-" ("<-")*] | ["->" ("->")*]

narrow: ["|" ("|")*]

string : ESCAPED_STRING

%import common.NUMBER
%import common.SIGNED_NUMBER
%import common.ESCAPED_STRING
%import common.CNAME -> NAME
%import common.WS_INLINE
%import common.WS
%ignore " "
%ignore WS_INLINE
%ignore WS
'''

@v_args(inline=True)
class LanguageTransformer(Transformer):
  from operator import add, sub, mul, truediv as div, neg
  number = int
  def __init__(self):
    self.vars = {}
  def assign(self, name, args):
    self.vars[name] = args
    return args
  def var(self, name):
    return self.vars[name]
  def array(self, *elements):
    l = []
    for a in elements:
      l.append(a)
    return l
  def petri(self, *elements):
    a = elements[0]
    firings = elements[1]
    coeff = [num for num in elements[2:] if isinstance(num, int)]
    print('all coeff', coeff)
    ps = [Place(m) for m in a]

    ts = None
    # if len(coeff) > 4:
    #   pass
    # else:
    #   innid1 = coeff[0]
    #   outid = coeff[1]
    #   transid = coeff[2]
    #   innid2 = coeff[3]
    #   innli1 = [] 
    #   outli = []
    #   innli2 = []
    #   for i in range(innid1):
    #     innli1=[In(ps[i])]
    #   for i in range(outid):
    #     outli=[Out(ps[i])]
    #   for i in range(innid2):
    #     innli2=[In(ps[i+1])]
    #   summ = innli1 + innli2
    #   for i in range(transid):
    #     ts = dict(i=Transition(outli, summ))
    #print(ts)

    ts = dict(t1=Transition([Out(ps[0])], [In(ps[0]), In(ps[1]), In(ps[2])]),
    t2=Transition([Out(ps[1]), Out(ps[2])], [In(ps[3])]),
    t3=Transition([Out(ps[2])], [In(ps[3])]))

    # ts = dict(
    #      t1=Transition(
    #          [Out(ps[0])], 
    #          [In(ps[0]), In(ps[1])]
    #     )
        # t2=Transition(
        #     [Out(ps[1])],
        #     [In(ps[2]), In(ps[0])])
        #,)
    firing_sequence = [choice(list(ts.keys())) for _ in range(firings)] # stochastic execution
    print(firing_sequence)
    petri_net = PetriNet(ts)
    petri_net.run(firing_sequence, ps)

'''
examp1
1 -> <- | -> *


examp2
    -> | -> *
100  
    -> | -> *

examp1
# li = [1,0]
# firings = 10

# ps = [Place(m) for m in li]
# ts = dict(
#     t1=Transition(
#         [Out(ps[0])], 
#         [In(ps[0]), In(ps[1])]
#         ),
#     # t2=Transition(
#     #     [Out(ps[1]), Out(ps[2])], 
#     #     [In(ps[3]), In(ps[0])]
#     #     ),
#     )

examp2
# li = [100, 0, 0]
# firings = 10
# ps = [Place(m) for m in li]
# ts = dict(
#     t1=Transition([Out(ps[0])], [In(ps[1])]),
#     t2=Transition([Out(ps[0])], [In(ps[2])])
# )

'''

l = Lark(grammar, parser='lalr', transformer=LanguageTransformer())
file = open('example.pn', 'r')
print(l.parse(file.read()))