import io
from configlambda import * 
import os.path
localdir=""
from aleatorio import reseed
import random
import numpy as np
phi=np.empty([V], dtype=np.dtype(float) ) #campo
x_p,y_p,z_p= [[0]*L,[0]*L,[0]*L]
x_m,y_m,z_m= [[0]*L,[0]*L,[0]*L]

cons=0.0; good=0.0 #para update INMUTABLE Ya no se reajustan, pero se inicializan desde fichero :-(
obs=[0.0]*n_obs #para medidas

datos=s_datos() 

v_dat=[[0.0]*maxit]*n_obs #root. Observese que los indices van de fuera adentro
co=[precision()]*L; si=[precision()]*L #inici medidas
name_evol=None #medidas
name_obs = ["E_c", "E2", "E4", "M", "F", "SD"]

if __name__ == '__main__':
    from root import lee_datos, lee_conf, escribe_medidas, escribe_conf, tiempo 
    from inici import table, Direccionamientos, Inicializa
    from update import MetropolisUpdateAll
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
  #vamos a gastar RAM que es gratis. Esto tambien podriamos haberlo hecho en C, claro. Tampoco mejora casi nada.
  neigh= np.zeros([L*L*L,2*Dim],dtype=np.dtype(int))
  site=0
  for z in range(L):
    for y in range(L):
      for x in range(L):
        neigh[site,5] = z_p[z]
        neigh[site,4] = z_m[z]
        neigh[site,3] = y_p[y]
        neigh[site,2] = y_m[y]
        neigh[site,1] = x_p[x]
        neigh[site,0] = x_m[x]
        site += 1

  #termalizacion
  for _ in range(datos.itmax*10):
          MetropolisUpdateAll(neigh,datos.mesfr)

  #arrays para calculo de errores. Deben ser double.
  temp_final=[0.0]*n_obs
  temp_final2=[0.0]*n_obs     

  for ibin in range(datos.itcut, datos.nbin):   #loop en numero de bloques 
      #srand (int(datos.seed))   # queremos reproducir la misma secuencia que cuando se lee de un backup, ¿basta reseed? 
      temp = [0]*n_obs
      temp2 = [0]*n_obs

      good = 0.0

      for it in range(datos.itmax):
          #realizando todo en el update se evita el overhead de traduccion de variables
          MetropolisUpdateAll(neigh,datos.mesfr)

          #esta version no tienes Ajustadelta(cons,good) #aunque aun tenemos la variable good 
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
            temp2[iop] += obs[iop]*obs[iop]
      # Fin for datos.itmax 
      for iop in range(0, n_obs):
        temp_final[iop] += temp[iop]
        temp_final2[iop] += temp2[iop]
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
  for iop in range(0, n_obs):
    temp_final[iop] /= (datos.itmax*datos.nbin)
    temp_final2[iop] /= (datos.itmax*datos.nbin)
  print("Final Results")
  from math import sqrt #bad practice
  for iop in range(0, n_obs):
    err=sqrt(temp_final2[iop]-temp_final[iop]*temp_final[iop])/sqrt(datos.itmax*datos.nbin)
    print("O[%d] = %lf +- %lf" % (iop, temp_final[iop],err) )
  return 1

if __name__ == '__main__':
  main ()
