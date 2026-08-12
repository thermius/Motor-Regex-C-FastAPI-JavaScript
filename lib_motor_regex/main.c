#include "motor_regex.c"
#include <stdio.h>

int main ()
{
	ResultadoRegex *analise = MotorRegex ("Este e um texto com exatamente cem caracteres para voce usar onde e como precisar. Tudo certo!","E*ste e um text c|oom");
	printf("status: %i\n",analise->aceito);
	 free (analise);
	return 0;
}