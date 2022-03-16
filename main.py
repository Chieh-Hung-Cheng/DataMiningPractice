import argparse
import os
import sys
import time
parser = argparse.ArgumentParser()
parser.add_argument('--supp_up', default=0.105, type=float)
parser.add_argument('--conf_up', default=0, type=float)
parser.add_argument('--lift_up', default=0, type=float)
parser.add_argument('--tfidf_up', default=0, type=float)
#parser.add_argument('--MI_up', default=sys.float_info.min, type=float)
#parser.add_argument('--chisq_up', default=sys.float_info.min, type=float)

parser.add_argument('--supp_down', default=0.015, type=float)
parser.add_argument('--conf_down', default=0.2, type=float)
parser.add_argument('--lift_down', default=1, type=float)
parser.add_argument('--tfidf_down', default=0, type=float)
#parser.add_argument('--MI_down', default=sys.float_info.min, type=float)
#parser.add_argument('--chisq_down', default=sys.float_info.min, type=float)

args = parser.parse_args()

limitations = vars(args)

import numpy as np
import math
from tqdm import tqdm
import json

import monpa
from collections import Counter
import csv

from frequencies import *
from doc_utils import *
from phrase import *
from relevance import *
from NaiveBayes import *
from other_utils import *

def main():
    force = False
    if (not os.path.exists('tf_up.json')) or force: generateAllFreqs()
    if (not os.path.exists('phraselist.json')) or force: generatePhraseList()
    if (not os.path.exists('tfdoc_up.json')) or force: generateTermFreqEachDoc()
    # Q1
    showLimitaions(limitations)
    phraselist_up, phraselist_down = generateUPDOWNlist(limitations)
    print('UP LIMIT LIST:')
    showNameList(phraselist_up)
    print('\nDOWN LIMIT LIST:')
    showNameList(phraselist_down)
    print('_'*70)

    # Q2
    ip = input('Paste the article below to SEARCH and CATEGORIZE:\n')
    phraselist_ttl = phraselist_up + phraselist_down
    searchByString(ip, phraselist_ttl)
    print('_'*70)
    # Q3
    sample_content = ip
    sample_tfcounter = Counter(frequencies.getPhraseLongEnoughImproved(sample_content))
    classifyByBayes(sample_tfcounter, phraselist_up, phraselist_down)

def test():
    xargs = vars(args)
    print(xargs)
    print(type(xargs))
if __name__ == '__main__':
    main()
