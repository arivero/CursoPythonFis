from configlambda import *

from mainlambda import \
  x_p,y_p,z_p, \
  x_m,y_m,z_m, \
  phi, \
  co,si, \
  datos

from math import cos, sin
import random

def Direccionamientos():
  for i in range(L):
      x_p[i] = 1
      x_m[i] = -1
      y_p[i] = L  #Lx
      y_m[i] = -L
      z_p[i] = L * L  #Lx * Ly
      z_m[i] = -L * L

  x_m[0] = L - 1
  y_m[0] = (L - 1) * L
  x_p[L - 1] = -x_m[0]
  y_p[L - 1] = -y_m[0]
  z_m[0] = (L - 1) * L * L
  z_p[L - 1] = -z_m[0]


def Inicializa(semilla, flag):
  random.seed(a=semilla)   #semilla a partir del sistema
  if flag < 2:
      for igen in range(0, V):
        if flag == 0:
          phi[igen] = RAN () * datos.delta * 4.
        else:
          phi[igen] = 1.0

def table():
  for i in range(L):
      co[i] = cos (TWOPI *  i /  L)
      si[i] = sin (TWOPI *  i /  L)
