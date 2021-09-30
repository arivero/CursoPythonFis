import math
#pragma warning(disable : 4996)
n_ope	= 6		# Numero de operadores en cada lattice 
nhit	= 3		# numero de hits de Metropolis         
maxit	= 1000		# maximo de medidas cada escritura     
#*************************************************************************
				   ##define DEBUG#*escribe en pantalla mas informacion */
EVOL	= #define LINUX
import sys
import math
import time
L	= 8			#Se puede definir en tiempo de compilacion en al makefile
Dim	= 3
L	= 8
L1	= (L-1)
L2	= (L*L)
L3	= (L*L*L)
V	= (L*L*L)	# numero de sites         
Vmed	= (int)((float)V/2.0+0.2)	# mitad del volumen       
nlinks	= V		# numero de links(puntos) 
Norma_cor	= ( (float) (1.0 / (double) (L2*L2)))  */ OJO */
twopi	= 6.283185307
N_OTROS	= 3

precision	= #define N_DATOS_INT 6
N_DATOS_FLOAT	= 3


#ifdef TURBOC
NormRAN	= (1.0/( (float) RAND_MAX+1.0))
NormRANu	= (1.0/math.pow(2.0,32))
#endif

#ifdef SUN4
NormRAN	= ((float) 4.656612595521636e-10)
NormRANu	= ((float) (0.5*4.656612595521636e-10))
#endif
#ifdef LINUX
NormRAN	= ((float) 4.656612595521636e-10)
NormRANu	= ((float) (0.5*4.656612595521636e-10))
#endif

def RAN():	return ( (float) rand() * NormRAN )

# nuevo generador random

Nestm1	= (Nest-1)

Normaener	= ( (float) (1.0/(double) (V*Dim)))
Normamag	= ( (float) (1.0/(double) V))
TWOPI	= 6.283185307


n_obs	= n_ope


LPATH	= 100

struct s_datos
  itmax,		# Numero de medidas por bloque                  
    mesfr,			# frecuencia de las medidas                     
    nbin,			# numero de bloque                              
    itcut,			# proximo bloque a calcular                     
    flag,			# conf de partida: 0(random), 1(fria),2(backup) 
    seed			# semilla random                                
  # acoplamientos           
    Lambda,			# acoplamientos           
    delta			# salto de Metropolis     
