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

def tfidf(tf_ctr, df_ctr):
    # return a sorted LIST
    # tf-idf = (1+log(tf)) * log(N_ttl/df)
    ret_dict = {}
    for idx, elm in enumerate(tf_ctr.most_common()):
        ret_dict[elm[0]] = (1 + math.log(elm[1])) * math.log(N_ttl/df_ctr[elm[0]])

    return sorted(ret_dict.items(), key=lambda x: x[1], reverse=True)

def MI_tfidf(lmttyp, tf_ctr, df_ctr, df_all_ctr):
    # tf-idf = (1+log(tf)) * log(N_ttl/df)
    # MI = log(N(XY) / N(X)N(Y)), belongs to df
    N_tmp = N_up if lmttyp=='up' else N_down
    ret_dict = {}
    for idx, elm in enumerate(tf_ctr.most_common()):
        # elm[0]: feature, elm[1]: count
        MI = math.log(df_ctr[elm[0]] / (N_tmp * df_all_ctr[elm[0]]))
        tid = (1 + math.log(elm[1])) * math.log(N_tmp/df_ctr[elm[0]])
        ret_dict[elm[0]] = MI*tid

    return sorted(ret_dict.items(), key=lambda x: x[1], reverse=True)

def associations(lmttyp, df_ctr, df_all_ctr):
    # Support P(XY) = N(XY)/N_ttl
    # Confidence(X->Y) P(Y|X) = P(XY)/P(X) = N(XY)/N(X)
    # Lift P(XY)/(P(X)P(Y)) = N_ttl*N(XY)/(N(X)N(Y))
    # Feature (X) -> up or down (Y)
    N_tmp = N_up if lmttyp=='up' else N_down

    sup_dict = {}
    cfd_dict = {}
    lft_dict = {}
    for idx, elm in enumerate(df_ctr.most_common()):
        # elm[0]: feature, elm[1]: counts
        sup_dict[elm[0]] = df_ctr[elm[0]] / N_ttl
        cfd_dict[elm[0]] = df_ctr[elm[0]] / df_all_ctr[elm[0]]
        lft_dict[elm[0]] = (N_ttl * df_ctr[elm[0]]) / (df_all_ctr[elm[0]] * N_tmp)
    ret_sup_lst = sorted(sup_dict.items(), key=lambda x: x[1], reverse=True)
    ret_cfd_lst = sorted(cfd_dict.items(), key=lambda x: x[1], reverse=True)
    ret_lft_lst = sorted(lft_dict.items(), key=lambda x: x[1], reverse=True)
    return ret_sup_lst, ret_cfd_lst, ret_lft_lst

def main():
    tf_up = JSON2COUNTER('up', 'tf')
    df_up = JSON2COUNTER('up', 'df')
    tf_down = JSON2COUNTER('down', 'tf')
    df_down = JSON2COUNTER('down', 'df')
    tf_all = JSON2COUNTER('all', 'tf')
    df_all = JSON2COUNTER('all', 'df')

    print(df_up)
    print(df_down)
    print(df_all)

    sup_lst, cfd_lst, lft_lst = associations('up', df_up, df_all)
    print(sup_lst[0:20])
    print(cfd_lst[0:20])
    print(lft_lst[0:20])

if __name__ == '__main__':
    main()
