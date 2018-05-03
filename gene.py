from sys import stdout

def clean_line(line):
    line = line.replace('\n','')
    line = line.replace('\"','')
    line = line.split(',')
    return line

EXONS_TABLE = 'exons-norm-1.csv'
STD_DEV_THRESH = 195

print 'Threshold is {0}'.format(STD_DEV_THRESH)

genes = []
with open(EXONS_TABLE) as fp:
    print 'Pulling genes from {0}'.format(EXONS_TABLE)
    for row in fp.readlines():
        row = clean_line(row)
        gene = row[0]
        for nucleus in row[1:]:
            try:
                if nucleus != '':
                    if abs(float(nucleus)) > STD_DEV_THRESH:
                        genes.append(gene)
            except ValueError:
                ''' This exception is here to handle the error
                thrown when the float has the letters in it'''
                pass

print '\nFound {0} genes over the threshold'.format(len(genes))
print genes
