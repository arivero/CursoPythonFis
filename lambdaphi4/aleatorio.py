import random
import numpy as np
from numba import njit,jit
NormRANu= float(0.5*4.656612595521636e-10)   
Seed=0
np.seterr(over='ignore')
irr=np.empty([256], dtype=np.uintc)
ind = ig1 = ig2 = ig3 = 0
def reseed(seed):
    global ig1,ig2,ig3,ind
    random.seed(a=int(seed))
    for i in range(256):
      irr[i] = random.randrange(2**32)
    ind = ig1 = ig2 = ig3 = 0
reseed(Seed)

def rng():
    global ig1,ig2,ig3,ind
    return rngjit(ig1,ig2,ig3,ind,irr)
#compilar asi tan solo nos baja de 28-29 a 23-24 segundos el bloque
@njit
def rngjit(ig1,ig2,ig3,ind,irr):
    ig1 = (ind - 24) & 255
    ig2 = (ind - 55 ) & 255
    ig3 = (ind - 61) & 255
    irr[ind] = (irr[ig1] + irr[ig2] )#& 4294967295 
    ir1 = (irr[ind] ^ irr[ig3])
    ind = (ind+1 )& 255
    return ir1 * NormRANu
