# zero recursion, 
# no "try and fail" and recurse new attempt
# instead iteratively apply rules until done

# moderate
strboard = '''
|695 1    |
|73 4 621 | 
|24  7 365|
|   681   |
|   534   |
|   792  4|
| 1 84    |
| 84 2   3|      
|5 2      |
'''
strboard = '''
|   4     |
|    6 1  | 
|679      |
|  8  3   |
|3   416  |  
| 1 6 78 4|
| 8 975  1|
|    1    |
|9       5|
'''

mlines = strboard.splitlines()

def pos2rowcol(pos):
    return int(pos/9),pos%9

def rowcol2pos(row,col):
    return row*9+col

# initial board
candidates = []
for pos in range(81):
    row,col = pos2rowcol(pos)
    rowstring = mlines[row+1]
    colchar = rowstring[col+1]
    if colchar == ' ':
        candidates.append(['1','2','3','4','5','6','7','8','9'])
    else:
        candidates.append([colchar])

def multiplechoices(candidates):
    for pos in range(81):
        if len(candidates[pos]) > 1:
            return True
    return False

def samerow(pos):
    currow,curcol = pos2rowcol(pos)
    return [rowcol2pos(currow,c) for c in range(9) if c != curcol]

def samecol(pos):
    currow,curcol = pos2rowcol(pos)
    return [rowcol2pos(r,curcol) for r in range(9) if r != currow]

def samebox(pos):
    currow,curcol = pos2rowcol(pos)
    boxrowstart = int(currow/3)*3
    boxcolstart = int(curcol/3)*3
    return [rowcol2pos(r,c) for r in range(boxrowstart,boxrowstart+3) for c in range(boxcolstart,boxcolstart+3) if not (r==currow and c==curcol)]

def nomatchingsingleton(candidates,pos,search):
    numRemovals = 0
    for spos in search:
        if len(candidates[spos]) == 1:
            schar = candidates[spos][0]
            if schar in candidates[pos]:
                prow, pcol = pos2rowcol(pos)
                srow, scol = pos2rowcol(spos)
                print(f"Removing {schar} at {prow},{pcol} because singleton at {srow},{scol}")
                candidates[pos].remove(schar)
                numRemovals += 1
    return numRemovals

def nomatchingpair(candidates,pos,search):
    numRemovals = 0
    for s1pos in search:
        for s2pos in search:
            if s1pos != s2pos:
                if len(candidates[s1pos]) ==2 and len(candidates[s2pos]) ==2 and candidates[s1pos] == candidates[s2pos]:
                    for schar in candidates[s1pos]:
                        if schar in candidates[pos]:
                            print(f"Removing {schar} at {pos2rowcol(pos)} because of pair at {pos2rowcol(s1pos)} and {pos2rowcol(s2pos)}")
                            candidates[pos].remove(schar)
                            numRemovals += 1
    return numRemovals

def nomatchingtriple(candidates,pos,search):
    numRemovals = 0
    for s1pos in search:
        for s2pos in search:
            if s1pos != s2pos:
                for s3pos in search:
                    if s1pos != s3pos and s2pos != s3pos:
                        if len(candidates[s1pos]) <=3 and len(candidates[s2pos]) <=3 and len(candidates[s3pos])<=3:
                            mergedSet = set(candidates[s1pos] + candidates[s2pos] + candidates[s3pos])
                            if len(mergedSet) == 3:
                                for schar in mergedSet:
                                    if schar in candidates[pos]:
                                        print(f"Removing {schar} at {pos2rowcol(pos)} because of triple at {pos2rowcol(s1pos)} and {pos2rowcol(s2pos)}")
                                        candidates[pos].remove(schar)
                                        numRemovals += 1
    return numRemovals

def applyrule(rule, candidates, pos):
    numRemoved = rule(candidates, pos, samerow(pos))
    numRemoved += rule(candidates, pos, samecol(pos))
    numRemoved += rule(candidates, pos, samebox(pos))
    return numRemoved

# while multiplechoices(candidates):
while True: 
    removed=0
    for pos in range(81):
        if len(candidates[pos])>1:
            # print(f"{pos=} samerow={samerow(pos)} samecol={samecol(pos)} samebox={samebox(pos)}")
            removed += applyrule(nomatchingsingleton, candidates, pos)
            removed += applyrule(nomatchingpair, candidates, pos)
            removed += applyrule(nomatchingtriple, candidates, pos)
    if removed>0:
        pass
        # print("Singleton looping again because of rule success")
    else:
        break

for row in range(9):
    for col in range(9):
        pos = rowcol2pos(row,col)
        print(f"{candidates[pos]}",end=" ")
    print()