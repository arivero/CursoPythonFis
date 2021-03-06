#include "lambda.h"


extern char dir[];
extern precision phi[];
extern float v_dat[n_obs][maxit];
extern struct s_datos datos;

FILE *Finput,*Foutput,*Fconfig;
int otros_datos[N_OTROS+1]={N_OTROS,L,L,L};

void tiempo(void)
{
    static time_t time1=0,
		  time2;

    time2 = time(NULL);
    if (time1>0)
	printf("%4ds:",time2-time1);
    time1=time2;
}

void pinta_datos(struct s_datos *dat)   /* solo para debug */
{
    printf("itmax  %ld \n",dat->itmax);
    printf("mesfr  %ld \n",dat->mesfr);
    printf("nbin   %ld \n",dat->nbin);
    printf("itcut  %ld \n",dat->itcut);
    printf("flag   %ld \n",dat->flag);
    printf("seed   %ld \n",dat->seed);
    printf("Kappa %f  \n",dat->Kappa);
    printf("Lambda %f \n",dat->Lambda);
    printf("delta  %f  \n",dat->delta);
}
void lee_datos(int i)
{
    int j;
    long int * ptdatos_int;
    float * ptdatos_real;
    int addrandom;

    char name[LPATH+12],dummy[LPATH];

    sprintf(name,"%s.%i","input",i);

    Finput=fopen(name,"rt");


    if (Finput==NULL)
    {
	Finput=fopen("input","rt");
	addrandom=i*13;
	printf("'%s' no existe, usando 'input'\n",name);
    }
    else
	addrandom=0;

    if (Finput==NULL)
    {
	printf(" No existe el fichero '%s'\n",name);
	exit(0);
    }
    fscanf(Finput,"%s %s",dir,dummy);
    for (j=0,ptdatos_int=&datos.itmax;j<N_DATOS_INT;j++)
	fscanf(Finput,"%ld %s",ptdatos_int++,dummy);
	for (j=0,ptdatos_real=&datos.Kappa;j<N_DATOS_FLOAT;j++)
	fscanf(Finput,"%f %s",ptdatos_real++,dummy);
    fclose(Finput);
#ifdef DEBUG
    pinta_datos(&datos);
#endif
    if (datos.itmax>maxit)
    {
	printf(" itmax > %i\a\n",maxit);
	exit(0);
    }
    datos.seed+=addrandom;
    if (datos.flag<2)
    {                                      /* existe outxxx.dat o conf. ? */

	sprintf(name,"%s%s%03ld.%i",dir,"OUT",datos.itcut,i);
	Foutput=fopen(name,"rb");
	if (Foutput!=NULL)
	{
	    fclose(Foutput);
	    printf(" %s  ya existe.\a\n",name);
	}
	sprintf(name,"%s%s.%i",dir,"conf",i);

	Foutput=fopen(name,"rb");
	if (Foutput!=NULL)
	{
	    fclose(Foutput);
	    printf(" %s  ya existe.\a\n",name);
	}
    }
}

void lee_conf(int i)
{
    struct s_datos datosb;
    char name[LPATH+12];
    int j;
    int otros_datosb[N_OTROS+1];
    sprintf(name,"%s%s.%i",dir,"conf",i);

    Fconfig=fopen(name,"rb");
    if (Fconfig==NULL)
    {
	printf(" No existe el fichero CONF.%i\a\n",i);
	exit(0);
    }

    fread(&datosb,sizeof(datosb),1,Fconfig);
    fread(otros_datosb,(unsigned) (otros_datos[0]+1),4,Fconfig);
    if(otros_datosb[0]!=N_OTROS)
      {
	printf("La configuracion no es compatible con este programa.\n");
	printf("(otros_datos[0]=%d)\n",otros_datosb[0]);
	exit(1);
      }
for(j=0;j<=otros_datos[0];j++)
    if(otros_datosb[j]!=otros_datos[j])
      {
	printf("La configuracion no es compatible con este programa.\n");
	exit(1);
      }
    fread(phi,sizeof(phi[0]),V,Fconfig);
#ifdef DEBUG
    pinta_datos(&datosb);
    /*printf("%4d %4d %4d\n",u[0],u[1],u[nlinks-1]);*/
#endif
    if (datos.itmax != datosb.itmax ||
	datos.mesfr != datosb.mesfr ||
	datos.Lambda  != datosb.Lambda  ||
	datos.flag  == 3 )
    {
	printf(" Los datos de CONF.%i no son compatibles con los de INPUT.\n",i);
	printf(" Se utilizaran solo los de INPUT.\a\n");

	sprintf(name,"%s%s%03ld.%i",dir,"OUT",datos.itcut,i);

	Foutput=fopen(name,"rb");
	if (Foutput!=NULL)
	{
	    fclose(Foutput);
	    printf(" %s  ya existe.\a\n",name);
	}
    }
    else
    {
	datos.itcut=datosb.itcut;
	datos.seed=datosb.seed;
    }
    fclose(Fconfig);
}


void escribe_medidas(int i,int t)
{
    int idat;
    char name[LPATH+12];

    sprintf(name,"%s%s%03d.DAT",dir,"OUT",i);

    Foutput=fopen(name,"wb");
    fwrite(&datos,sizeof(datos),1,Foutput);
    fwrite(otros_datos,sizeof(otros_datos),1,Foutput);
    for(idat=0;idat<n_obs;idat++)
	fwrite(&v_dat[idat][0],4*(int) datos.itmax,1,Foutput);
    fclose(Foutput);
}
void escribe_conf(int i)
{
    char name[LPATH+12],name_dollar[LPATH+12],name_old[LPATH+12];

    sprintf(name_dollar,"%s%s",dir,"conf.$$$");
    sprintf(name,"%s%s.%i",dir,"conf",i);
    sprintf(name_old,"%s%s.%i",dir,"confold",i);

    Fconfig=fopen(name_dollar,"wb");
    fwrite(&datos,sizeof(datos),1,Fconfig);
#ifdef DEBUG
    pinta_datos(&datos);
#endif
    fwrite(otros_datos,sizeof(otros_datos),1,Fconfig);
    fwrite(phi,sizeof(phi[0]),V,Fconfig);

    fclose(Fconfig);
    remove(name_old);
    rename(name,name_old);
    rename(name_dollar,name);
}










