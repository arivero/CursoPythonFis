#include "lambda.h"

char dir[LPATH];
unsigned int irr[256];
unsigned int ir1;
unsigned char ind,ig1,ig2,ig3;

precision phi[V];		/* Campo */

int x_p[L],y_p[L],z_p[L], /* direccionamientos */
  x_m[L],y_m[L],z_m[L];
int neigh[2*Dim];

double cons,good;
double obs[n_obs];
struct s_datos datos;

float v_dat[n_obs][maxit];
precision co[L],si[L];              /* -> Estimador */
char name_obs[n_ope][256]={"E_c","E2","E4","M","F","SD"};

extern void lee_datos(int);
extern void lee_conf(int);
extern void escribe_res(int);
extern void escribe_medidas(int,int);
extern void escribe_conf(int);
extern void table(void);
extern void tiempo(void);
extern void Direccionamientos(void);
extern void Inicializa(long int,long int);
extern void Metropolis(int);
extern void FlipCluster(int,int,int);
extern void Ajustadelta(double,double);
extern void Medida(void);
extern void Correlacion(void);
char name_evol[LPATH+12];
int main(void)
{
	int i, ibin, it, j, site, iop;
	int x, y, z;
	float temp[n_obs], temp2[n_obs];
	double temp_final[n_obs], temp_final2[n_obs];
	unsigned long int low, high;
	FILE* evol;

	Direccionamientos();
	tiempo();
	lee_datos(0);
	table();
	if (datos.flag >= 2)
		lee_conf(0);
	cons = (float)V * datos.mesfr * datos.itmax * nhit;

	Inicializa(datos.seed, datos.flag);
	srand((int)datos.seed);
#ifdef EVOL
	sprintf(name_evol, "%s%s", dir, "evol.dat");
	if ((evol = fopen(name_evol, "wt")) == NULL)
	{
		printf("Error abriendo fichero %s\n", name_evol);
		exit(1);
	}
	else
		fclose(evol);
#endif
	for (i = 0; i < 256; i++)
	{
#ifdef SUN4
		irr[i] = rand();
#else
		low = rand();
		high = rand();
		irr[i] = low ^ (high << 16);
#endif
	}
	ind = ig1 = ig2 = ig3 = 0;

	for (j = 0; j < datos.mesfr * 10; j++) /*loop de MonteCarlo sin medidas */
	{

		site = 0;
		for (z = 0; z < L; z++)
		{
			neigh[5] = z_p[z];
			neigh[4] = z_m[z];
			for (y = 0; y < L; y++)
			{
				neigh[3] = y_p[y];
				neigh[2] = y_m[y];
				for (x = 0; x < L; x++)
				{
					neigh[1] = x_p[x];
					neigh[0] = x_m[x];
					Metropolis(site);
					site++;
				}
			}
		}
	} /* Fin for datos.mesfr */

	for (iop = 0; iop < n_obs; iop++)
		temp_final[iop] = temp_final2[iop] = 0;

	for (ibin = datos.itcut; ibin < datos.nbin; ibin++) /*loop en numero de bloques*/
	{
		srand((int)datos.seed);    /* asi se reproduce la misma secuencia que
					   cuando se lee de un backup              */
		for (iop = 0; iop < n_obs; iop++)
			temp[iop] = temp2[iop] = 0;

		good = 0.0F;

		for (it = 0; it < datos.itmax; it++)
		{
			for (j = 0; j < datos.mesfr; j++) /*loop de MonteCarlo sin medidas */
			{

				site = 0;
				for (z = 0; z < L; z++)
				{
					neigh[5] = z_p[z];
					neigh[4] = z_m[z];
					for (y = 0; y < L; y++)
					{
						neigh[3] = y_p[y];
						neigh[2] = y_m[y];
						for (x = 0; x < L; x++)
						{
							neigh[1] = x_p[x];
							neigh[0] = x_m[x];
							Metropolis(site);
							site++;
						}
					}
				}
			} /* Fin for datos.mesfr */

		  /*Ajustadelta(cons,good);*/
			Medida();

			for (iop = 0; iop < n_obs; iop++)
				v_dat[iop][it] = obs[iop];

			for (iop = 0; iop < n_obs; iop++)
			{
				temp[iop] += obs[iop];
				temp2[iop] += obs[iop] * obs[iop];
			}
		}/* Fin for datos.itmax */

		for (iop = 0; iop < n_obs; iop++)
		{
			temp_final[iop] += temp[iop];
			temp_final2[iop] += temp2[iop];
		}


		for (iop = 0; iop < n_obs; iop++)
			temp[iop] /= datos.itmax;

		tiempo();
		printf("A=%4.2f ", good / cons);
		printf("i=%d ", ibin);
		for (x = 0; x < n_ope; x++)
			printf("%s=%+5.3f ", name_obs[x], temp[x]);
		printf("\n");

		escribe_medidas(ibin, 0);

		datos.seed = rand();
		/*datos.delta=delta;*/
		datos.itcut = ibin + 1;
		escribe_conf(0);



	} /* Fin for datos.nbin */

	for (iop = 0; iop < n_obs; iop++)
	{
		temp_final[iop] /= (datos.itmax * datos.nbin);
		temp_final2[iop] /= (datos.itmax * datos.nbin);
	}
	double err;

	printf("Final Results\n");
	for (iop = 0; iop < n_obs; iop++)
	{
		err = sqrt(temp_final2[iop] - temp_final[iop] * temp_final[iop]) / sqrt(datos.itmax * datos.nbin);
		printf("O[%d]= %lf +/- %lf\n", iop, temp_final[iop], err);
	}


	return 1;
}

