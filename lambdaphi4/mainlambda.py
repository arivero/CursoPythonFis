from configlambda import * 
dir=['']*LPATH #root
from aleatorio import reseed

phi=[precision()]*V #inici medidas rrot update
x_p,y_p,z_p= [[0]*L,[0]*L,[0]*L]
x_m,y_m,z_m= [[0]*L,[0]*L,[0]*L]

cons=0.0; good=0.0 #update INMUTABLE Ya no se reajustan, pero se inicializan desde fichero :-(
obs=[0.0]*n_obs #medidas

datos=s_datos()  #inici medidas root update

v_dat=[[0.0]*n_obs]*maxit #root
co=[precision()]*L; si=[precision()]*L #inici medidas
name_evol=['']*(LPATH + 12) #medidas
#name_obs[n_ope][256] = { "E_c", "E2", "E4", "M", "F", "SD"

if __name__ == '__main__':
    from root import lee_datos, lee_conf, escribe_medidas, tiempo #falta escribe_conf
    from inici import table, Direccionamientos, Inicializa
    from update import Metropolis
    from medidas import Medida
    from mainlambda import *
    #el bloque "compartido"
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
    sprintf (name_evol, "%s%s" % (dir, "evol.dat"))
    try:
      evol = fopen (name_evol, "wt")
      fclose(evol)
    except:
      printf ("Error abriendo fichero %s\n" % (name_evol))
      exit (1)

  for ibin in range(datos.itcut, datos.nbin):   #loop en numero de bloques 
      #srand (int(datos.seed))   # queremos reproducir la misma secuencia que cuando se lee de un backup, ¿basta reseed?             
      for iop in range(0, n_obs):
         temp[iop] = 0

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
                          Metropolis (site)
                          site += 1
          # Fin for datos.mesfr 

          #Ajustadelta(cons,good) 
          Medida ()

          for iop in range(0, n_obs):
            v_dat[iop][it] = obs[iop]

          for iop in range(0, n_obs):
            temp[iop] += obs[iop]
      # Fin for datos.itmax 

      for iop in range(0, n_obs):
        temp[iop] /= datos.itmax

      tiempo ()
      printf ("A=%4.2f " % (good / cons))
      printf ("i=%d " % (ibin))
      for x in range(0, n_ope):
        printf ("%s=%+5.3f " % (name_obs[x], temp[x]))
      printf ("\n")

      escribe_medidas (ibin, 0)

      datos.seed = rand () 
      #datos.delta=delta 
      datos.itcut = ibin + 1
      escribe_conf (0)
  # Fin for datos.nbin 
  return 1

if __name__ == '__main__':
  main ()
