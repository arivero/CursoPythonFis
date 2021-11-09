from math import sqrt,sin
from array import array 
from numba import njit
from pathlib import Path
import numpy
@njit()
def double(n):
    #return [0.0]*n  #expresion Not supported in numba as constant
    return numpy.empty(n,dtype=numpy.float64)
    #return array('d',[0.0]*n) los desconoce

from sys import argv

h=0.0001
N_par=0
N_secs=200

if len(argv) > 1:
    print(argv)
    N_secs=int(argv[1])

G_Un=1000.0
epsilon=1.0
M = double(0)

def main():
    global N_par
    global M
    fichero= Path("./") / "inicial.dat"
    with fichero.open('rt') as f:
        N_par=len(f.readlines())

    M, x,y,z,v_x,v_y,v_z = [double(N_par) for _ in range(7) ]

    mesfr:int =1000

    p_cdm_x,p_cdm_y,p_cdm_z,s_m= 0.0,0.0,0.0,0.0
    with fichero.open('rt') as f:
        for i, line in enumerate(f.readlines()):
            M[i],x[i],y[i],z[i],v_x[i],v_y[i],v_z[i] = [float(s) for s in line.split()]
            p_cdm_x+=M[i]*v_x[i]
            p_cdm_y+=M[i]*v_y[i]
            p_cdm_z+=M[i]*v_z[i]
            s_m+=M[i]

    for i in range(N_par): #//Nos ponemos en el sistema de referencia centro de masas
        v_x[i]-=p_cdm_x/s_m
        v_y[i]-=p_cdm_y/s_m
        v_z[i]-=p_cdm_z/s_m


    tiempo=0
    import matplotlib.pyplot as plt
    print("#     t        T           V             E_t \n");
    data2d_x, data2d_y, data3d =[],[],[]
    for i in range(N_secs):
        for j in range(mesfr):
            Evoluciona_dt(x,y,z,v_x,v_y,v_z)
        tiempo+=mesfr*h
        #Escribe_resultados(tiempo,x,y,z,v_x,v_y,v_z)
        #genere gráficas de las trayectorias de un subconjunto de objetos, diez como máximo, proyectadas en un plano 2D. 
        data2d_x = data2d_x + [list(x[:10])]
        data2d_y = data2d_y + [list(y[:10])]
        #genere gráficas de la trayectoria de un solo objeto, el primer planeta de la lista, en 3D
        data3d = data3d + [[x[0],y[0],z[0]]]
    #print(data2d_x[:3], data2d_y[:3])
    #see https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
        if i % 10 == 0:
            print("secs=",i)
            fig = plt.figure()
            plt.plot(data2d_x,data2d_y)
            plt.savefig("mov{}.jpg".format(i))
            plt.show()
            plt.close()
            
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.plot([x for x,y,z in data3d],[y for x,y,z in data3d],[z for x,y,z in data3d] )
    fig.show()


@njit()
def Evoluciona_dt(x, y, z, v_x, v_y, v_z):
        #int i;
        Fx,Fy,Fz =   double(N_par),double(N_par),double(N_par) #  (double(N_par) for _ in range(3) )
        v_temp_x,v_temp_y,v_temp_z = double(N_par),double(N_par),double(N_par)     #(double(N_par) for _ in range(3) )
 
    
        Calcula_Fuerza(x,y,z,Fx,Fy,Fz)
        for i in range(N_par):
            v_temp_x[i]=v_x[i]+0.5*Fx[i]*h/M[i]
            x[i]+=h*v_temp_x[i]
            v_temp_y[i]=v_y[i]+0.5*Fy[i]*h/M[i]
            y[i]+=h*v_temp_y[i]
            v_temp_z[i]=v_z[i]+0.5*Fz[i]*h/M[i]
            z[i]+=h*v_temp_z[i]
        Calcula_Fuerza(x,y,z,Fx,Fy,Fz) #Ya hemos cambiado r, esta es la nueva fuerza
        for i in range(N_par):
            v_x[i]  = v_temp_x[i]+0.5*Fx[i]*h/M[i]
            v_y[i]  = v_temp_y[i]+0.5*Fy[i]*h/M[i]
            v_z[i]  = v_temp_z[i]+0.5*Fz[i]*h/M[i]

@njit()
def Calcula_Fuerza(x,y,z,Fx,Fy,Fz):

    #double r2,distance;
    #int i,j;
    for i in range(N_par):
        Fx[i]=Fy[i]=Fz[i]=0.0
        for j in range(N_par):
            if(i==j):
                continue
            r2=epsilon+(x[i]-x[j])*(x[i]-x[j])+(y[i]-y[j])*(y[i]-y[j])+(z[i]-z[j])*(z[i]-z[j])
            distance=sqrt(r2)
            r2=r2*distance
            Fx[i]-=(G_Un*M[i]*M[j]*(x[i]-x[j])/r2)
            Fy[i]-=(G_Un*M[i]*M[j]*(y[i]-y[j])/r2)
            Fz[i]-=(G_Un*M[i]*M[j]*(z[i]-z[j])/r2)

 
def Escribe_resultados(time, x, y, z, v_x, v_y, v_z):

   
    Energia_p,Energia_c= 0.0, 0.0
    for i in range(N_par):
        for j in range(N_par):
            if(j==i):
                continue
            r2=epsilon+(x[i]-x[j])*(x[i]-x[j])+ (y[i]-y[j])*(y[i]-y[j])+(z[i]-z[j])*(z[i]-z[j]);
            distancia=sqrt(r2);
            Energia_p-=(G_Un*M[i]*M[j]/distancia/2.0); 
                #/* Cuento todo dos veces !!! por eso /2*/
        Energia_c+=0.5*M[i]*(v_x[i]*v_x[i]+v_y[i]*v_y[i]+v_z[i]*v_z[i]);
 
    Energia=Energia_c+Energia_p
    print(" %f %f %f %lf %f %f %f %f %f %f" % (time, Energia_c,Energia_p, Energia,x[0],y[0],z[0],x[1],y[1],z[1] ));


main()

