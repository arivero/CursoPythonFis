#pragma warning(disable : 4996)
#define n_ope  	   6    	   /* Numero de operadores en cada lattice */
#define nhit       3		   /* numero de hits de Metropolis     	   */
#define maxit      10000            /* maximo de medidas cada escritura 	   */
/***************************************************************************/
/*#define DEBUG*/                  /*escribe en pantalla mas informacion */
#define EVOL
#define LINUX
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>
#define L 8 //Se puede definir en tiempo de compilacion en al makefile
#define Dim 3

#define L1 (L-1)
#define L2 (L*L)
#define L3 (L*L*L)
#define V  (L*L*L)                     /* numero de sites         */
#define twopi 6.283185307
#define N_OTROS 3

#define precision float
#define N_DATOS_INT 6
#define N_DATOS_FLOAT 3


#ifdef TURBOC
#define NormRAN (1.0/( (float) RAND_MAX+1.0))
#define NormRANu (1.0/pow(2.0,32))
#endif

#ifdef SUN4
#define NormRAN  ((float) 4.656612595521636e-10)       
#define NormRANu ((float) (0.5*4.656612595521636e-10)) 
#endif
#ifdef LINUX
#define NormRAN  ((float) 4.656612595521636e-10)       
#define NormRANu ((float) (0.5*4.656612595521636e-10)) 
#endif

#define  RAN() ( (float) rand() * NormRAN )

/* nuevo generador random*/

#define  Nestm1  (Nest-1)

#define Normaener  ( (float) (1.0/(double) (V*Dim)))
#define Normamag   ( (float) (1.0/(double) V))
#define TWOPI      6.283185307    


#define n_obs n_ope


#define LPATH 100

struct s_datos
{
  long int itmax,           /* Numero de medidas por bloque                  */
           mesfr,           /* frecuencia de las medidas                     */
           nbin,            /* numero de bloque                              */
           itcut,           /* proximo bloque a calcular                     */
           flag,            /* conf de partida: 0(random), 1(fria),2(backup) */
           seed;            /* semilla random                                */
     float Kappa,          /* acoplamientos           */
           Lambda,         /* acoplamientos           */
           delta;           /* salto de Metropolis     */
};

