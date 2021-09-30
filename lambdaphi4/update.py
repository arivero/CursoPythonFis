from configlambda import *
from mainlambda import \
  irr,
  ir1,  ### PELIGROSO, INMUTABLE,
  ind,ig1,ig2,ig3, ### PELIGRO, INMUTABLES
  phi,
  good,cons, #PELIGRO, INMUTABLES
  datos,
  pointer #PELIGRO, INMUTABLE


def Metropolis (j):             #  algoritmo de Metropolis 
  #precision delta_S, prob, r
  #precision Accion_new, Accion_old, modulo
  #precision Staple, uold, unew, variacion

  uold = phi[j]

  Staple = datos.Kappa * (phi[j + neigh[0]] + phi[j + neigh[1]] +
                          phi[j + neigh[2]] + phi[j + neigh[3]] + phi[j + neigh [4]] + phi[j + neigh[5]])

  modulo = uold * uold

  Accion_old = uold * Staple - modulo - datos.Lambda * modulo * modulo

  for ihit in range(nhit):
      ig1 = ind - 24
      ig2 = ind - 55
      ig3 = ind - 61
      irr[ind] = irr[ig1] + irr[ig2]
      ir1 = (irr[ind] ^ irr[ig3])
      ind += 1
      r = ir1 * NormRANu
      variacion = (r - 0.5) * datos.delta

      unew = uold + variacion

      modulo = unew * unew
      Accion_new = unew * Staple - modulo - datos.Lambda * modulo * modulo

      delta_S = Accion_new - Accion_old

      if delta_S < 0.0:
          ig1 = ind - 24
          ig2 = ind - 55
          ig3 = ind - 61
          irr[ind] = irr[ig1] + irr[ig2]
          ir1 = (irr[ind] ^ irr[ig3])
          ind += 1
          r = ir1 * NormRANu

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
