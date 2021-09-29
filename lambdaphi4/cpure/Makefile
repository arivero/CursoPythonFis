L=4
DEFINES=-DL=$(L)
OBJ   = root.o medidas.o lambda.o update.o inici.o
#CFLAGS= -g
CFLAGS= -O3 -Wall -funroll-loops -finline-functions 

iso: $(OBJ)
	gcc $(CFLAGS) $(OBJ) -lm -o phi_cl_$(L)
.c.o:
	gcc $(DEFINES)  -c $(CFLAGS) $<

clean: 
	/bin/rm -f $(OBJ) is

#		*Individual File Dependencies*
root.o: root.c lambda.h Makefile

medidas.o: medidas.c lambda.h Makefile

lambda.o: lambda.c lambda.h Makefile

update.o: update.c lambda.h Makefile

inici.o: inici.c lambda.h Makefile












