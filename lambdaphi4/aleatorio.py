import random
import numpy as np
from numba import njit,jit
import aleatorio
NormRANu= float(0.5*4.656612595521636e-10)   
Seed=0
np.seterr(over='ignore')
irr=np.empty([257], dtype=np.uintc)
def reseed(seed):
    #global irr curiosamente no hace falta
    random.seed(a=int(seed))
    for i in range(256):
      irr[i] = random.randrange(2**32)
    irr[256]=7
reseed(Seed)
def rng():
    global irr
    return rngjit(irr)
@njit
def rngjit(irr):
    ind=irr[256]
    ig1 = (ind - 24) & 255
    ig2 = (ind - 55 ) & 255
    ig3 = (ind - 61) & 255
    irr[ind] = (irr[ig1] + irr[ig2] )#& 4294967295 
    ir1 = (irr[ind] ^ irr[ig3])
    irr[256] = (ind+1 )& 255
    return ir1 * NormRANu
