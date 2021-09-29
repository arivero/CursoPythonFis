from lambdaconfig import *

char dir[LPATH]; #root
unsigned int irr[256] #update
unsigned int ir1 #update INMUTABLE NO SE USA
unsigned char ind,ig1,ig2,ig3 #update INMUTABLE SOLO SE PONEN A CERO EN INIT

precision phi[V];  #inici medidas rrot update				

int x_p[L],y_p[L],z_p[L], #inici medidas
  x_m[L],y_m[L],z_m[L];
int neigh[2*Dim];

double cons,good; #update INMUTABLE Ya no se reajustan, pero se inicializan desde fichero :-(
double obs[n_obs]  #medidas
struct s_datos datos #inici medidas root update

float v_dat[n_obs][maxit] #root
precision co[L],si[L]   #inici medidas
char name_evol[LPATH+12] #medidas

char name_obs[n_ope][256]={"E_c","E2","E4","M","F","SD"};

if __name__=='__main__'
    from root import lee_datos,lee_conf,escribe_medidas,escribe_conf,tiempo
    from inici import table,Direccionamientos,Inicializa
    from update import Metropolis
    from medida import Medida
    #el bloque "compartido"
    from lambda import * 

int main(void)
{
  int i,ibin,it,j,site,iop;
  int x,y,z;
  float temp[n_obs];
  unsigned long int low,high;
  FILE *evol;

  Direccionamientos();
  tiempo();
  lee_datos(0);
  table();
  if (datos.flag>=2)
    lee_conf(0);
  cons=(float) V*datos.mesfr*datos.itmax*nhit;

  Inicializa(datos.seed,datos.flag);
  srand((int) datos.seed);
#ifdef EVOL
	sprintf(name_evol,"%s%s",dir,"evol.dat");
	if((evol=fopen(name_evol,"wt"))==NULL)
	{
		printf("Error abriendo fichero %s\n",name_evol);
		exit(1);
	}
	else
		fclose(evol);
#endif
  for(i=0;i<256;i++)
    {
#ifdef SUN4
      irr[i]=rand();
#else
      low=rand();
      high=rand();
      irr[i]=low^(high<<16);
#endif
    }
  ind=ig1=ig2=ig3=0;


  for (ibin=datos.itcut;ibin<datos.nbin;ibin++) /*loop en numero de bloques*/
    {
      srand((int) datos.seed);    /* asi se reproduce la misma secuencia que
				     cuando se lee de un backup              */
      for (iop=0;iop<n_obs;iop++)
	temp[iop]=0;

      good=0.0F;
	
      for (it=0;it<datos.itmax;it++)
	{
	  for (j=0;j<datos.mesfr;j++) /*loop de MonteCarlo sin medidas */
	    {

		  site=0;
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
			      Metropolis(site);
			      site++;
			    }
			}
		    }				
	    } /* Fin for datos.mesfr */

	  /*Ajustadelta(cons,good);*/
	  Medida();
	    
	  for (iop=0;iop<n_obs;iop++)
	    v_dat[iop][it] = obs[iop];
	    
	  for (iop=0;iop<n_obs;iop++)
	    temp[iop]+=obs[iop];
	    
	}/* Fin for datos.itmax */

      for (iop=0;iop<n_obs;iop++)
	temp[iop]/=datos.itmax;

      tiempo();
      printf("A=%4.2f ",good/cons);
      printf("i=%d ",ibin);
      for(x=0;x<n_ope;x++)
	printf("%s=%+5.3f ",name_obs[x],temp[x]);
      printf("\n");

      escribe_medidas(ibin,0);

      datos.seed=rand();
      /*datos.delta=delta;*/
      datos.itcut=ibin+1;
      escribe_conf(0);

    } /* Fin for datos.nbin */

  return 1;
}

if __name__='__main__':
    main()
