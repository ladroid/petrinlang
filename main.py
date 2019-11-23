from lark import Lark, Transformer, Visitor, Tree, v_args, UnexpectedInput
from place import Place
from net import PetriNet
from arc import Arc
from out import Out
from inn import In
from transition import Transition
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
petri: "petrin" "->" "place=" array "," "time=" value "," star arrow narrow arrow star

star: ["*" ("*")*]

arrow: ["<-" ("<-")*] | ["->" ("->")*]

narrow: ["|" ("|")*]

string : ESCAPED_STRING

%import common.NUMBER
%import common.SIGNED_NUMBER
%import common.ESCAPED_STRING
%import common.CNAME -> NAME
%import common.WS_INLINE
%ignore " "
%ignore WS_INLINE
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
    ps = [Place(m) for m in a]
    ts = dict(
        t1=Transition(
            [Out(ps[1])],
            [In(ps[2])]),
        t2=Transition(
            [Out(ps[1])],
            [In(ps[2]), In(ps[0])]),)
    firing_sequence = [choice(list(ts.keys())) for _ in range(firings)] # stochastic execution
    print(firing_sequence)
    petri_net = PetriNet(ts)
    petri_net.run(firing_sequence, ps)
    # def inn(self, *elements):
    #     return [elements]
        # alist = []
        # #for i in elements:
        # alist.append(elements)
        # ps = [Place(m) for m in alist]
        # for i in ps:
        #     return i
    # def outt(self, *elements):
    #     return [elements]
        # alist = []
        # #for i in elements:
        # alist.append(elements)
        # ps = [Place(m) for m in alist]
        # for i in ps:
        #     return i


l = Lark(grammar, parser='lalr', transformer=LanguageTransformer())
file = open('example.pn', 'r')
print(l.parse(file.read()))