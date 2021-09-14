#include "lambda.h"

extern int x_p[],y_p[],z_p[],
	   x_m[],y_m[],z_m[];

extern precision phi[];
extern precision co[],si[];
extern struct s_datos datos;

void Direccionamientos(void)
{
    int i;
	for (i=0;i<L;i++)
	{
	    x_p[i]= 1;
	    x_m[i]=-1;
	    y_p[i]= L;
	    y_m[i]=-L;
	    z_p[i]= L*L;
	    z_m[i]=-L*L;

	}
	x_m[0]= L-1;
	y_m[0]=(L-1)*L;
	x_p[L-1]=-x_m[0];
	y_p[L-1]=-y_m[0];
	z_m[0]=(L-1)*L*L;
	z_p[L-1]=-z_m[0];

}

void Inicializa( long semilla, long flag)
{
	int igen;

	srand(semilla);


	if (flag<2)
	  {
	    for (igen=0;igen<V;igen++)
	      if (flag == 0)
			phi[igen]= RAN()*datos.delta*4.;
	      else
			phi[igen]=1.0;
	  }
}

void table(void)
{
long i;
for(i=0;i<L;i++)
  {
    co[i]=cos(TWOPI*(float) i/(float) L);
    si[i]=sin(TWOPI*(float) i/(float) L);
  }
}


