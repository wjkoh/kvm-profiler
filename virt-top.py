import subprocess
import time
import csv

args = ['virt-top', '-b', '--script', '-d', '1', '--csv', '/dev/stdout']
p = subprocess.Popen(args, stdout = subprocess.PIPE)

def make_inf_gen(head, repeat):
    yield head
    while True:
        yield repeat

header = None
while p.poll() is None:
    output = p.stdout.readline()
    for row in csv.reader([output]):
        if header is None:
            header = row
            domain_idx = header.index('Domain ID')
        else:
            header_gen = (x for l in make_inf_gen(header[:domain_idx], header[domain_idx:]) for x in l)
            zipped = zip(header_gen, row)
            print zipped
