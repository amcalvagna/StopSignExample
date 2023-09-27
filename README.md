# StopSignExample
## Code for a simple car model approaching a stop sign encoded in Tulip. Requires Tulip 1.4.0 installed and a Python 3.10 environment to be run
### demo.py is the code for a Tulip based encoding of a simple discrete car model moving inside an unknown environment, and synthesizing three controller versions, for comparison: 1)base, 2)with incremental perception, 3)with knowledge awareness. these in turn are then used by the simulation code to compare their performances.
### simulator.py is a set of support functions used to simulate operation of the synthesized controller into three different types of (emulated) environment behaviours. 
