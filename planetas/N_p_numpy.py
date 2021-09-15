"""
tiempo 200 loops con listas  22 segundos
tiempo 200 loops con arrays python 26 segundos
tiempo 200 loops arrays numpy  69 secs user, 1:10
tiempo 200 loops arrays y sin, sqrt numpy 84 segundos. 1:24
tiempo vectorizando euler 82 segundos 1:22
"""
#from numba import njit
import numpy
import array
from numpy import sqrt,sin
#@njit()
def double(n):
    #return [0.0]*n
    return numpy.empty(n,dtype=numpy.float64)
    #return array.array('d',[0.0]*n)

from numba import njit

h=0.0001
N_par=10
DEBUG=False
EULER=True
VERLET=not EULER
G_Un=1000.0
epsilon=1.0
M=double(N_par)
for i in range(N_par):
        M[i]=1.0+i
#@njit()
def main():
    x,y,z,v_x,v_y,v_z = [double(N_par) for _ in range(6) ]
    #double p_cdm_x,p_cdm_y,p_cdm_z,s_m,restar_x,restar_y,restar_z;
    #double tiempo;
    #int i,j;
    mesfr:int =1000
    #global G_Un
    #global M
    #global epsilon
    #global h
    #G_Un=1000.0
    p_cdm_x,p_cdm_y,p_cdm_z,s_m= 0.0,0.0,0.0,0.0
    for i in range(N_par):
        #M[i]=1.0+i
        x[i]=(N_par*i + 10)
        y[i]=68*sqrt(i) + 13
        z[i]=N_par*sin(6.28*i/N_par)+18
        v_x[i]=i/(10*N_par)
        v_y[i]=2*v_x[i]
        v_z[i]=v_x[i]
        p_cdm_x+=M[i]*v_x[i]
        p_cdm_y+=M[i]*v_y[i]
        p_cdm_z+=M[i]*v_z[i]
        s_m+=M[i]
        
    #//Nos ponemos en el sistema de referencia centro de masas
    restar_x=p_cdm_x/s_m
    restar_y=p_cdm_y/s_m
    restar_z=p_cdm_z/s_m
    #vector (N_par): 
    v_x-=restar_x
    v_y-=restar_y
    v_z-=restar_z

    if DEBUG:
        for i in range(N_par):
            print("%f %f %f %f %f %f" %( x[i],y[i],z[i],v_x[i],v_y[i],v_z[i]))
            
    #h=0.0001 #//Paso temporal de la ecuacion diferencial discreta
    #epsilon=1.0 #//Para evitar la singularidad en el cero

    tiempo=0

    print("#     t        T           V             E_t \n");
 
    for i in range(200):
        for j in range(mesfr):
            Evoluciona_dt(x,y,z,v_x,v_y,v_z)
        tiempo+=mesfr*h
        Escribe_resultados(tiempo,x,y,z,v_x,v_y,v_z)

#@njit()
def Evoluciona_dt(x, y, z, v_x, v_y, v_z):
    #int i;
    Fx,Fy,Fz =   double(N_par),double(N_par),double(N_par) #  (double(N_par) for _ in range(3) )
    v_temp_x,v_temp_y,v_temp_z = double(N_par),double(N_par),double(N_par)     #(double(N_par) for _ in range(3) )
    if EULER: 
        Calcula_Fuerza(x,y,z,Fx,Fy,Fz);
        if DEBUG:
            print("En evoluciona, h=%f\n",h);
            for i in range(N_par):
                print("Evol: F[%d]=%f %f %f ,v=%f %f %f" %(i,Fx[i],Fy[i],Fz[i],v_x[i],v_y[i],v_z[i]));
        #vector N_par
        x+=h*v_x
        y+=h*v_y
        z+=h*v_z
        #vector(N_par):
        v_x  += (Fx*h/M);
        v_y  += (Fy*h/M);
        v_z  += (Fz*h/M);
    if VERLET:
        Calcula_Fuerza(x,y,z,Fx,Fy,Fz);
        if DEBUG:
            printf("En evoluciona, h=%f",h);
            for i in range(N_par):
                print("Evol: F[%d]=%f %f %f ,v=%f %f %f" %( i,Fx[i],Fy[i],Fz[i],v_x[i],v_y[i],v_z[i] ) );
        for i in range(N_par):
            v_temp_x[i]=v_x[i]+0.5*Fx[i]*h/M[i];
            x[i]+=h*v_temp_x[i];
            v_temp_y[i]=v_y[i]+0.5*Fy[i]*h/M[i];
            y[i]+=h*v_temp_y[i]
            v_temp_z[i]=v_z[i]+0.5*Fz[i]*h/M[i];
            z[i]+=h*v_temp_z[i]
        Calcula_Fuerza(x,y,z,Fx,Fy,Fz) #Ya hemos cambiado r, esta es la nueva fuerza
        for i in range(N_par):
            v_x[i]  = v_temp_x[i]+0.5*Fx[i]*h/M[i]
            v_y[i]  = v_temp_y[i]+0.5*Fy[i]*h/M[i]
            v_z[i]  = v_temp_z[i]+0.5*Fz[i]*h/M[i]

#@njit()
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
            if DEBUG:
                print("F[%d]=%f %f %f" % (i,Fx[i],Fy[i],Fz[i]) )


#@njit()
def Escribe_resultados(time, x, y, z, v_x, v_y, v_z):

    #double r2,distancia;
    #double Energia_c,Energia_p,Energia;
    #int i,j;

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
        if DEBUG:
            print("i=%3d,r=(%-10.3lf,%-10.3lf,%-10.3lf),v=(%-10.3lf,%-10.3lf,%-10.3lf),Ec=%-10.3lf,Ep=%-10.3lf\n",
                   i,x[i],y[i],z[i],v_x[i],v_y[i],v_z[i],Energia_c,Energia_p)
    Energia=Energia_c+Energia_p
    print(" %f %f %f %lf %f %f %f %f %f %f" ,(time, Energia_c,Energia_p, Energia,x[0],y[0],z[0],x[1],y[1],z[1] ));
    #//getchar();

main()

