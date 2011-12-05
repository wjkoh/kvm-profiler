/* MEMORY UTILIZATION BENCHMARK PROGRAM.
 *
 * OPTIONS
 * -r: random access option
 * -w: read-write or read-only
 * -s: the size of the memory (in number of pages)
 * -n: the number of operations (n = 0 means forever)
 *
 * EXAMPLES
 * ./memory -r -s 10000 -n 100000000
 * random: 1
 * write: 0
 * size: 10000
 * n: 100000000
 * 
 * real	0m6.939s
 * user	0m6.900s
 * sys	0m0.012s
 *
 * time ./memory -s 10000 -n 100000000
 * random: 0
 * write: 0
 * size: 10000
 * n: 100000000
 * 
 * real	0m1.248s
 * user	0m1.236s
 * sys	0m0.004s
 */

#include <cstdio>
#include <cstdlib>
#include <unistd.h>

using namespace std;

const int PAGE_SIZE = 4096;

bool random_flag, write_flag;
int size = -1, n = -1;

int main (int argc, char **argv)
{
    int c;
    while ((c = getopt (argc, argv, "rws:n:")) != -1)
    {
        switch (c)
        {
        case 'r':
            random_flag = true;
            break;
        case 'w':
            write_flag = true;
            break;
        case 's':
            size = atoi (optarg);
            break;
        case 'n':
            n = atoi (optarg);
            break;
        default:
            fprintf (stderr, "Invalid option.\n");
            return 1;
        }
    }

    if (size < 0)
    {
        fprintf (stderr, "Invalid size.\n");
        return 1;
    }

    if (n < 0)
    {
        fprintf (stderr, "Invalid n.\n");
        return 1;
    }
    
    printf ("random: %d\nwrite: %d\nsize: %d\nn: %d\n", random_flag, write_flag, size, n);
    srand (19890509);

    char **mem = (char **) malloc (size * sizeof (char *));
    if (random_flag)
    {
        for (int i = 0; i < size; ++i)
        {
            mem[i] = (char *) malloc (PAGE_SIZE * sizeof (char));
        }
    }
    else
    {
        mem[0] = (char *) malloc (size * PAGE_SIZE * sizeof (char));
        for (int i = 1; i < size; ++i)
        {
            mem[i] = mem[0] + i * PAGE_SIZE;
        }
    }

    int ptr = 0;
    char t;
    
    for (int i = 0; n == 0 || i < n; ++i)
    {
        ptr = (random_flag ? rand() : ptr + 1) % size;

        if (write_flag && (rand() % 2))
        {
            mem[ptr][rand() % PAGE_SIZE] = rand();
        }
        else
        {
            t = mem[ptr][rand() % PAGE_SIZE];
        }
    }

    return 0;
}
