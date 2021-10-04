from configlambda import * 
import os.path
localdir=""
from aleatorio import reseed
import random
import numpy as np
phi=np.empty([V], dtype=np.dtype(float) ) #inici medidas rrot update
x_p,y_p,z_p= [[0]*L,[0]*L,[0]*L]
x_m,y_m,z_m= [[0]*L,[0]*L,[0]*L]

cons=0.0; good=0.0 #update INMUTABLE Ya no se reajustan, pero se inicializan desde fichero :-(
obs=[0.0]*n_obs #medidas

datos=s_datos()  #inici medidas root update

v_dat=[[0.0]*maxit]*n_obs #root. Observese que los indices van de fuera adentro
co=[precision()]*L; si=[precision()]*L #inici medidas
name_evol=None #medidas
name_obs = ["E_c", "E2", "E4", "M", "F", "SD"]

if __name__ == '__main__':
    from root import lee_datos, lee_conf, escribe_medidas, escribe_conf, tiempo 
    from inici import table, Direccionamientos, Inicializa
    from update import Metropolis
    from medidas import Medida
    #el bloque compartido no es lo mismo que el bloque __main__
    import mainlambda
    from mainlambda import *
def main ():
  #unsigned low, high

  Direccionamientos ()
  tiempo ()
  lee_datos (0)
  table ()
  if datos.flag >= 2:
    lee_conf (0)
  cons = float( V *datos.mesfr * datos.itmax * nhit)

  Inicializa (datos.seed, datos.flag) #phi
  reseed (int( datos.seed) ) #
  if EVOL:
    name_evol = os.path.join(mainlambda.localdir, "evol.dat")
    try:
      evol = open (name_evol, "wt")
      evol.close()
    except Exception as instance:
      print(instance)
      print ("Error abriendo fichero %s" % (name_evol))
      exit (1)
  else:
    name_evol= None
    

  for ibin in range(datos.itcut, datos.nbin):   #loop en numero de bloques 
      #srand (int(datos.seed))   # queremos reproducir la misma secuencia que cuando se lee de un backup, ¿basta reseed? 
      temp = [0]*n_obs
      neigh= np.zeros([2*Dim],dtype=np.dtype(int))

      good = 0.0

      for it in range(datos.itmax):
          for j in range(0, datos.mesfr):       #loop de MonteCarlo sin medidas 
              site = 0
              for z in range(L):
                  neigh[5] = z_p[z]
                  neigh[4] = z_m[z]
                  for y in range(L):
                      neigh[3] = y_p[y]
                      neigh[2] = y_m[y]
                      for x in range(L):
                          neigh[1] = x_p[x]
                          neigh[0] = x_m[x]
                          Metropolis (site,neigh)
                          site += 1
          # Fin for datos.mesfr 

          #Ajustadelta(cons,good) 
          Medida ()
          #este append quizas no sea necesario tras cada medida. 
          #necesitamos una decisicion 
          if name_evol:
            with open (name_evol, "at") as ev:
                for x in range(0, n_ope):
                   ev.write( "%lf " % (obs[x]))
                ev.write("\n")
            #fclose (ev)
          for iop in range(0, n_obs):
            v_dat[iop][it] = obs[iop]

          for iop in range(0, n_obs):
            temp[iop] += obs[iop]
      # Fin for datos.itmax 

      for iop in range(0, n_obs):
        temp[iop] /= datos.itmax

      tiempo ()
      print ("A=%4.2f " % (good / cons), end='')
      print ("i=%d " % (ibin), end='')
      for x in range(0, n_ope):
        print ("%s=%+5.3f " % (name_obs[x], temp[x]), end='')
      print ()

      if IO:
            escribe_medidas (ibin, 0)

      datos.seed = random.randrange(2**32) 
      #datos.delta=delta 
      datos.itcut = ibin + 1
      if IO:
          escribe_conf (0)
  # Fin for datos.nbin 
  return 1

if __name__ == '__main__':
  main ()
