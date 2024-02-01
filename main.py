#!/usr/bin/env python3

from boltzmannEq import boltz
from components import Component
import auxFunc
from modelParameters import particlesDict, T0, Tlist
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import logging as logger


   

def main(partDict,verbose):

    comp_list = []
    for label,pDict in partDict.items():
        comp = Component.from_dict(label,pDict)
        comp_list.append(comp)

    y0 = [comp.equilibrium_yield(T0) for comp in comp_list]

    dmList = [comp for comp in comp_list if comp.decay_width == 0.0]
    if len(dm) != 1:
        logger.error('A unique DM component must be defined')
        raise ValueError()
    dm = dm[0]


    x = dm.mass/Tlist

    sol = odeint(boltz, y0, x, args=(comp_list,),
                 atol = 10**(-16), rtol = 10**(-14))
    


    sol_dm = []
    sol_mediator = []

    for i in range(0, len(Tlist)):
        sol_dm.append(sol[i][0])
        sol_mediator.append(sol[i][1])

    return x,sol

if __name__ == "__main__":

    import argparse    
    ap = argparse.ArgumentParser( description=
            "Solve Boltzmann equations." )
    ap.add_argument('-p', '--parfile', default='parameters.ini',
            help='path to the parameters file [parameters.ini].')
    ap.add_argument('-v', '--verbose', default='info',
            help='verbose level (debug, info, warning or error). Default is info')


    args = ap.parse_args()
    output = main(args.parfile,args.verbose)
