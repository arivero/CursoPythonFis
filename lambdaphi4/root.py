from configlambda import *
from mainlambda import dir, phi, v_dat, datos

#en C: otros_datos[N_OTROS+1]={N_OTROS,L,L,L}
otros_datos = [N_OTROS, L,L,L]

from time import time
time1 = time()
def tiempo ():
  global time1
  time2 = time ()
  if time1 > 0:
    print ("%4ds:" % (time2 - time1))
  time1 = time2

def pinta_datos (dat):  # solo para debug 
  print ("itmax  %ld " % (dat.itmax), end='')
  print ("mesfr  %ld " % (dat.mesfr))
  print ("nbin   %ld " % (dat.nbin))
  print ("itcut  %ld " % (dat.itcut))
  print ("flag   %ld " % (dat.flag))
  print ("seed   %ld " % (dat.seed))
  print ("Kappa %f " % (dat.Kappa))
  print ("Lambda %f " % (dat.Lambda))
  print ("delta  %f " % (dat.delta))


def lee_datos(i):
  name= "%s.%i" % ("input", i)
  dummy="".join(['']*LPATH) #????
  Finput = fopen (name, "rt")

  if Finput == None:
      Finput = fopen ("input", "rt")
      addrandom = i * 13
      print ("'%s' no existe, usando 'input'" % (name))
  else:
    addrandom = 0

  if Finput == None:
      print (" No existe el fichero '%s'" % (name))
      exit (0)
  fscanf (Finput, "%s %s" % (dir, dummy))

  ptdatos_int = datos.itmax
  for ptdatos_int in range(datos.itmax,  datos.itmax+N_DATOS_INT):
    fscanf (Finput, "%ld %s" % (ptdatos_int, dummy))
  
  for ptdatos_real in range( datos.Kappa, datos.Kappa + N_DATOS_FLOAT):
    fscanf (Finput, "%f %s" % (ptdatos_real, dummy))
  fclose (Finput)
  if DEBUG:
    pinta_datos (datos)
  if datos.itmax > maxit:
      printf (" itmax > %i\a\n" % (maxit))
      exit (0)
  datos.seed += addrandom
  if datos.flag < 2:    # existe outxxx.dat o conf. ? 
      sprintf (name, "%s%s%03ld.%i" % (dir, "OUT", datos.itcut, i))
      Foutput = fopen (name, "rb")
      if Foutput != NULL:
          fclose (Foutput)
          printf (" %s  ya existe.\a\n" % (name))
      sprintf (name, "%s%s.%i" % (dir, "conf", i))

      Foutput = fopen (name, "rb")
      if Foutput != NULL:
          fclose (Foutput)
          printf (" %s  ya existe.\a\n" % (name))

def lee_conf(i):
  sprintf (name, "%s%s.%i" % (dir, "conf", i))

  Fconfig = fopen (name, "rb")
  if Fconfig == NULL:
      printf (" No existe el fichero CONF.%i\a\n" % (i))
      exit (0)

  fread (datosb, sizeof (datosb), 1, Fconfig)
  fread (otros_datosb, (unsigned) (otros_datos[0] + 1), 4, Fconfig)
  if otros_datosb[0] != N_OTROS:
      printf ("La configuracion no es compatible con este programa.\n")
      printf ("(otros_datos[0]=%d)\n" % (otros_datosb[0]))
      exit (1)
  for j in range(otros_datos[0]+1):
    if otros_datosb[j] != otros_datos[j]:
        printf ("La configuracion no es compatible con este programa.\n")
        exit (1)
  fread (phi, sizeof (phi[0]), V, Fconfig)
  if DEBUG:
    pinta_datos (datosb)
    #printf("%4d %4d %4d\n",u[0],u[1],u[nlinks-1]) 
  if (datos.itmax != datosb.itmax or 
      datos.mesfr != datosb.mesfr or 
      datos.Lambda != datosb.Lambda or datos.flag == 3):
          printf (" Los datos de CONF.%i no son compatibles con los de INPUT.\n" % (i))
          printf (" Se utilizaran solo los de INPUT.\a\n")

          sprintf (name, "%s%s%03ld.%i" % (dir, "OUT", datos.itcut, i))

          Foutput = fopen (name, "rb")
          if Foutput != NULL:
              fclose (Foutput)
              printf (" %s  ya existe.\a\n" % (name))
  else:
      datos.itcut = datosb.itcut
      datos.seed = datosb.seed
  fclose (Fconfig)

def escribe_medidas(i,t):

  sprintf (name, "%s%s%03d.DAT" % (dir, "OUT", i))

  Foutput = fopen (name, "wb")
  fwrite (datos, sizeof (datos), 1, Foutput)
  fwrite (otros_datos, sizeof (otros_datos), 1, Foutput)
  for idat in range(0, n_obs):
    fwrite (v_dat[idat][0], 4 * datos.itmax, 1, Foutput)
  fclose (Foutput)


  sprintf (name_dollar, "%s%s" % (dir, "conf.$$$"))
  sprintf (name, "%s%s.%i" % (dir, "conf", i))
  sprintf (name_old, "%s%s.%i" % (dir, "confold", i))

  Fconfig = fopen (name_dollar, "wb")
  fwrite (datos, sizeof (datos), 1, Fconfig)
  if DEBUG:
    pinta_datos (datos)
  fwrite (otros_datos, sizeof (otros_datos), 1, Fconfig)
  fwrite (phi, sizeof (phi[0]), V, Fconfig)

  fclose (Fconfig)
  remove (name_old)
  rename (name, name_old)
  rename (name_dollar, name)
