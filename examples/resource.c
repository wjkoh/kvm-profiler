/* RESOURCE UTILIZATION BENCHMARK PROGRAM.
 *
 * OPTIONS
 * -r: random access
 * -w: read-write or read-only
 * -d: disk operation
 * -s: the size of the disk or the memory space (in number of pages)
 * -n: the number of operations (n = 0 means forever)
 *
 * USAGE
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
 *
 * time ./memory -d -s 1000000 -n 1000
 * random: 0
 * write: 0
 * disk: 1
 * size: 1000000
 * n: 1000
 * 1000000+0 records in
 * 1000000+0 records out
 * 4096000000 bytes (4.1 GB) copied, 30.6082 s, 134 MB/s
 * 
 * real	0m30.697s
 * user	0m0.144s
 * sys	0m3.980s
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>

const int PAGE_SIZE = 4096;

bool random_flag, write_flag, disk_flag;
int size = -1, n = -1;

int main (int argc, char **argv)
{
    int c;
    while ((c = getopt (argc, argv, "rwds:n:")) != -1)
    {
        switch (c)
        {
        case 'r':
            random_flag = true;
            break;
        case 'w':
            write_flag = true;
            break;
        case 'd':
            disk_flag = true;
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
    
    printf ("random: %d\nwrite: %d\ndisk: %d\nsize: %d\nn: %d\n", random_flag, write_flag, disk_flag, size, n);
    srand (19890509);

    FILE *file;
    char **mem;
    char cmd[100];

    if (disk_flag)
    {
        sprintf (cmd, "dd if=/dev/zero of=file.dat bs=4096 count=%d", size);
        system (cmd);
        file = fopen ("file.dat", "rw");
    }
    else
    {
        mem = (char **) malloc (size * sizeof (char *));
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
    }

    int ptr0 = 0, ptr1 = 0;
    char t;
    
    for (int i = 0; n == 0 || i < n; ++i)
    {
        if (disk_flag)
        {
            if (random_flag)
            {
                fseek (file, rand() % (size * PAGE_SIZE), SEEK_SET);
            }
            else
            {
                if (fseek (file, 1, SEEK_CUR) != 0)
                {
                    fseek (file, 0, SEEK_SET);
                }
            }

            if (write_flag && (rand() % 2))
            {
                fwrite (cmd, 1, 1, file);
            }
            else
            {
                fread (cmd, 1, 1, file);
            }
        }
        else
        {
            if (random_flag)
            {
                ptr0 = rand() % size;
                ptr1 = rand() % PAGE_SIZE;
            }
            else
            {
                if ((++ptr1) == PAGE_SIZE)
                {
                    ptr0 = (ptr0 + 1) % size;
                    ptr1 = 0;
                }
            }

            if (write_flag && (rand() % 2))
            {
                mem[ptr0][ptr1] = rand();
            }
            else
            {
                t = mem[ptr0][ptr1];
            }
        }
    }

    if (disk_flag)
    {
        fclose (file);
        system ("rm file.dat");
    }
    else
    {
        if (random_flag)
        {
            for (int i = 0; i < size; ++i)
            {
                free (mem[i]);
            }
        }
        else
        {
            free (mem[0]);
        }
        free (mem);
    }
    
    return 0;
}
