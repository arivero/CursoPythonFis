"""
tiempo 200 loops con listas  22 segundos
tiempo 200 loops con arrays python 26 segundos
tiempo 200 loops arrays numpy  69 secs user, 1:10
tiempo 200 loops arrays y sin, sqrt numpy 84 segundos. 1:24
tiempo vectorizando euler tiempo vectorizando y sin reallocs 80 seg user 1:24 total
 si añadimos kronecker: baja a 45 segundos ... y sigue dando lo mismo que el Npython.txt :-)
 si transponemos para poder multiplicar vectorizado, nos baja a 39 segundos
 y a 35 segundos si usamos la transposicion tambien en la distancia.
Finalmente, haciendo matricialmente las distancias ¡bajamos a 7 segundos! O menos si usamos otra multiplicacion
"""
#from numba import njit
import numpy
import array
import numpy as np
from numpy import sqrt,sin, square

N_par=100
N_secs=200

kronecker=np.eye(N_par)
nodiag=1-kronecker
#from numba import njit

h=0.0001
    #h=0.0001 #//Paso temporal de la ecuacion diferencial discreta
    #epsilon=1.0 #//Para evitar la singularidad en el cero
DEBUG=False
EULER=False
VERLET=not EULER
G_Un=1000.0
epsilon=1.0
M=numpy.empty(N_par,dtype=numpy.float64)
for i in range(N_par):
        M[i]=1.0+i
    #el vector de Masas es (n,), ojo no confundir con (n,1) o (1,n) que son matrices
    #y es lo que debemos usar para que el broadcast funcione: un producto (3,1) * 3
MM=M[:,None] * M #Asi, M*M es un (n,n)
Gmm = - G_Un* MM * nodiag


#@njit()
def main():
    xyz=numpy.empty((3,N_par),dtype=numpy.float64)
    v_xyz=numpy.empty((3,N_par),dtype=numpy.float64)
    v_x,v_y,v_z = v_xyz[0],v_xyz[1],v_xyz[2]    
    x,y,z=xyz[0],xyz[1], xyz[2]

    mesfr:int =1000
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
            

    tiempo=0

    print("#     t        T           V             E_t \n")
    F=numpy.empty((3,N_par),dtype=numpy.float64)
 
    for i in range(N_secs):
        for j in range(mesfr):
            Evoluciona_dt(F,xyz,v_xyz,x,y,z,v_x,v_y,v_z)
        tiempo+=mesfr*h
        Escribe_resultados(tiempo,x,y,z,v_x,v_y,v_z)

#@njit()
def Evoluciona_dt(F,xyz,v_xyz, x, y, z, v_x, v_y, v_z):
 
    Fx,Fy,Fz =  F[0],F[1],F[2]

    if EULER: 
        Calcula_Fuerza(F,xyz)
        if DEBUG:
            print("En evoluciona, h=%f\n",h);
            for i in range(N_par):
                print("Evol: F[%d]=%f %f %f ,v=%f %f %f" %(i,Fx[i],Fy[i],Fz[i],v_x[i],v_y[i],v_z[i]));
        #vector N_par, xyz
        xyz += h* v_xyz
        #vector(N_par) xyz, pero M es la masa, solo vector(NPar), pero debe funcionar porque numpy admite esa division por filas
        v_xyz  += F*h/M
    if VERLET:
        #v_temp=numpy.empty((3,N_par),dtype=numpy.float64)
        Calcula_Fuerza(F,xyz)
        if DEBUG:
            printf("En evoluciona, h=%f",h)
            for i in range(N_par):
                print("Evol: F[%d]=%f %f %f ,v=%f %f %f" %( i,Fx[i],Fy[i],Fz[i],v_x[i],v_y[i],v_z[i] ) );
        v_temp=v_xyz+0.5*F*h/M
        xyz+=h*v_temp
        Calcula_Fuerza(F,xyz) #Ya hemos cambiado r, esta es la nueva fuerza
        #v_xyz.fill(0.0)
        np.copyto(v_xyz,v_temp+0.5*F*h/M)

#@njit()
def Calcula_Fuerza(F,xyz):
    #xyz es un (3,n) 
    #F es tambien un (3,n)
    #vectors tiene que ser un (3,n,n). Promovemos xyz a un (3,1,n) y a un (3,n,1)
    vectors=xyz[:,None,:]-xyz[:,:,None] #ojo al signo de ambiguedad
    #r2 es un (n,n)
    x=xyz[0]
    y=xyz[1]
    z=xyz[2]
    r2=epsilon+(x[:,None]-x)*(x[:,None]-x) + (y[:,None]-y)*(y[:,None]-y)+(z[:,None]-z)*(z[:,None]-z)
    #r2=epsilon+np.sum(vectors*vectors,axis=0) #mas rapido, pero diverge distinto
    distance=np.sqrt(r2)
    r2=r2*distance

    F.fill(0.0)
    F += np.sum(Gmm*vectors/r2,axis=1) #### la suma en axis=1 y axis=2 no da lo mismo, es el signo +- 
    #return F


#@njit()
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
        if DEBUG:
            print("i=%3d,r=(%-10.3lf,%-10.3lf,%-10.3lf),v=(%-10.3lf,%-10.3lf,%-10.3lf),Ec=%-10.3lf,Ep=%-10.3lf\n",
                   i,x[i],y[i],z[i],v_x[i],v_y[i],v_z[i],Energia_c,Energia_p)
    Energia=Energia_c+Energia_p
    print(" %f %f %f %lf %f %f %f %f %f %f" %(time, Energia_c,Energia_p, Energia,x[0],y[0],z[0],x[1],y[1],z[1] ));
    #//getchar();

main()

