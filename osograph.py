#!/usr/bin/env python

import sys, os
import re

syms = {}
insts = []

class Inst:

    def __init__(self, inst, ty, dst, srcs):
        self.inst = inst
        self.ty = ty
        self.dst = dst
        self.srcs = srcs

    def __str__(self):
        s = "%s %s %s" % (self.inst, self.ty, self.dst)
        for src in self.srcs:
            s += " %s" % src
        return s

def searchInst(start, name):

    # Simple backward linear search.
    for i in range(start, -1, -1):
        if insts[i].dst == name:
            return i

    return -1   # = not found

def parseGlobal(t):

    ty = t[1]
    i = 2
    if ty == "closure":
        ty = t[i]
        i = i + 1

    name = t[i]

    syms[name] = ('global', ty, name)
    insts.append(Inst('global', ty, name, []))

def parseLocal(t):

    ty = t[1]
    i = 2
    if ty == "closure":
        ty = t[i]
        i = i + 1

    name = t[i]

    syms[name] = ('local', ty, name)
    insts.append(Inst('local', ty, name, []))

def parseTemp(t):

    ty = t[1]
    i = 2
    if ty == "closure":
        ty = t[i]
        i = i + 1

    name = t[i]

    syms[name] = ('temp', ty, name)
    insts.append(Inst('temp', ty, name, []))

def parseConst(t):

    ty = t[1]
    reg = t[2]
    assert reg[0] == '$'

    val = t[3]

    print val
    if val[0] == '"':  # string begin
        s = val
        if val[-1] != '"':
            for i in range(4, len(t)):
                while t[i][-1] != '"':
                    s += " " + t[i]
                    i = i + 1
                s += " " + t[i]
                break

        val = s

    syms[reg] = ('const', ty, reg)
    insts.append(Inst('const', ty, reg, [val]))

def parseFun(t):

    funname = t[0]
    dst = t[1]
    srcs = []
    for i in range(2, len(t)):
        if t[i][0] == '%':  # hint
            break

        srcs.append(t[i])

    s = syms[dst]
    ty = s[1]

    insts.append(Inst(funname, ty, dst, srcs))

def parseAssign(t):

    dst = t[1]
    src = t[2]

    s = syms[dst]
    ty = s[1]

    insts.append(Inst('assign', ty, dst, [src]))

def parseCompAssign(t):

    dst = t[1]
    comp = t[2]
    src = t[3]

    s = syms[dst]
    ty = s[1]

    insts.append(Inst('compassign', ty, dst, [src]))

def parseCompRef(t):

    dst = t[1]
    src = t[2]
    comp = t[3]

    s = syms[dst]
    ty = s[1]

    insts.append(Inst('compref', ty, dst, [src]))

def parseMul(t):

    dst = t[1]
    src0 = t[2]
    src1 = t[3]

    s = syms[dst]
    ty = s[1]

    insts.append(Inst('mul', ty, dst, [src0, src1]))

def parseSqrt(t):

    dst = t[1]
    src = t[2]

    s = syms[dst]
    ty = s[1]

    insts.append(Inst('sqrt', ty, dst, [src]))

def parseSqrt(t):

    dst = t[1]
    src0 = t[2]
    src1 = t[3]

    s = syms[dst]
    ty = s[1]

    insts.append(Inst('mul', ty, dst, [src0, src1]))

def dumpGraph():

    f = open("output.dot", "w")

    print >>f, "digraph G {"

    # emit nodes
    for (n, i) in enumerate(insts):

        id = "node%d" % n
        s = id

        # espcape '"' and '\'
        ss = re.sub(r'\\', r'\\\\', str(i))
        ss = re.sub(r'"', '\\"', ss)
        s += " [label=\"%s\"]" % ss

        print >>f, s

    # emit links
    for (n, i) in enumerate(insts):
        for src in i.srcs:
            k = searchInst(n-1, src)
            if k >= 0:
                print >>f, "node%d -> node%d" % (k, n)

        k = searchInst(n-1, i.dst)
        if k >= 0:
            print >>f, "node%d -> node%d" % (n, k)
    

    print >>f, "}"

    f.close()
    

def main():
    
    if len(sys.argv) < 2:
        print "Needs input"
        sys.exit(-1)

    f = open(sys.argv[1], "r")

    for l in f:
        t = l.split()
        if len(t) < 2: continue

        if t[0] == 'OpenShadingLanguage': continue
        elif t[0] == '#': continue        # comment        
        elif t[0] == 'shader': continue   # comment        
        elif t[0] == 'param': continue   # comment        
        elif t[0] == 'code': continue   # comment        
        elif t[0] == 'const': parseConst(t)
        elif t[0] == 'global': parseGlobal(t)
        elif t[0] == 'local': parseLocal(t)
        elif t[0] == 'temp': parseTemp(t)
        elif t[0] == 'assign': parseAssign(t)
        elif t[0] == 'compassign': parseCompAssign(t)
        elif t[0] == 'compref': parseCompRef(t)
        elif t[0] == 'mul': parseMul(t)
        elif t[0] == 'sqrt': parseSqrt(t)
        else: parseFun(t)

        print t

    f.close()

    dumpGraph()

    print "# SYMS ---------------------------"
    for s in syms:
        print s

    print "# INSTS --------------------------"
    for (n, i) in enumerate(insts):
        for src in i.srcs:
            k = searchInst(n-1, src)
            if k >= 0:
                print "%s = %d" % (src, k)
        print i

# ---
main()
