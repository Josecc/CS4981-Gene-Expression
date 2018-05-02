'''
Final Project: Normalization Stage
CS 4984: Computing the Brain
Author: Jose Canahui
Date: April 28th, 2018
'''

from scipy import stats
import pandas as pd
from multiprocessing import Pool
from tqdm import tqdm
import numpy as np

# Mutes errors that happen when trying to get z-score of row filled with zeros
np.seterr(divide='ignore', invalid='ignore')

#------------------------- Instantiating Reader/Pool --------------------------#

chunksize = 7
p = Pool(32)
df = pd.read_csv('exons-new-table.csv', header=None, index_col=0, chunksize=chunksize)

#--------------------------- Multithreading Function --------------------------#
'''
Will run several times in a pool under different threads to calculate z-score
of each row and save to file. The chunks for large columns are recommended to be
smaller so multithreading can be mostly used.
@param chunk is a chunk of rows to work on
'''
def norm(chunk):
    for i, row in chunk.iterrows():
        chunk.at[i] = stats.zscore(row)
    chunk.to_csv('exons-norm-1.csv', mode='a', header=False)

#--------------------- Read, Transform, and Track Chunks ----------------------#
total_progress=50281/chunksize
for _ in tqdm(p.imap_unordered(norm, df), total=total_progress):
    pass

#-------------------------------- Close Tools ---------------------------------#
p.close()
p.join()
pbar.close()
