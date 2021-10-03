from configlambda import *
from mainlambda import \
  phi, \
  datos
import mainlambda as mainvars
  #good,cons, #PELIGRO, INMUTABLES pointer #PELIGRO, INMUTABLE
from aleatorio import rng

def Metropolis (j):             #  algoritmo de Metropolis 
  #precision delta_S, prob, r
  #precision Accion_new, Accion_old, modulo
  #precision Staple, uold, unew, variacion

  uold = phi[j]

  Staple = datos.Kappa * (phi[j + neigh[0]] + phi[j + neigh[1]] + phi[j + neigh[2]] + phi[j + neigh[3]] + phi[j + neigh [4]] + phi[j + neigh[5]])

  modulo = uold * uold

  Accion_old = uold * Staple - modulo - datos.Lambda * modulo * modulo

  for ihit in range(nhit):
      #ojo, ig1 ig2 ig3 e ind son indices de array, van mod 256
      #usease unsigned char ig1,ig2...
      
      r = rng()
      variacion = (r - 0.5) * datos.delta

      unew = uold + variacion

      modulo = unew * unew
      Accion_new = unew * Staple - modulo - datos.Lambda * modulo * modulo

      delta_S = Accion_new - Accion_old

      if delta_S < 0.0:
          r = rng()
          prob = exp (delta_S)

          if prob > r:
              uold = unew
              Accion_old = Accion_new
              mainvars.good += 1
      else:
          uold = unew
          Accion_old = Accion_new
          mainvars.good += 1
  phi[j] = uold
