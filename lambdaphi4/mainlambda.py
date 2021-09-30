from lambdaconfig import * 
dir=['']*[LPATH] #root
irr=[0]*256 #unsigned irr[256] #update
unsigned ind, ig1, ig2, ig3 #update INMUTABLE SOLO SE PONEN A CERO EN INIT
precision phi[V] #inici medidas rrot update
x_p[L],y_p[L],z_p[L]= [[0]*L,[0]*L,[0]*L]
x_m[L],y_m[L],z_m[L]= [[0]*L,[0]*L,[0]*L]

cons=0.0; good=0.0 #update INMUTABLE Ya no se reajustan, pero se inicializan desde fichero :-(
obs=[0.0]*n_obs #medidas

struct s_datos datos #inici medidas root update

v_dat=[[0.0]*n_obs]*maxit #root
precision co[L], si[L] #inici medidas
name_evol[LPATH + 12] #medidas
name_obs[n_ope][256] = { "E_c", "E2", "E4", "M", "F", "SD"

if __name__ == '__main__'
    from root import lee_datos, lee_conf, escribe_medidas, escribe_conf, tiempo 
    from inici import table, Direccionamientos, Inicializa
    from update import Metropolis
    from medida import Medida
    #el bloque "compartido"
def main ()
  unsigned low, high

  Direccionamientos ()
  tiempo ()
  lee_datos (0)
  table ()
  if datos.flag >= 2:
    lee_conf (0)
  cons = float( V *datos.mesfr * datos.itmax * nhit)

  Inicializa (datos.seed, datos.flag)
  srand (int( datos.seed) )
  if EVOL:
    sprintf (name_evol, "%s%s" % (dir, "evol.dat")
    if ((evol = fopen (name_evol, "wt")) == NULL):
      printf ("Error abriendo fichero %s\n" % (name_evol))
      exit (1)
    else:
      fclose (evol)
  for i in range(256):
      low = rand ()
      high = rand ()
      irr[i] = low ^ (high << 16)
  ind = ig1 = ig2 = ig3 = 0

  for ibin in range(datos.itcut, datos.nbin):	#loop en numero de bloques 
      srand ((int) datos.seed)	# asi se reproduce la misma secuencia que cuando se lee de un backup              
      for iop in range(0, n_obs):
	temp[iop] = 0

      good = 0.0

      for it in range(datos.itmax):
	  for j in range(0, datos.mesfr):	#loop de MonteCarlo sin medidas 
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

if __name__ = '__main__':
  main ()
