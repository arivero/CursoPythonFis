from configlambda import *
from mainlambda import \
  phi, \
  datos
import mainlambda as mainvars
  #good,cons, #PELIGRO, INMUTABLES pointer #PELIGRO, INMUTABLE
import aleatorio as alea
from math import exp
from numba import njit


#punto de entrada al compilador, tiene que pasar todo lo que no sean constantes o tipos que no reconozca
def MetropolisUpdateAll(neigh,n=1):
  compiledUpdateAll(neigh,n,phi,datos.Kappa,datos.Lambda, datos.delta, mainvars.good, alea.irr)

@njit
def compiledUpdateAll(neigh,n,phi, Kappa, Lambda, delta,good, irr  ):
  for _ in range(n):
    for site in range(L*L*L):
      MetropolisJIT(phi,site,neigh[site],Kappa,Lambda, delta, good, irr)

@njit()
def MetropolisJIT (phi,j,neigh, Kappa, Lambda, delta,good, irr):             #  algoritmo de Metropolis 
  #precision delta_S, prob, r
  #precision Accion_new, Accion_old, modulo
  #precision Staple, uold, unew, variacion
  #return #6-7 segundos hasta aqui, 7-8 segundos hasta el final: el peso esta en el overhead de la llamada
  uold = phi[j]

  Staple = Kappa * (phi[j + neigh[0]] + phi[j + neigh[1]] + phi[j + neigh[2]] 
                    + phi[j + neigh[3]] + phi[j + neigh [4]] + phi[j + neigh[5]])

  modulo = uold  * uold

  Accion_old = uold * Staple - modulo - Lambda * modulo * modulo

  for ihit in range(nhit):
      #ojo, ig1 ig2 ig3 e ind son indices de array, van mod 256
      #usease unsigned char ig1,ig2...
      r = alea.rngjit(irr)
      variacion = (r - 0.5) * delta

      unew = uold + variacion

      modulo = unew * unew
      Accion_new = unew * Staple - modulo - Lambda * modulo * modulo

      delta_S = Accion_new - Accion_old

      if delta_S < 0.0:
          r = alea.rngjit(irr)
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
