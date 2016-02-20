/*
-------------------------------------------------------------------------------
primes.c
-------------------------------------------------------------------------------
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <time.h>
#include <math.h>
#include <limits.h>
#include <sys/types.h>
#include <sys/time.h>
#include <sys/stat.h>

#define DIAG_PRINT 1

// Function prototypes

long long sqrtll( long long x );
void usage();

// main program

int main( int argc, char *argv[])
{ // begin main()

// Declarations

extern char
  *optarg;

extern int
  optind,
  opterr,
  optopt;

int
  remaining_args,
  i,
  c;

long long
  start_search,
  end_search,
  i_div,
  i_div_tot,
  x,
  divisor,
  max_divisor,
  remainder;

char
  *ptr;

//----------------------
// Begin executable code
//----------------------

// May have up to two optional args:
//
//  -s <search_start>
//  -e <search_end>

clock_t begin, end;
double time_spent;
begin = clock();

if( DIAG_PRINT )
  {
  printf("\n");
  printf("primes.c DIAGNOSTIC OUTPUT:\n\n");
  printf("Command line arguments:\n\n");
  for (i=0; i<argc; i++)
    {
    printf("  iarg = %d, arg = '%s'\n", i, argv[i]);
    }
  printf("\n");
  printf("  optind    = %d\n", optind);
  printf("  opterr    = %d\n", opterr);
  printf("  optopt    = %d\n", optopt);
  printf("  LLONG_MAX = %lld\n", LLONG_MAX);
  }

// Parse command line arguments

start_search = 1;
end_search = LLONG_MAX;

while ((c = getopt( argc, argv, "s:e:")) != EOF)
  {
  //printf("DEBUG: c = %d [%c]\n", c, (char) c );
  switch (c)
    {
    case 's':
      //printf("DEBUG: case 's': optarg = '%s'\n", optarg);
      start_search = atoll(optarg);
      //printf("DEBUG: start_search = %d\n", start_search);
      break;
    case 'e':
      //printf("DEBUG: case 'e': optarg = '%s'\n", optarg);
      end_search = atoll(optarg);
      //printf("DEBUG: end_search = %d\n", end_search);
      break;
    case '?':
      printf("ERROR: unrecognized option '%s'", optarg);
      usage();
      exit(1);
      break;
    } // end switch
  } // end while

//printf("DEBUG: start_search = %d, end_search = %d\n",
//       start_search, end_search);
  
remaining_args = argc - optind;

if (DIAG_PRINT)
  {
  printf("\n");
  printf("Parameters set from command line arguments:\n\n");
  printf("  start_search   = %lld\n", start_search);
  printf("  end_search     = %lld\n", end_search);
  printf("  remaining_args = %d\n", remaining_args);
  }

// start_search and end_search must be greater than zero

if (start_search < 0 || end_search < 0)
  {
  printf("ERROR: -s and -e must be greater than zero");
  usage();
  exit(1);
  }

// start_search must be less than end_search

if (start_search >= end_search)
  {
  printf("ERROR: -s must be less than -e");
  usage();
  exit(2);
  }

// start_search must be an odd number

if (start_search % 2 == 0)
  start_search += 1;

x         = start_search;
i_div     = 0;
i_div_tot = 0;

while (x < end_search)
  { // START while (x < end_search)

  max_divisor = sqrtll(x);
  if (max_divisor % 2 == 0)
    max_divisor += 1;

  divisor   =  3;
  remainder = -1;

  //if (DIAG_PRINT)
  //  printf("x = %d, max_divisor = %d\n", x, max_divisor);

  //i_div = 0;

  while ((divisor <= max_divisor) && (remainder != 0))
    {
    remainder = x % divisor;
    divisor += 2;
    i_div += 1;
    }

  if (remainder != 0)
    {
    printf("%lld [%lld]\n", x, i_div);
    i_div_tot += i_div;
    i_div = 0;
    }

  x += 2;

  } // END while (x < end_search)

end = clock();
time_spent = (double)(end - begin) / CLOCKS_PER_SEC;

long long
  div_per_second = i_div_tot / time_spent;

printf("Total divisors checked      = %lld\n", i_div_tot);
printf("Divisors checked per second = %lld\n\n", div_per_second);

if (DIAG_PRINT)
  printf("\n");

// Exit with status 0: keeps Make happier.
exit(0);

// Makes gcc happier.
return(0);

} // end main()

//////////////////////////////////////////////////////////////////////////////

void usage()
{
}


// http://stackoverflow.com/questions/18499492/how-can-you-easily-calculate-the-square-root-of-an-unsigned-long-long-in-c
// Then this code calculates the square root of x, truncated to an integer,
// provided the operations conform to IEEE 754:

long long sqrtll( long long x )
{
long long y;

//if(DIAG_PRINT)
//  printf("sqrtll: x = %d\n", x);

y = sqrt( x ) - 0x1p-20;
if (2*y < x - y*y)
  ++y;

return y;
}
