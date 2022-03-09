import os
import sys
import time

import numpy as np
import math
from tqdm import tqdm
import json

import monpa
from collections import Counter
import csv

from frequencies import *
from doc_utils import *

N_up = 612 # 613-1
N_down = 126 # 127-1
N_ttl = 738 # 613+127-1-1

def tf_idf(tf_cnt, df_cnt):
    # tf-idf = (1+log(tf))*log(N/df)
    # MI =
    ret_dict = {}
    for idx, elm in enumerate(tf_cnt.most_common()):
        ret_dict[elm[0]] = (1 + math.log(elm[1])) * math.log(N_ttl/df_cnt[elm[0]])

    return ret_dict



def main():
    tf_up = JSON2COUNTER('up', 'tf')
    df_up = JSON2COUNTER('up', 'df')
    tf_down = JSON2COUNTER('down', 'tf')
    df_down = JSON2COUNTER('down', 'df')

    tfidfDict = tf_idf(tf_up, df_up)
    tfidfSorted = sorted(tfidfDict.items(), key=lambda x:x[1], reverse=True)
    print(tfidfSorted[0:10])

if __name__ == '__main__':
    main()
