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

class Phrase:
    def __init__(self, name, tf_up, df_up, tf_down, df_down):
        self.name = name
        # Frequencies
        self.tf_up = tf_up
        self.df_up = df_up
        self.tf_down = tf_down
        self.df_down = df_down
        self.df_all = self.df_up + self.df_down # df_all

        # MI, tfidf, associations
        # UP
        self.MI_up = 0
        self.tfidf_up = 0
        self.supp_up = 0
        self.conf_up = 0
        self.lift_up = 0
        # Down
        self.MI_down = 0
        self.tfidf_down = 0
        self.supp_down = 0
        self.conf_down = 0
        self.lift_down = 0
        for elm in ['up', 'down']:
            self.calc_MI(elm)
            self.calc_tfidf(elm)
            self.calc_assocs(elm)

    def calc_MI(self, lmttyp):
        # MI = log(N(XY) / (N(X)N(Y)), belongs to df
        if lmttyp == 'up':
            self.MI_up = math.log(self.df_up + 1e-4 / (N_up*self.df_all))
        elif lmttyp == 'down':
            self.MI_down = math.log(self.df_down + 1e-4 / (N_down*self.df_all))

    def calc_tfidf(self, lmttyp):
        # tf-idf = (1+log(tf)) * log(N_ttl/df) ???
        N_tmp = N_up if lmttyp == 'up' else N_down
        if lmttyp == 'up':
            self.tfidf_up = (1+math.log(self.tf_up+1e-4)) * math.log(N_ttl/self.df_all)
        elif lmttyp == 'down':
            self.tfidf_down = (1+math.log(self.tf_down+1e-4)) * math.log(N_ttl/self.df_all)

    def calc_assocs(self, lmttyp):
        # Support P(XY) = N(XY)/N_ttl
        # Confidence(X->Y) P(Y|X) = P(XY)/P(X) = N(XY)/N(X)
        # Lift P(XY)/(P(X)P(Y)) = N_ttl*N(XY)/(N(X)N(Y))
        # Feature (X) -> up or down (Y)
        if lmttyp == 'up':
            self.supp_up = self.df_up / N_ttl
            self.conf_up = self.df_up / self.df_all
            self.lift_up = (N_ttl * self.df_up) / (self.df_all*N_up)
        elif lmttyp == 'down':
            self.supp_down = self.df_down / N_ttl
            self.conf_down = self.df_down / self.df_all
            self.lift_down = (N_ttl * self.df_down) / (self.df_all * N_down)

    def __str__(self):
        frqstr = 'Phrase:{}\nUP: tf={}, df={} \nDOWN: tf={}, df={} \n ALL:     , df={}\n'\
            .format(self.name, self.tf_up, self.df_up, self.tf_down, self.df_down, self.df_all)
        ascstr = 'UP: MI={:.3f}, tfidf={:.3f}, support={:.3f}, confidence={:.3f}, lift={:.3f} \nDOWN: MI={:.3f}, tfidf={:.3f}, support={:.3f}, confidence={:.3f}, lift={:.3f}'\
            .format(self.MI_up, self.tfidf_up, self.supp_up, self.conf_up, self.lift_up, self.MI_down, self.tfidf_down, self.supp_down, self.conf_down, self.lift_down)
        return frqstr + ascstr
    def toJSON(self):
        return json.dumps(self, default=lambda o:o.__dict__, sort_keys=True, indent=4)

def generatePhraseList():
    tf_up = JSON2COUNTER('up', 'tf')
    df_up = JSON2COUNTER('up', 'df')
    tf_down = JSON2COUNTER('down', 'tf')
    df_down = JSON2COUNTER('down', 'df')
    tf_all = JSON2COUNTER('all', 'tf')
    df_all = JSON2COUNTER('all', 'df')
    print(df_up)
    print(df_down)
    print(df_all)

    ret_lst = []
    for key, val in df_all.most_common():
        phrase = Phrase(name=key,
                        tf_up= tf_up[key] if key in tf_up else 0,
                        df_up= df_up[key] if key in df_up else 0,
                        tf_down= tf_down[key] if key in tf_down else 0,
                        df_down= df_down[key] if key in df_down else 0
                        )
        ret_lst.append(phrase)
    return ret_lst

def PhraseList2JSON(phraselist):
    with open('phraselist.json', 'w') as file:
        json.dump(phraselist, file, default=lambda o:o.__dict__, sort_keys=True, indent=4)

def main():
    with open('phraselist.json', 'r') as file:
        x = json.load(file)
    



if __name__ == '__main__':
    main()
