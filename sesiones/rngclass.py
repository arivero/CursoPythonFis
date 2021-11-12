import random
import numpy as np
np.seterr(over='ignore')
NormRANu= float(0.5*4.656612595521636e-10)   


class aleatorio:
    def __init__(self, seed=0):
        random.seed(a=int(seed))
        self.irr=[random.randrange(2**32) for _ in range(256)]
        self.irrnp=np.array(self.irr)
        self.ind = 0
        self.ig1 = 0
        self.ig2 = 0
        self.ig3 = 0
    def rng(self):
        self.ig1 = (self.ind - 24) & 255
        self.ig2 = (self.ind - 55 ) & 255
        self.ig3 = (self.ind - 61) & 255
        self.irr[self.ind] = (self.irr[self.ig1] + self.irr[self.ig2] )& 4294967295 
        ir1 = (self.irr[self.ind] ^ self.irr[self.ig3])
        self.ind = (self.ind+1 )& 255
        return ir1 * NormRANu

"""como todas las clases basadas en numpy, incluida la compilada,
   usan la misma inicializacion, la definimos en una clase 'ancestro'
   y aplicamos herencia
"""

class _aleatorioBase:
    def __init__(self, seed=0):
        random.seed(a=int(seed))
        irr=[random.randrange(2**32) for _ in range(256)]
        self.irrnp=np.array(irr, dtype=np.uintc)
        self.ig=np.array([0,-24,-55,-61],dtype=np.ubyte)
        self.i = 0
        #print(self.ig)

class aleatorioNumpy(_aleatorioBase):
    def rng(self):
        ig=self.ig
        irrnp=self.irrnp
        ig[1] = (ig[0] - 24) 
        ig[2] = (ig[0] - 55 )
        ig[3] = (ig[0] - 61) 
        irrnp[ig[0]] = irrnp[ig[1]] + irrnp[ig[2]]
        ir1 = (irrnp[ig[0]] ^ irrnp[ig[3]])
        ig[0] = (ig[0]+1 )
        return ir1 * NormRANu

#la clase aleatorioNumba compila una funcion que no va asociada
#a la instancia, dado que recibe todo como parametros. Podriamos
#haberla construido como un "metodo de clase", pero eso podria
#complicar la vida con algunas versiones del compilador

from numba import njit
@njit()
def _rngJit(ig,irrnp):
        ig[1] = (ig[0] - 24) 
        ig[2] = (ig[0] - 55 )
        ig[3] = (ig[0] - 61) 
        irrnp[ig[0]] = irrnp[ig[1]] + irrnp[ig[2]]
        ir1 = (irrnp[ig[0]] ^ irrnp[ig[3]])
        #ig[:]= ig + np.array([1,1,1,1],dtype=np.ubyte) # es mas lento
        ig[0] = (ig[0]+1 )
        return ir1 * NormRANu


class aleatorioNumba(_aleatorioBase):
    def rng(self):
        r=_rngJit(self.ig,self.irrnp)
        return r

#
#
#


class aleatorioBloque(_aleatorioBase):
    #ig3=[ (i-61) & 255 for i in range(256)]
    #def ronda(self):
    #    self.irrnp[:24]=self.irrnp[256-24:] + self.irrnp[256-55:][:24]
    #    ir1=  self.irrnp[:24] ^ self.irrnp[aleatorioBloque.ig3][:24]
    #    self.irrnp=np.roll(self.irrnp,-24)
    #    return ir1*NormRANu

    def _ronda(self):
        bloque=self.irrnp[232:] + self.irrnp[201:225]
        ir1 = bloque ^ self.irrnp[195:219]
        self.irrnp=np.concatenate( (self.irrnp[24:],bloque) )
        return ir1*NormRANu

    def rng(self):
        if self.i  == 0:
            self.ir= self._ronda()
        r = self.ir[self.i]
        self.i = (self.i + 1) % 24 
        return r
 

class aleav2():
    def __init__(self, seed=0):
        random.seed(a=int(seed))
        self.irr=[random.randrange(2**32) for _ in range(256)]
        self.generator = self._generator()
  
    def _generator(self):
        irrnp=np.array(self.irr,dtype=np.uintc)
        while True:
            bloque=irrnp[232:] + irrnp[201:225]
            ir1 = bloque ^ irrnp[195:219]
            irrnp=np.concatenate( (irrnp[24:],bloque) )
            for r in ir1 * NormRANu:
                yield r

    def rng(self):
        return next(self.generator)

class aleav2plain():
    def __init__(self, seed=0):
        random.seed(a=int(seed))
        self.irr=[random.randrange(2**32) for _ in range(256)]
        self.generator = self._generator()
  
    def _generator(self):
        irr=self.irr
        while True:
            bloque=[ (a+b) & 4294967295  for a,b in zip(irr[232:] , irr[201:225])]
            ir1 = [ a ^ b for a, b in zip(bloque,irr[195:219])]
            irr=irr[24:]+bloque
            for r in ir1:
                yield r * NormRANu

    def rng(self):
        return next(self.generator)

@njit()
def _rngJit2(irrnp):
    bloque=irrnp[232:] + irrnp[201:225]
    ir1 = bloque ^ irrnp[195:219]
    irrnp[:]=np.concatenate( (irrnp[24:],bloque) )
    return ir1 * NormRANu


class aleav2Numba():
    def __init__(self, seed=0):
        random.seed(a=int(seed))
        self.irr=[random.randrange(2**32) for _ in range(256)]
        self.generator = self._generator()
  
    def _generator(self):
        irrnp=np.array(self.irr,dtype=np.uintc)
        while True:
            ir1=_rngJit2(irrnp)
            for r in ir1:
                yield r

    def rng(self):
        return next(self.generator)

@njit() #sin compilar 33 microsecs, compilando 323 nanosecs: un factor 100
def _rngJit3(ig,irrnp,ir1):
    for i in range(len(ir1)):
        irrnp[ig[0]] = irrnp[ig[1]] + irrnp[ig[2]]
        ir1[i] = (irrnp[ig[0]] ^ irrnp[ig[3]])
        for x in range(4):
            ig[x]+=1
        #ig[:]= ig + np.array([1,1,1,1],dtype=np.ubyte) # es mas lento
    return ir1 * NormRANu

class aleav2NumbaIdx():
    def __init__(self, seed=0, prefetch=2048):
        random.seed(a=int(seed))
        self.irr=[random.randrange(2**32) for _ in range(256)]
        self.generator = self._generator()
        self.prefetch=prefetch
  
    def _generator(self):
        irrnp=np.array(self.irr,dtype=np.uintc)
        ig = np.array([0,-24,-55,-61],dtype=np.ubyte)
        prefetch=np.ndarray(self.prefetch, dtype=np.uintc)
        while True:
            for x in _rngJit3(ig, irrnp, prefetch):
                yield x

    def rng(self):
        return next(self.generator)