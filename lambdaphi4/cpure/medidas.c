#include "lambda.h"

extern precision phi[];
extern precision co[],si[];
extern double obs[];
int neigh[2*Dim];
extern int x_p[],y_p[],z_p[],
		   x_m[],y_m[],z_m[];
extern struct s_datos datos;
extern char name_evol[LPATH+12];

void Medida(void)
{
  float RCX,RSX,RCY,RSY,RCZ,RSZ,RCT,RST;
  double energia_c,energia_2,energia_4;
  double phir2,u12,SD; 
  int sit;
  FILE *ev;

precision magne,u1,Staple,Staple_m;

  int x,y,z,sit1,sit3,sit5,sit0,sit2,sit4;
  
  sit=0;
  energia_c=energia_2=energia_4=0.;
  magne=0.0;
  phir2=0.0;
  SD=0;
  RCX=RSX=RCY=RSY=RCZ=RSZ=RCT=RST=0.0;
  for (z=0;z<L;z++)
    {
      neigh[5]=z_p[z];
      neigh[4]=z_m[z];
      for (y=0;y<L;y++)
	{
	  neigh[3]=y_p[y];
	  neigh[2]=y_m[y];
	  for (x=0;x<L;x++)
	    {
	      neigh[1]=x_p[x];
	      neigh[0]=x_m[x];
	      
	      u1=phi[sit];
	      
	      u12=u1*u1;
	      
	      
	      sit1=sit+neigh[1];
	      sit3=sit+neigh[3];
	      sit5=sit+neigh[5];

	      
	      Staple=phi[sit1]+phi[sit3]+phi[sit5];
		  energia_c+=u1*Staple;

	      sit0=sit+neigh[0];
	      sit2=sit+neigh[2];
	      sit4=sit+neigh[4];

	      Staple_m=Staple+phi[sit0]+phi[sit2]+phi[sit4];

	      SD+=exp(-2.0*datos.Kappa*u1*Staple_m);

	      
	      magne+=u1;
	      energia_2+=u12;
	      energia_4+=u12*u12;
	      
	      RCX+=u1*co[x];  /* Propagador a momento minimo(>0) */
	      RSX+=u1*si[x];
	      RCY+=u1*co[y];
	      RSY+=u1*si[y];
	      RCZ+=u1*co[z];
	      RSZ+=u1*si[z];
	      sit++;
	    }
	}
    }
  obs[0]=energia_c   * Normaener;
  obs[1]=energia_2   * Normamag;
  obs[2]=energia_4   * Normamag;
  obs[3]=magne       * Normamag;
  obs[4]=(RCX*RCX+RSX*RSX+RCY*RCY+RSY*RSY+
	   RCZ*RCZ+RSZ*RSZ)* Normamag / 3.0;
  obs[5]=SD          * Normamag;

  ev=fopen(name_evol,"at");

      for(x=0;x<n_ope;x++)
		fprintf(ev,"%lf ",obs[x]);
      fprintf(ev,"\n");

  fclose(ev);

}


