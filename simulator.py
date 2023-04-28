import random

def genTraceStrict(depth):
    # incremental features traces, but onyl partially ordered: sign->(red/circ)->stop
    sign = [0 for x in range(depth)]
    red = [0 for x in range(depth)]
    circ = [0 for x in range(depth)]
    stop = [0 for x in range(depth)]
    i=random.randint(0,depth-5)
    for x in range(i,depth-1) : sign[x] = 1
    if random.randint(0,1): 
        for x in range(i+1,depth) : circ[x] = 1 
        for x in range(i+2,depth) : red[x] = 1 
    else : 
        for x in range(i+1,depth) : red[x] = 1 
        for x in range(i+2,depth) : circ[x] = 1 
    for x in range(i+3,depth): stop[x] = 1
    return sign, red, circ, stop  # change into sign col shape actual

def genTraceDepth(depth):
    # incremental features traces, but onyl partially ordered: sign->(red/circ)->stop
    sign = [0 for x in range(depth)]
    red = [0 for x in range(depth)]
    circ = [0 for x in range(depth)]
    stop = [0 for x in range(depth)]
    i=random.randint(0,depth-5)
    for x in range(i,depth) : sign[x] = 1 
    i=random.randint(i,depth)
    for x in range(i,depth) : circ[x] = 1 
    for x in range(i,depth) : red[x] = 1 
    i=random.randint(i,depth)
    for x in range(i,depth): stop[x] = 1
    return sign, red, circ, stop  # change into sign col shape actual

def genTrace(pdf):
    depth = len(pdf)  # this is also the number of time steps of the traces
    rnd = random.randint(0, 99)
    sign = [1 if rnd < pdf[d] else 0 for d in range(depth)]  #
    red = [0 for x in range(depth)]
    circ = [0 for x in range(depth)]
    stop = [0 for x in range(depth)]
    for d in range(1, depth):
        if red[d-1] == 1:
            red[d] = 1
        elif sign[d-1] == 1:
            red[d] = random.randint(0, 1)
    for d in range(1, depth):
        if circ[d-1] == 1:
            circ[d] = 1
        elif sign[d-1] == 1:
            circ[d] = random.randint(0, 1)
    for d in range(2, depth):
        if stop[d-1] == 1:
            stop[d] = 1
        elif sign[d-1] == 1 and (red[d-1] == 1 or circ[d-1] == 1):
            stop[d] = random.randint(0, 1)
        # is it rigth to subordinate actual stop detection only AFTER other features?
        # only if it is modeling the actual stop sight seeing and not just a specific feature of the
    # always have the whole sign visible at least, in these tests traces
    sign[depth-1] = 1
    red[depth-1] = 1
    circ[depth-1] = 1
    stop[depth-1] = 1
    return sign, red, circ, stop  # change into sign col shape actual


def printTrace(sT, rT, cT, ssT):
    print('sign: ', sT)
    print(' red: ', rT)
    print('circ: ', cT)
    print('stop: ', ssT)
    print()

def printState(states):
    print('loc     :', states['loc'])
    print('signDet :', states['signDet'])
    print('stopping:', states['stopping'])
    print('redSign :', states['redSign'])
    print()

# Simulation
def simulatePdf(ctrl, pdf, n):
    depth = len(pdf)  # this is also the number of time steps of the traces
    stop_at = [0 for i in range(depth-1)] #use pdf len -1 to avoid counting final pos
    for i in range(n):
    # Run a simulation
        # Pick an environmental signal
        sT, rT, cT, ssT = genTrace(pdf)
        #printTrace(sT, rT, cT, ssT)
        # Run controller on env
        time, states = ctrl.run('Sinit', {'sign': sT, 'red': rT, 'circle': cT,  'stopSign': ssT})
        #printState(states)
        loc=0; 
        for i in range(depth) : 
            if states['signDet'][depth-1-i] == True : loc=i 
        #print(loc, states['signDet']) 
        stop_at[loc]+=1 
    
    assert sum(stop_at) == n
    #print(stop_at)
    return stop_at  #produce reversed with respect to states[]: stop_at[0] is last state, and starting state is avoided (alwais false)

def simulateSeq(ctrl, depth, n):
    #depth = len(pdf)  # this is also the number of time steps of the traces
    stop_at = [0 for i in range(depth-1)] #pass pdf len -1 to avoid counting final pos
    for i in range(n):
    # Run a simulation
        # Pick an environmental signal
        sT, rT, cT, ssT = genTraceStrict(depth)
        #printTrace(sT, rT, cT, ssT)
        # Run controller on env
        time, states = ctrl.run('Sinit', {'sign': sT, 'red': rT, 'circle': cT,  'stopSign': ssT})
        #printState(states)
        loc=0; 
        for i in range(depth) : 
            if states['signDet'][depth-1-i] == True : loc=i 
        #print(loc, states['signDet']) 
        stop_at[loc]+=1 
    
    assert sum(stop_at) == n
    #print(stop_at)
    return stop_at  #produce reversed with respect to states[]: stop_at[0] is last state, and starting state is avoided (alwais false)

def simulateStrict(ctrl, depth, n):
    #depth = len(pdf)  # this is also the number of time steps of the traces
    stop_at = [0 for i in range(depth)] #pass pdf len -1 to avoid counting final pos
    for i in range(n):
    # Run a simulation
        # Pick an environmental signal
        sT, rT, cT, ssT = genTraceDepth(depth)
        #printTrace(sT, rT, cT, ssT)
        # Run controller on env
        time, states = ctrl.run('Sinit', {'sign': sT, 'red': rT, 'circle': cT,  'stopSign': ssT})
        #printState(states)
        loc=0; 
        for i in range(depth) : 
            if states['signDet'][depth-1-i] == True : loc=i 
        #print(loc, states['signDet']) 
        stop_at[loc]+=1 
    
    assert sum(stop_at) == n
    #print(stop_at)
    return stop_at  #produce reversed with respect to states[]: stop_at[0] is last state, and starting state is avoided (alwais false)


def testTraces(n): 
    for x in range(10): 
    #sT, rT, cT, ssT = genTrace([80,80,80,80,80,80])
    #sT, rT, cT, ssT = genTraceDepth(6)
        sT, rT, cT, ssT = genTraceStrict(6)
        printTrace(sT, rT, cT, ssT)



