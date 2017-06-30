text = '''A -> is
B -> mm
C -> oo
D -> rgr
E -> ryg
F -> dth
G -> you
H -> esol
I -> ionA
J -> GDaBarA
K -> veECFHutI
L -> PQ
M -> n
N -> m
O -> oaNcho
P -> MO
Q -> NR
R -> sky
S -> JKL'''.split('\n')
rule = []
for r in text:
    rule.append(r.split(' -> ')[1])
s = 'S'
flag = True
while flag:
    flag = False
    ss = ""
    for x in s:
        if 'A' <= x <= 'Z':
            flag = True
            ss += rule[ord(x) - 65]
        else:
            ss += x
    s = ss
print(s)