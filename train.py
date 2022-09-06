exec(open("schemes.py").read())

def match(pattern, string):
    if len(pattern) != len(string):
        return False
    ok = True
    for i in range(len(pattern)):
        if pattern[i].islower():
            ok &= (string[i] == pattern[i])
        else:
            ok &= (string[i] in sets[pattern[i]])
    return ok

def atom(S, pos):
    for p in rules:
        if match(p, S[pos:]):
            return S[pos:(pos+len(p))]
    for p in multirules:
        if match(p[0], S[pos-len(p[0]):pos]) and match(p[1], S[pos:pos+len(p[1])]) and match(p[2], S[pos+len(p[1]):pos+len(p[1])+len(p[2])]):
            return S[pos:(pos+len(p[1]))]
    return S[pos]

def parse(S):
    S = S.lower()

    out = []
    i = 0
    while i < len(S):
        a = atom(S, i)
        out.append(a)
        i += len(a)

    return out

training = []
network = {}
sums = {}

def train():
    for s in map(parse, training):
        s.insert(0, ' ')
        s.insert(0, ' ')
        s.append(' ')
        for i in range(len(s)-2):
            t = (s[i], s[i+1])
            n = s[i+2]

            if t not in network:
                network.update({t: {}})
            if n not in network[t]:
                network[t].update({n: 0})
            network[t][n] += 1
            
            if t not in sums:
                sums.update({t: 0})
            sums[t] += 1

    for k in network.keys():
        for l in network[k].keys():
            network[k][l] *= 10000
            network[k][l] += sums[k]
            network[k][l] //= sums[k]

def import_data():
    f = open("data.txt", "r")
    for x in f:
        training.append(x.strip())
    f.close()

def save():
    f = open("network.py", "w")
    f.write("network = ")
    f.write(str(network))
    f.close()

import_data()
train()
save()
