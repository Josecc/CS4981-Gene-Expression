import sys
from sets import Set

def binsearch(sorted_list, key):
    while len(sorted_list) > 0:
        i = len(sorted_list) / 2
        if key == sorted_list[i]:
            return True
        elif len(sorted_list) == 1:
            return False
        elif key < sorted_list[i]:
            sorted_list = sorted_list[:i]
        else:
            sorted_list = sorted_list[i:]

COLUMNS_NUCLEI_FILE = 'columns-nuclei.csv'
EXONS_FILE = 'exons-table.csv'
OUTPUT_FILE = 'exons-new-table.csv'

def clean_line(line):
    line = line.replace('\n', '')
    line = line.replace('\"', '')
    line = line.split(',')
    return line

print 'Finding NeuN+ cells...'
neun_p = ['']
with open(COLUMNS_NUCLEI_FILE) as fp:
    for line in fp.readlines():
        line = line.split(',')
        if 'NeuN-positive' in line[7]:
            neun_p.append(str(line[0]))

neun_p = sorted(neun_p)

with open(EXONS_FILE) as fp:
    with open(OUTPUT_FILE, 'w+') as output:
        line = clean_line(fp.readline())

        print 'Determining what columns we want...'
        desired_cols = Set([])
        for i, entry in enumerate(line):
            if binsearch(neun_p, str(entry)):
                desired_cols.add(i)

        print 'Pulling out desired columns...'
        cnt = 0
        for line in fp.readlines():
            cnt += 1
            if cnt % 1000 == 0:
                sys.stdout.write('.')
                sys.stdout.flush()

            line = clean_line(line)
            new_row = ''
            for i, col in enumerate(line):
                if i in desired_cols:
                    new_row = '{0},{1}'.format(new_row, col)

            new_row = '{0}\n'.format(new_row[1:]) # cut off unnecessary first comma and add \n
            output.write(new_row)
