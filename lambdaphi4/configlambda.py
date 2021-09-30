#pragma warning(disable : 4996)
n_ope   = 6             # Numero de operadores en cada lattice 
nhit    = 3             # numero de hits de Metropolis         
maxit   = 1000          # maximo de medidas cada escritura     
#*************************************************************************
DEBUG= False #*escribe en pantalla mas informacion */
EVOL=True
LINUX=True

L       = 8     #makefile? como lo pondriamos?
Dim     = 3
L       = 8
L1      = (L-1)
L2      = (L*L)
L3      = (L*L*L)
V       = (L*L*L)       # numero de sites         
Vmed    = int(V/2.0+0.2)       # mitad del volumen       
nlinks  = V             # numero de link(puntos) 
Norma_cor  =  float (1.0 /  (L2*L2)) #OJO 
twopi   = 6.283185307
N_OTROS = 3

precision       = float
N_DATOS_INT = 6
N_DATOS_FLOAT   = 3


NormRAN = float(4.656612595521636e-10)
NormRANu= float(0.5*4.656612595521636e-10)

def RAN():
    return float (rand() * NormRAN )

Normaener       = float(1.0/ (V*Dim))
Normamag        =  float(1.0/ V)
TWOPI   = 6.283185307


n_obs   = n_ope


LPATH   = 100

class s_datos:
  itmax=0       # Numero de medidas por bloque                  
  mesfr=0       # frecuencia de las medidas                     
  nbin=0        # numero de bloque                              
  itcut=0       # proximo bloque a calcular                     
  flag=0        # conf de partida: 0(random), 1(fria),2(backup) 
  seed=0        # semilla random                                
  Kappa= 0.0 # acoplamientos           
  Lambda=0.0    # acoplamientos           
  delta=0.0     # salto de Metropolis     
