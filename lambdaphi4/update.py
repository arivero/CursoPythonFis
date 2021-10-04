from configlambda import *
from mainlambda import \
  phi, \
  datos
import mainlambda as mainvars
  #good,cons, #PELIGRO, INMUTABLES pointer #PELIGRO, INMUTABLE
from aleatorio import rng
from math import exp
from numba import njit

def Metropolis (j,neigh): 
    r1=rng()#no es facil llamar a rng que no esta compilada
    r2=rng()#esto es perder otro par de segundos
    MetropolisJIT(phi,j,neigh,datos.Kappa,datos.Lambda, datos.delta, mainvars.good,r1,r2)

@njit()
def MetropolisJIT (phi,j,neigh, Kappa, Lambda, delta,good,r1,r2):             #  algoritmo de Metropolis 
  #precision delta_S, prob, r
  #precision Accion_new, Accion_old, modulo
  #precision Staple, uold, unew, variacion

  uold = phi[j]

  Staple = Kappa * (phi[j + neigh[0]] + phi[j + neigh[1]] + phi[j + neigh[2]] 
                    + phi[j + neigh[3]] + phi[j + neigh [4]] + phi[j + neigh[5]])

  modulo = uold * uold

  Accion_old = uold * Staple - modulo - Lambda * modulo * modulo

  for ihit in range(nhit):
      #ojo, ig1 ig2 ig3 e ind son indices de array, van mod 256
      #usease unsigned char ig1,ig2...
      
      r = r1
      variacion = (r - 0.5) * delta

      unew = uold + variacion

      modulo = unew * unew
      Accion_new = unew * Staple - modulo - Lambda * modulo * modulo

      delta_S = Accion_new - Accion_old

      if delta_S < 0.0:
          r = r2
          prob = exp (delta_S)

          if prob > r:
              uold = unew
              Accion_old = Accion_new
              good += 1
      else:
          uold = unew
          Accion_old = Accion_new
          good += 1
  phi[j] = uold
