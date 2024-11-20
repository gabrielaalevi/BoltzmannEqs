#this module creates the boltzmann equation for each component

import numpy as np
from scipy.special import kn
import thermal.equilibriumDensities as eqDensitities
from components import Component, CollisionProcess
from typing import List,Dict

def boltz(x: float, Y : List[float], compDict : Dict[int,Component], 
          mDM : float, collisions : List[CollisionProcess]):
    """
    Boltzmann equations for the BSM components. Assumes the energy density is dominated by radiation
    and the SM degrees of freedom.

    :param x: Evolution variable, x = mDM/T
    :param Y: List of yields for each BSM componnent (zero component is the SM)
    :param compDict: Dictionary with PDG as keys and Component objects as values
    :param mDM: Dark Matter mass
    :param collisions: CollisionProcesses object holding all the relevant thermally averaged collision cross-sections
    """

    T = mDM/x
    # The zero component is the SM, so we set dY = 0 and Y = Yeq always
    Y[0] = compDict[0].Yeq(T)
    H = eqDensitities.H(T) #hubble rate at temperature T
    s = eqDensitities.S(T) #entropy density at temperature T
    dsdx = eqDensitities.dSdx(x, mDM) #variation of entropy with x


    # Pre-compute relevant decay terms:
    Dij = np.zeros((len(Y),len(Y)))
    for comp_i in enumerate(compDict.values()):
        if comp_i.ID == 0: # skip SM
            continue
        if comp_i.decays is None:
            continue
        if comp_i.totalwidth <= 0.0:
            continue
        i = comp_i.ID
        Y_i = Y[i]
        Yeq_i = comp_i.Yeq(T)
        gamma_i = (kn(1,comp_i.mass/T)/kn(2,comp_i.mass/T))
        #loop over all the possible decays
        for daughter_pdgs,br in comp_i.decays.items():
            daughters = [compDict[pdg] for pdg in daughter_pdgs]                
            daughter_ids = [daughter.ID for daughter in daughters]
            for j in sorted(np.unique(daughter_ids)):
                Yprod = np.prod([Y[daughter.ID]/daughter.Yeq(T) for daughter in daughters])  
                Dij[i,j] += gamma_i*comp_i.totalwidth*br*(Y_i - Yeq_i*Yprod)/s
            
    # Pre-compute collision factors:
    Yratio = np.ones(len(Y))
    for comp in compDict.values():
        Yratio[comp.ID] = Y[comp.ID]/comp.Yeq(T)
        
    #loop over all components
    dY = np.zeros(Y) #list with all the rhs for all the components, ordered as in the comp_list
    for comp_i in compDict.values():        
        i = comp_i.ID
        if i == 0:
            continue # Skip SM
        Y_i = Y[i]
        Yeq_i = comp_i.Yeq(T)
        ## Decay and inverse decay terms ( i -> j + ...)
        dec_term = -np.sum(Dij[i,:])
        ## Injection and inverse injection terms ( j -> i + ...)
        inj_term = np.sum(Dij[:,i])
        ### Collision term (i + a -> b + c)
        coll_term = 0.0
        for process in collisions:
            i_pdg,j_pdg = process.initialPDGs
            l_pdg, m_pdg = process.finalPDGs            
            if comp_i.PDG not in process.initialPDGs:
                continue
            if j_pdg == comp_i.PDG: # switch order
                j_pdg, i_pdg = i_pdg, j_pdg
            j = compDict[j_pdg].ID
            l = compDict[l_pdg].ID
            m = compDict[m_pdg].ID
            # Set the indices
            coll_term -= process.sigmaV(T)*(Yratio[i]*Yratio[j]-Yratio[l]*Yratio[m])

        dY[i] += (1/(3*H))*dsdx*(dec_term + inj_term + coll_term)

    return dY
