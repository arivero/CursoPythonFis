from configlambda import *
import mainlambda
from mainlambda import  phi, v_dat, datos
from pathlib import Path
import shelve
import dataclasses
import struct
import array

#en C: otros_datos[N_OTROS+1]={N_OTROS,L,L,L}
otros_datos = [N_OTROS, L,L,L]

#nota sobre io: python no tiene scanf. Se recomienda usar split o expresiones regulares

from time import time
time1 = time()
def tiempo ():
  global time1
  time2 = time ()
  if time1 > 0:
    print ("%4ds:" % (time2 - time1), end='')
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
  global dirname
  name= Path( "%s.%i" % ("input", i) ) 
  if not name.exists():
      addrandom = i * 13
      print ("'%s' no existe, usando 'input'" % (name))
      name= Path("input")
  else:
    addrandom = 0
  if not name.exists():
      print (" No existe el fichero '%s'" % (name))
      exit (0)
  with name.open("rt") as Finput:
    dirname,_ = Finput.readline().split()
    mainlambda.localdir=dirname
    datos.itmax=int(Finput.readline().split()[0])
    datos.mesfr=int(next(Finput).split()[0])                   
    datos.nbin=int(next(Finput).split().pop(0))                            
    datos.itcut=int(Finput.readline().split()[0])            
    datos.flag=int(Finput.readline().split().pop(0))
    datos.seed=int(Finput.readline().split()[0])                               
    datos.Kappa=float(Finput.readline().split()[0])        
    datos.Lambda=float(Finput.readline().split()[0])         
    datos.delta=float(Finput.readline().split()[0]) 
  #fclose (Finput)
  if True: #DEBUG:
    pinta_datos (datos)
  if datos.itmax > maxit:
      print (" itmax > %i\a" % (maxit))
      exit (0)
  datos.seed += addrandom
  if datos.flag < 2:    # existe outxxx.dat o conf. ? 
      name = Path( "%s%s%03ld.%i" % (dir, "OUT", datos.itcut, i))
      if name.exists():
          printf (" %s  ya existe.\a" % (name))
      name = Path( "%s%s.%i" % (dir, "conf", i))
      if name.exists():
          printf (" %s  ya existe.\a" % (name))

def lee_conf(i):
  #TODO (estamos pendientes de decidir el formato de la conf)
  #leer una shelf puede ejecutar codigo arbitrario :-( 
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
  global dirname
  name=Path ( "%s%s%03d.DAT" % (dirname, "OUT", i))

  with name.open ("wb") as Foutput:
      #fwrite (datos, sizeof (datos), 1, Foutput)
      #fwrite (otros_datos, sizeof (otros_datos), 1, Foutput)
      for idat in range(0, n_obs):
        k=array.array('f') 
        k.fromlist(v_dat[idat])
        Foutput.write(k.tobytes())
      #  fwrite (v_dat[idat][0], 4 * datos.itmax, 1, Foutput)
  with shelve.open(str(name)+".shelf") as shelf:
    shelf["datos"]=datos
    shelf["otros_datos"]=otros_datos
    shelf["v_dat"]=v_dat


def escribe_conf(i):
  name_dollar= Path( "%s%s" % (dirname, "conf.$$$"))
  name=Path ("%s%s.%i" % (dirname, "conf", i))
  name_old=Path ("%s%s.%i" % (dirname, "confold", i))

  if DEBUG:
        pinta_datos (datos)
    
  with name_dollar.open ("wb") as Fconfig:
      for field in dataclasses.fields(datos):
            if field.type==int:
                tipo='I' #unsigned 
            else:
                tipo='f' #float 4 bits
            Fconfig.write(struct.pack(tipo,datos.__dict__[field.name]))
      Fconfig.write(struct.pack('iiii',*otros_datos))
      #k=array.array('d')
      #k.fromlist(phi)
      Fconfig.write(phi.tobytes())
  with shelve.open(str(name_dollar)+".shelf") as shelf:
    shelf["datos"]=datos
    shelf["otros_datos"]=otros_datos
    shelf["phi"]=phi
  
  if name.exists():
      if name_old.exists():
          name_old.unlink() #equivale a os.remove
      name.rename(name_old)
  name_dollar.rename(name)
