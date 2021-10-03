#modulo para rng. Ojo, no es thread-safe. Si se quieren threads, hay que usar clases/instancias o proteger la funcion
import random
NormRANu= float(0.5*4.656612595521636e-10)   
seed=0
irr=[0]*256
random.seed(a=int(seed))
for i in range(256):
      irr[i] = random.randrange(2**32)
ind = ig1 = ig2 = ig3 = 0
def rng():
    global ig1,ig2,ig3,ind
    ig1 = (ind - 24) & 255
    ig2 = (ind - 55 ) & 255
    ig3 = (ind - 61) & 255
    irr[ind] = (irr[ig1] + irr[ig2] )& 4294967295 
    ir1 = (irr[ind] ^ irr[ig3])
    ind = (ind+1 )& 255
    return ir1 * NormRANu
import numpy as np
np.seterr(over='ignore')
irrnp=np.empty([256], dtype=np.uintc)
for i in range(256):
      irrnp[i] = random.randrange(2**32)
def rngnp():
    global ig1,ig2,ig3,ind
    ig1 = (ind - 24) & 255
    ig2 = (ind - 55 ) & 255
    ig3 = (ind - 61) & 255
    irrnp[ind] = irrnp[ig1] + irrnp[ig2]
    ir1 = (irrnp[ind] ^ irrnp[ig3])
    ind = (ind+1 )& 255
    return ir1 * NormRANu
ig=np.zeros([4],dtype=np.ubyte)
ig[1] = (ig[0] - 24) 
ig[2] = (ig[0] - 55)
ig[3] = (ig[0] - 61) 
def rngnpB():
    ig[1] = (ig[0] - 24) 
    ig[2] = (ig[0] - 55 )
    ig[3] = (ig[0] - 61) 
    irrnp[ig[0]] = irrnp[ig[1]] + irrnp[ig[2]]
    ir1 = (irrnp[ig[0]] ^ irrnp[ig[3]])
    ig[0] = (ig[0]+1 )
    return ir1 * NormRANu
def rngnpC():
    np.add.at(ig,slice(None),1)
    irrnp[ig[0]] = irrnp[ig[1]] + irrnp[ig[2]]
    ir1 = (irrnp[ig[0]] ^ irrnp[ig[3]])
    return ir1 * NormRANu
def rngnpD():
    np.add.at(ig,slice(None),1)
    irrnp[ig[0]] = np.add(irrnp[ig[1]] , irrnp[ig[2]])
    ir1 = (irrnp[ig[0]] ^ irrnp[ig[3]])
    return ir1 * NormRANu