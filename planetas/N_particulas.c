#include <math.h>
#include <stdio.h>
//#define DEBUG
double h;
#define N_par 100
double G_Un;
double epsilon;
double M[N_par];

void Evoluciona_dt(double *x, double *y,double *z,double *v_x,double *v_y,double *v_z);
void Calcula_Fuerza(double *x,double *y,double *z,double *Fx,double *Fy,double *Fz);
void Escribe_resultados(double time,double *x,double *y, double *z,double *v_x,double *v_y,double *v_z);


#define TRUE 1
main()
{
    
    double x[N_par],y[N_par],z[N_par],v_x[N_par],v_y[N_par],v_z[N_par];
    
    
    double p_cdm_x,p_cdm_y,p_cdm_z,s_m,restar_x,restar_y,restar_z;
    double tiempo;
    int i,j;
    int mesfr=1000;
  

    G_Un=1000.0;

    p_cdm_x=p_cdm_y=p_cdm_z=s_m=0.0;
    for(i=0;i<N_par;i++)
    {
	M[i]=1.0+i;
	x[i]=(N_par*i + 10);
	y[i]=68*sqrt((double)i) + 13;
	z[i]=N_par*sin(6.28*i/N_par)+18;
	v_x[i]=(float)i/(float)(10*N_par);
	v_y[i]=2*v_x[i];
	v_z[i]=v_x[i];
	p_cdm_x+=M[i]*v_x[i];
	p_cdm_y+=M[i]*v_y[i];
	p_cdm_z+=M[i]*v_z[i];
	s_m+=M[i];
    }
    restar_x=p_cdm_x/s_m;
    restar_y=p_cdm_y/s_m;
    restar_z=p_cdm_z/s_m;
       
    for(i=0;i<N_par;i++) //Nos ponemos en el sistema de referencia centro de masas
    {
	v_x[i]-=restar_x;
	v_y[i]-=restar_y;
	v_z[i]-=restar_z;

    }

#ifdef DEBUG
    for(i=0;i<N_par;i++)
	printf("%f %f %f %f %f %f\n",x[i],y[i],z[i],v_x[i],v_y[i],v_z[i]);
#endif


    h=0.0001; //Paso temporal de la ecuacion diferencial discreta
    epsilon=1.0; //Para evitar la singularidad en el cero
    tiempo=0;

    printf("#     t        T           V             E_t \n");
 
    for(i=0;i<200;i++)
    {
	for(j=0;j<mesfr;j++)
	    Evoluciona_dt(x,y,z,v_x,v_y,v_z);
	tiempo+=mesfr*h;
	Escribe_resultados(tiempo,x,y,z,v_x,v_y,v_z);
    }
}



void Evoluciona_dt(double *x, double *y,double *z,double *v_x,double *v_y,double *v_z)
{
    int i;
    double Fx[N_par],Fy[N_par],Fz[N_par];
    double v_temp_x[N_par],v_temp_y[N_par],v_temp_z[N_par];

#define EULER
//#define VERLET


#ifdef EULER  

	
    Calcula_Fuerza(x,y,z,Fx,Fy,Fz);

#ifdef DEBUG
    printf("En evoluciona, h=%f\n",h);
	for(i=0;i<N_par;i++)
	    printf("Evol: F[%d]=%f %f %f ,v=%f %f %f \n",i,Fx[i],Fy[i],Fz[i],v_x[i],v_y[i],v_z[i]);
#endif

	for(i=0;i<N_par;i++)
	{
	    x[i]+=h*v_x[i];
	    y[i]+=h*v_y[i];
	    z[i]+=h*v_z[i];
	}

    for(i=0;i<N_par;i++)
    {
	v_x[i]  += (Fx[i]*h/M[i]);
	v_y[i]  += (Fy[i]*h/M[i]);
	v_z[i]  += (Fz[i]*h/M[i]);

    }

#endif

#ifdef VERLET  

	
    Calcula_Fuerza(x,y,z,Fx,Fy,Fz);

#ifdef DEBUG
    printf("En evoluciona, h=%f\n",h);
	for(i=0;i<N_par;i++)
	    printf("Evol: F[%d]=%f %f %f ,v=%f %f %f \n",i,Fx[i],Fy[i],Fz[i],v_x[i],v_y[i],v_z[i]);
#endif

	for(i=0;i<N_par;i++)
	{
	    v_temp_x[i]=v_x[i]+0.5*Fx[i]*h/M[i];
	    x[i]+=h*v_temp_x[i];

	    v_temp_y[i]=v_y[i]+0.5*Fy[i]*h/M[i];
	    y[i]+=h*v_temp_y[i];

	    v_temp_z[i]=v_z[i]+0.5*Fz[i]*h/M[i];
	    z[i]+=h*v_temp_z[i];
	}



    Calcula_Fuerza(x,y,z,Fx,Fy,Fz);//Ya hemos cambiado r, esta es la nueva fuerza



    for(i=0;i<N_par;i++)
    {
	v_x[i]  = v_temp_x[i]+0.5*Fx[i]*h/M[i];
	v_y[i]  = v_temp_y[i]+0.5*Fy[i]*h/M[i];
	v_z[i]  = v_temp_z[i]+0.5*Fz[i]*h/M[i];

    }

#endif


}


void Calcula_Fuerza(double *x,double *y,double *z,double *Fx,double *Fy,double *Fz)
{
    double r2,distance;
    int i,j;
    for(i=0;i<N_par;i++)
    {
	Fx[i]=Fy[i]=Fz[i]=0.0;
	for(j=0;j<N_par;j++)
	{
	    if(i==j)continue;
	    r2=epsilon+(x[i]-x[j])*(x[i]-x[j])+(y[i]-y[j])*(y[i]-y[j])+(z[i]-z[j])*(z[i]-z[j]);
	    distance=sqrt(r2);
	    r2=r2*distance;
	    Fx[i]-=(G_Un*M[i]*M[j]*(x[i]-x[j])/r2);
	    Fy[i]-=(G_Un*M[i]*M[j]*(y[i]-y[j])/r2);
	    Fz[i]-=(G_Un*M[i]*M[j]*(z[i]-z[j])/r2);
	}
#ifdef DEBUG
	    printf("F[%d]=%f %f %f \n",i,Fx[i],Fy[i],Fz[i]);
#endif


    }
}





void Escribe_resultados(double time,double *x,double *y, double *z,double *v_x,double *v_y,double *v_z)
{
    double r2,distancia;
    double Energia_c,Energia_p,Energia;
    int i,j;

    Energia_p=Energia_c=0.0;
    

    for(i=0;i<N_par;i++)
    {
	for(j=0;j<N_par;j++)
	{
	    if(j==i)continue;
				
	    r2=epsilon+(x[i]-x[j])*(x[i]-x[j])+ (y[i]-y[j])*(y[i]-y[j])+(z[i]-z[j])*(z[i]-z[j]);
	    distancia=sqrt(r2);
	    Energia_p-=(G_Un*M[i]*M[j]/distancia/2.0); 
	    /* Cuento todo dos veces !!! por eso /2*/
	}


	Energia_c+=0.5*M[i]*(v_x[i]*v_x[i]+v_y[i]*v_y[i]+v_z[i]*v_z[i]);


#ifdef DEBUG
	printf("i=%3d,r=(%-10.3lf,%-10.3lf,%-10.3lf),v=(%-10.3lf,%-10.3lf,%-10.3lf),Ec=%-10.3lf,Ep=%-10.3lf\n",
	       i,x[i],y[i],z[i],v_x[i],v_y[i],v_z[i],Energia_c,Energia_p);
#endif
    }
	Energia=Energia_c+Energia_p;

	printf(" %f %f %f %lf %f %f %f %f %f %f \n",time, Energia_c,Energia_p, Energia,x[0],y[0],z[0],x[1],y[1],z[1]);
    //getchar();
}

