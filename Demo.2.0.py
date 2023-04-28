

# Import TuLiP and other Python packages
from tulip import transys, spec, synth
import random
import simulator as sim
# Create a finite transition system
sys = transys.FTS()
# Define the states of the system.
# round trip from POS 0 to 0 with backward count, stop sign is at 0 (sys doesn't know! it, env tells it)
# 0 is the position of the sign
sys.states.add_from(['M0', 'M1', 'M2', 'M3', 'M4',
                    'S0', 'S1', 'S2', 'S3', 'S4'])
# Define the allowable transitions
sys.sys_actions.add_from(['go', 'hard_stop', 'slow_down'])

# Add atomic propositions to the states
# sys.atomic_propositions.add_from(['start', 'moving', 'stopping']) #,'stop_in_4','stop_in_3','stop_in_2','stop_in_1' ])
# ,'stop_in_4','stop_in_3','stop_in_2','stop_in_1' ])
sys.atomic_propositions.add_from(['moving', 'stopping'])
# 'stopping' is the atomic prop representing the stop sign detection event, even before an actual stopSign is visible
# no sign detected state chain
sys.transitions.add('M4', 'M3', sys_actions='go')
sys.transitions.add('M3', 'M2', sys_actions='go')
sys.transitions.add('M2', 'M1', sys_actions='go')
sys.transitions.add('M1', 'M0', sys_actions='go')
sys.transitions.add('M0', 'M4', sys_actions='go')
# sign detected state chain
sys.transitions.add('S4', 'S3', sys_actions='slow_down')
sys.transitions.add('S3', 'S2', sys_actions='slow_down')
sys.transitions.add('S2', 'S1', sys_actions='slow_down')
sys.transitions.add('S1', 'S0', sys_actions='slow_down')
sys.transitions.add('S0', 'S4', sys_actions='slow_down')

# from no sing to sign detected
sys.transitions.add('M4', 'S3', sys_actions='slow_down')
sys.transitions.add('M3', 'S2', sys_actions='slow_down')
sys.transitions.add('M2', 'S1', sys_actions='slow_down')
sys.transitions.add('M1', 'S0', sys_actions='hard_stop')
sys.transitions.add('M0', 'S4', sys_actions='slow_down')

# to allow fairness cond: allow all reverse paths
# from sing to no sign detected
sys.transitions.add('S4', 'M3', sys_actions='go')
sys.transitions.add('S3', 'M2', sys_actions='go')
sys.transitions.add('S2', 'M1', sys_actions='go')
sys.transitions.add('S1', 'M0', sys_actions='go')
sys.transitions.add('S0', 'M4', sys_actions='go')

# add labels
sys.states.add_from(['M0', 'M1', 'M2', 'M3', 'M4'], ap={'moving'})
sys.states.add_from(['S0', 'S1', 'S2', 'S3', 'S4'], ap={'stopping'})

# define allowed start states
sys.states.initial.add_from({'M0', 'S0'})  # can start with or without sign
# Generate a picture of the system
# print(sys)

# metto sign come env action e la tolgo dalle env vars
# oppure riduco fts ad un gridworld circolare di movimento e metto le ap come sys vars

# isolated features, reduced to one single stop sign example
# features = {'no', 'sign', 'red','circle', 'stopSign'}
env_vars = {'sign', 'red', 'circle', 'stopSign'}  # stopSign is StopD for now
env_init = {}  # empty set: values set from the simulation run
env_prog = {}           # it is ASSUMED that !sign is possible, in GR(1)
env_safe = {            # assumptions
    # incrementality, partial
    # '!sign -> X !stopping', #fix bad transition system
    'stopSign -> circle | red',
    '(circle | red) -> sign',
    '!sign -> !(red | circle | stopSign)',
}
# redSign to simulate walking down the perception tree, signDet models sign detection, by rule, even when not seeing the stopSign yet
sys_vars = {'Sign', 'redSign', 'signDet'}
# start without knowledge of sign (!signDet), and the sim traces always end in S0 (because of their fixed length)
sys_init = {'loc="M0"'}
sys_prog = {}  # {'!moving'}  #have to complete the to support fairness conditions   # []<>at_sign & X moving

#####################
# BASE CNTRL 
sys_safe_base = {
    'signDet <-> X stopping', #required by all
   # base case: try to stop when you see the whole actual sign
    'stopSign <-> signDet', #detection is immediate
}    

sys_safe_tree = {
    'signDet <-> X stopping', #required by all
    # perception tree enhancement: change to red circle to col and shape for generality4
    'sign <-> X Sign',
    'Sign & red <-> signDet', 
    'signDet & circle -> signDet ',
    #'sign & red -> X stopping', #early action
}

sys_safe_onto = {
    'signDet <-> X stopping',
    # ontology derived knowledge based enhancement
    'sign & red & circle -> signDet', 
    #early action   
    '(sign & red)|(sign & circle)|(circle & red) <-> signDet',
}

specs_base = spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                    env_safe, sys_safe_base, env_prog, sys_prog)
# print(specs.pretty())
specs_tree = spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                    env_safe, sys_safe_tree, env_prog, sys_prog)
specs_onto = spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                    env_safe, sys_safe_onto, env_prog, sys_prog)

# BASE CONTROLLER
specs_base.qinit = '\A \E'
specs_base.moore = False
ctrl_base = synth.synthesize(specs_base, sys=sys)
assert ctrl_base is not None, 'base unrealizable'

# PERCEPTION TREE CONTROLLER
specs_tree.qinit = '\A \E'
specs_tree.moore = False
ctrl_tree = synth.synthesize(specs_tree, sys=sys)
assert ctrl_tree is not None, 'tree unrealizable'

# ONTOLOGY BASED CONTROLLER
specs_onto.qinit = '\A \E'
specs_onto.moore = False
ctrl_onto = synth.synthesize(specs_onto, sys=sys)
assert ctrl_onto is not None, 'onto unrealizable'

ctrl=[ctrl_base, ctrl_tree, ctrl_onto]
# Description of the synthesized controller
# ctrl.plot()
#print(ctrl)

## simulation parameters
pdf = [85, 85, 85, 85, 85, 99]
depth = len(pdf)
# Invoke simulation
print('pdf :', pdf)
for c in ctrl : print(sim.simulatePdf(c, pdf, 10000))
#print('simple seq :')    
#for c in ctrl : print(sim.simulateSeq(c, depth, 10000))
print('strict seq :')    
for c in ctrl : print(sim.simulateStrict(c, depth, 10000))
